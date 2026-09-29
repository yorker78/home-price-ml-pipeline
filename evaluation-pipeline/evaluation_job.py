import os

import psycopg
import requests
from psycopg.rows import dict_row


def check_environment():
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')
    host = os.getenv('DB_HOST')
    if user is not None and password is not None and host is not None:
        return 0
    elif password is not None and host is not None:
        return 1
    elif user is not None and host is not None:
        return 2
    elif user is not None and password is not None:
        return 3
    elif host is not None:
        return 4
    elif password is not None:
        return 5
    elif user is not None:
        return 6
    else:
        return 7

def run_job():
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASS')
    db_host = os.getenv('DB_HOST')
    
    pr_host = os.getenv('PR_HOST')
    pr_port = os.getenv('PR_PORT')
    
    conn_string = 'postgresql://{}:{}@{}:5432/house_price_prediction_service'.format(db_user, db_password, db_host)    
    print('Job Starting...')
    model_id = requests.get(f'http://{pr_host}:{pr_port}/model-id').json()['model_id']
    with psycopg.connect(conn_string, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(f'SELECT id, event_timestamp, data FROM raw_home_sale_events WHERE id NOT IN (SELECT id FROM evaluated_event_ids WHERE evaluated_event_ids.model_id=\'{model_id}\') ORDER BY event_timestamp DESC LIMIT 15000;')
            conn.commit()
            raw_events = cur.fetchall()
            for raw_event in raw_events:
                event = raw_event['data']
                event['id'] = raw_event['id']
                event['event_timestamp'] = str(raw_event['event_timestamp'])
                event['zipcode'] = str(event['zipcode'])
                response = requests.post(f'http://{pr_host}:{pr_port}/predicted-home-value', json={'property': event})
                if response.status_code == requests.codes.ok:
                    body = response.json()
                    predicted_price = body['predicted_price']
                    model_id = body['model_id']
                    cur.execute(f'''INSERT INTO evaluated_home_sale_events
                                (id, model_id, sale_date, true_price, predicted_price)
                                VALUES
                                ({event['id']}, \'{model_id}\', \'{event['event_timestamp']}\', {event['price']}, {predicted_price});
                                ''')
                else:
                    print(response.json()['error_message'])
                cur.execute(f'''INSERT INTO evaluated_event_ids
                            (id, model_id)
                            VALUES
                            ({event['id']}, \'{model_id}\');
                            ''')
                conn.commit()
    print('Job Finished')

if __name__ == '__main__':
    if check_environment() == 0:
        run_job()
    print('Environment Variables are not set.')