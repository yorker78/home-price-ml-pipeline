import argparse
import datetime as dt
import os

import dill as pickle
import pandas as pd
import psycopg
from flask import Flask, abort, jsonify, request
from home_event import HomeEvent
from marshmallow import ValidationError
from psycopg.rows import dict_row

messages = []

def parse_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--model-fl', type=str, required=True)
    
    parser.add_argument('--model-identifier', type=str, required=True)
    
    args = parser.parse_args()
    
    return args.model_fl, args.model_identifier

def connect_db(username, password, host):
    conn_string = f'postgresql://{username}:{password}@{host}:5432/house_price_prediction_service'
    
    conn = psycopg.connect(conn_string, row_factory=dict_row)
    
    return conn

def create_app(conn, schema, model, model_id):
    app = Flask(__name__)

    @app.errorhandler(400)
    def bad_request(error):
        message = messages[0]
        messages.clear()
        return jsonify({'error_message': message, 'model_id': model_id}), 400
    
    @app.get('/ping')
    def ping():
        return jsonify('pong!')
    
    @app.get('/model-id')
    def get_model_id():
        return jsonify({'model_id': model_id})
    
    @app.post('/predicted-home-value')
    def predicted_home_value():
        time = dt.datetime.now()
        raw_prop = check_body(request)
        prop = raw_prop['property']
        zipcode = prop['zipcode']
        get_complimentary_data(conn, prop, zipcode)
        valid_prop = check_schema(schema, prop)
        predicted_price = predict_price(model, conn, model_id, time, valid_prop)
        return jsonify({'predicted_price': predicted_price, 'model_id': model_id})
    
    return app

def check_body(request):
    if request.get_json(silent=True) is None:
        messages.append('Empty Body!')
        abort(400)
    raw_prop = request.get_json(silent=True)
    if 'property' not in raw_prop.keys():
        messages.append('\'property\' must be a top level object key to property object')
        abort(400)
    if 'zipcode' not in raw_prop['property'].keys() or not isinstance(raw_prop['property']['zipcode'], str) or not raw_prop['property']['zipcode'].isnumeric() or len(raw_prop['property']['zipcode']) != 5:
        messages.append('\'zipcode\' must be a numeric string of length 5')
        abort(400)
    return raw_prop

def get_complimentary_data(conn, prop, zipcode):
    with conn.cursor() as cur:
        cur.execute(f'SELECT population FROM cleaned_zipcode_populations WHERE zipcode = \'{zipcode}\';')
        conn.commit()
        pop = cur.fetchone()
        prop['zipcode_population'] = pop['population']
        cur.execute(f'SELECT high_schools, middle_schools, primary_schools, other_schools, unknown_schools, total_schools FROM cleaneD_zipcode_public_schools WHERE zipcode = \'{zipcode}\'')
        conn.commit()
        schools = cur.fetchone()
        prop['zipcode_public_high_schools'] = schools['high_schools']
        prop['zipcode_public_middle_schools'] = schools['middle_schools']
        prop['zipcode_public_primary_schools'] = schools['primary_schools']
        prop['zipcode_public_other_schools'] = schools['other_schools']
        prop['zipcode_public_unknown_schools'] = schools['unknown_schools']
        prop['zipcode_public_total_schools'] = schools['total_schools']

def check_schema(schema, prop):
    try:
        validation = schema.load(prop)
        return validation
    except ValidationError as err:
        messages.append(err.messages)
        abort(400)

def predict_price(model, conn, model_id, time, prop):
    data = {k:[v] for k,v in prop.items()}
    predicted_price = model.predict(pd.DataFrame(data))[0]
    with conn.cursor() as cur:
        cur.execute(f'''INSERT INTO predicted_prices
                        (model_id, request_timestamp, predicted_price)
                        VALUES
                        (\'{model_id}\', \'{time}\', {predicted_price})
                        ''')
    return predicted_price

if __name__ == "__main__":
    host = os.environ.get('SERVICE_HOST')
    port = os.environ.get('SERVICE_PORT')
    
    pg_username = os.environ['POSTGRES_USERNAME']
    pg_password = os.environ['POSTGRES_PASSWORD']
    pg_host = os.environ['POSTGRES_HOST']
    
    model_fl, model_id = parse_args()
    schema = HomeEvent()
    
    with open(model_fl, "rb") as fl:
        model = pickle.load(fl)
    
    conn = connect_db(pg_username, pg_password, pg_host)
    
    app = create_app(conn, schema, model, model_id)
    
    app.run(host=host, port=port)
