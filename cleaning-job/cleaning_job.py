import os

import psycopg
from home_event import HomeEvent
from marshmallow import ValidationError
from psycopg.rows import dict_row

"""
Query unprocessed home sale events from the raw home sale events table by 
looking for ids not in the processed ids table
"""
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
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')
    host = os.getenv('DB_HOST')
    conn_string = 'postgresql://{}:{}@{}:5432/house_price_prediction_service'.format(user, password, host)
    schema = HomeEvent()
    print('Job Starting...')
    with psycopg.connect(conn_string, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, event_timestamp, data FROM raw_home_sale_events WHERE id NOT IN (SELECT id FROM processed_home_sale_events) ORDER BY event_timestamp DESC LIMIT 10000;')
            conn.commit()
            raw_events = cur.fetchall()
            cur.execute('SELECT zipcode, population FROM cleaned_zipcode_populations;')
            conn.commit()
            pops = cur.fetchall()
            cur.execute('SELECT zipcode, high_schools, middle_schools, primary_schools, other_schools, unknown_schools, total_schools FROM cleaned_zipcode_public_schools;')
            conn.commit()
            schools = cur.fetchall()
            for raw_event in raw_events:
                event = raw_event['data']
                event['id'] = raw_event['id']
                event['event_timestamp'] = raw_event['event_timestamp']
                filtered_pop = list(filter(lambda x: int(x['zipcode']) == event['zipcode'], pops))
                if len(filtered_pop) == 0:
                    continue
                event['zipcode_population'] = filtered_pop[0]['population']
                zipcode_schools = list(filter(lambda x: int(x['zipcode']) == event['zipcode'], schools))
                if len(zipcode_schools) == 0:
                    continue
                event['zipcode_public_high_schools'] = zipcode_schools[0]['high_schools']
                event['zipcode_public_middle_schools'] = zipcode_schools[0]['middle_schools']
                event['zipcode_public_primary_schools'] = zipcode_schools[0]['primary_schools']
                event['zipcode_public_other_schools'] = zipcode_schools[0]['other_schools']
                event['zipcode_public_unknown_schools'] = zipcode_schools[0]['unknown_schools']
                event['zipcode_public_total_schools'] = zipcode_schools[0]['total_schools']
                try:
                    validation = schema.load(event)
                    keys = event.keys()
                    key_string = '('
                    value_string = '('
                    for key in keys:
                        key_string += f'{key}, '
                        if key == 'event_timestamp':
                            value_string += f'\'{validation[key]}\', '
                        else:
                            value_string += f'{validation[key]}, '
                    key_string = key_string[:-2] + ')'
                    value_string = value_string[:-2] + ')'
                    cur.execute(f'''INSERT INTO processed_home_sale_events
                                (id)
                                VALUES
                                ({validation['id']})
                                ON CONFLICT DO NOTHING;
                                ''')
                    cur.execute(f'''INSERT INTO cleaned_home_sale_events
                                {key_string}
                                VALUES
                                {value_string}
                                ON CONFLICT DO NOTHING;
                                ''')
                    conn.commit()
                except ValidationError as err:
                    print(err.messages)
                    cur.execute(f'''INSERT INTO processed_home_sale_events
                                (id)
                                VALUES
                                ({event['id']})
                                ON CONFLICT DO NOTHING;
                                ''')
                    conn.commit()
    print('Job Finished')

if __name__ == "__main__":
    if check_environment() == 0:
        run_job()
    print('Environment Variables are not set.')