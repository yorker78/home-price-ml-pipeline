import json
import unittest
from unittest.mock import MagicMock

import dill as pickle
import prediction_service


class TestPredictionService(unittest.TestCase):
    
    def setUp(self):
        self.app = prediction_service.create_app(None, prediction_service.HomeEvent(), None, 'test_model')
        self.client = self.app.test_client()
    
    def tearDown(self):
        pass
    
    def test_ping(self):
        response = self.client.get('/ping')
        assert response.status == '200 OK'
        assert response.json == 'pong!'
    
    def test_empty_payload(self):
        data = {}
        response = self.client.post('/predicted-home-value', content_type='application/json', data=data)
        assert response.status == '400 BAD REQUEST'
        assert len(response.json['error_message']) > 0
        assert response.json['error_message'] == 'Empty Body!'
        
    def test_non_property_payload(self):
        data = {
            'lat': '47.6916',
            'long': '-122.341',
            'view': 0,
            'grade': 8,
            'floors': 3.0,
            'zipcode': '98103',
            'bedrooms': 3,
            'sqft_lot': 1448,
            'yr_built': 2005,
            'bathrooms': 2.25,
            'condition': 3,
            'sqft_above': 1430,
            'sqft_lot15': 1383,
            'waterfront': 0,
            'sqft_living': 1430,
            'yr_renovated': 0,
            'sqft_basement': 0,
            'sqft_living15': 1430,
            'event_timestamp': '2026-06-27T22:02:03.61179',
            'economic_conditions': 1.0
        }
        
        response = self.client.post('/predicted-home-value', content_type='application/json', data=json.dumps(data))
        assert response.status == '400 BAD REQUEST'
        assert len(response.json['error_message']) > 0
        assert response.json['error_message'] == '\'property\' must be a top level object key to property object'
    
    def test_empty_zipcode_payload(self):
        data = {
            'property': {
                'lat': '47.6916',
                'long': '-122.341',
                'view': 0,
                'grade': 8,
                'floors': 3.0,
                'bedrooms': 3,
                'sqft_lot': 1448,
                'yr_built': 2005,
                'bathrooms': 2.25,
                'condition': 3,
                'sqft_above': 1430,
                'sqft_lot15': 1383,
                'waterfront': 0,
                'sqft_living': 1430,
                'yr_renovated': 0,
                'sqft_basement': 0,
                'sqft_living15': 1430,
                'event_timestamp': '2026-06-27T22:02:03.61179',
                'economic_conditions': 1.0
            }
        }
        
        response = self.client.post('/predicted-home-value', content_type='application/json', data=json.dumps(data))
        assert response.status == '400 BAD REQUEST'
        assert len(response.json['error_message']) > 0
        assert response.json['error_message'] == '\'zipcode\' must be a numeric string of length 5'
    
    def test_nonstring_zipcode_payload(self):
        data = {
            'property': {
                'lat': '47.6916',
                'long': '-122.341',
                'view': 0,
                'grade': 8,
                'floors': 3.0,
                'zipcode': 98103,
                'bedrooms': 3,
                'sqft_lot': 1448,
                'yr_built': 2005,
                'bathrooms': 2.25,
                'condition': 3,
                'sqft_above': 1430,
                'sqft_lot15': 1383,
                'waterfront': 0,
                'sqft_living': 1430,
                'yr_renovated': 0,
                'sqft_basement': 0,
                'sqft_living15': 1430,
                'event_timestamp': '2026-06-27T22:02:03.61179',
                'economic_conditions': 1.0
            }
        }
        
        response = self.client.post('/predicted-home-value', content_type='application/json', data=json.dumps(data))
        assert response.status == '400 BAD REQUEST'
        assert len(response.json['error_message']) > 0
        assert response.json['error_message'] == '\'zipcode\' must be a numeric string of length 5'
    
    def test_nonnumeric_zipcode_payload(self):
        data = {
            'property': {
                'lat': '47.6916',
                'long': '-122.341',
                'view': 0,
                'grade': 8,
                'floors': 3.0,
                'zipcode': '981O3',
                'bedrooms': 3,
                'sqft_lot': 1448,
                'yr_built': 2005,
                'bathrooms': 2.25,
                'condition': 3,
                'sqft_above': 1430,
                'sqft_lot15': 1383,
                'waterfront': 0,
                'sqft_living': 1430,
                'yr_renovated': 0,
                'sqft_basement': 0,
                'sqft_living15': 1430,
                'event_timestamp': '2026-06-27T22:02:03.61179',
                'economic_conditions': 1.0
            }
        }
        
        response = self.client.post('/predicted-home-value', content_type='application/json', data=json.dumps(data))
        assert response.status == '400 BAD REQUEST'
        assert len(response.json['error_message']) > 0
        assert response.json['error_message'] == '\'zipcode\' must be a numeric string of length 5'
    
    def test_short_zipcode_payload(self):
        data = {
            'property': {
                'lat': '47.6916',
                'long': '-122.341',
                'view': 0,
                'grade': 8,
                'floors': 3.0,
                'zipcode': '9810',
                'bedrooms': 3,
                'sqft_lot': 1448,
                'yr_built': 2005,
                'bathrooms': 2.25,
                'condition': 3,
                'sqft_above': 1430,
                'sqft_lot15': 1383,
                'waterfront': 0,
                'sqft_living': 1430,
                'yr_renovated': 0,
                'sqft_basement': 0,
                'sqft_living15': 1430,
                'event_timestamp': '2026-06-27T22:02:03.61179',
                'economic_conditions': 1.0
            }
        }
        
        response = self.client.post('/predicted-home-value', content_type='application/json', data=json.dumps(data))
        assert response.status == '400 BAD REQUEST'
        assert len(response.json['error_message']) > 0
        assert response.json['error_message'] == '\'zipcode\' must be a numeric string of length 5'
    
    def test_long_zipcode_payload(self):
        data = {
            'property': {
                'lat': '47.6916',
                'long': '-122.341',
                'view': 0,
                'grade': 8,
                'floors': 3.0,
                'zipcode': '98103-1234',
                'bedrooms': 3,
                'sqft_lot': 1448,
                'yr_built': 2005,
                'bathrooms': 2.25,
                'condition': 3,
                'sqft_above': 1430,
                'sqft_lot15': 1383,
                'waterfront': 0,
                'sqft_living': 1430,
                'yr_renovated': 0,
                'sqft_basement': 0,
                'sqft_living15': 1430,
                'event_timestamp': '2026-06-27T22:02:03.61179',
                'economic_conditions': 1.0
            }
        }
        
        response = self.client.post('/predicted-home-value', content_type='application/json', data=json.dumps(data))
        assert response.status == '400 BAD REQUEST'
        assert len(response.json['error_message']) > 0
        assert response.json['error_message'] == '\'zipcode\' must be a numeric string of length 5'

    def test_bad_schema_payload(self):
        
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value.fetchone.side_effect = [{'population':137733}, {
            'high_schools': 1,
            'middle_schools': 1,
            'primary_schools': 6,
            'other_schools': 0,
            'unknown_schools': 0,
            'total_schools': 8
        }]
        self.app = prediction_service.create_app(conn, prediction_service.HomeEvent(), None, 'test_model')
        self.client = self.app.test_client()
        data = {
            'property': {
                'lat': '47.6916',
                'long': '-122.341',
                'view': 0,
                'grade': 8,
                'floors': 3.0,
                'zipcode': '98103',
                'bedrooms': 3,
                'sqft_lot': 1448,
                'yr_built': 2005,
                'bathrooms': 2.25,
                'condition': 3,
                'sqft_above': 1430,
                'sqft_lot15': 1383,
                'sqft_living': 1430,
                'yr_renovated': 0,
                'sqft_basement': 0,
                'sqft_living15': 1430,
                'event_timestamp': '2026-06-27T22:02:03.61179',
                'economic_conditions': 1.0
            }
        }
        
        response = self.client.post('/predicted-home-value', content_type='application/json', data=json.dumps(data))
        assert response.status == '400 BAD REQUEST'
        assert len(response.json['error_message']) > 0
        assert response.json['error_message']['waterfront'][0] == 'Missing data for required field.'
    
    def test_out_of_range_schema_payload(self):
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value.fetchone.side_effect = [{'population':137733}, {
            'high_schools': 1,
            'middle_schools': 1,
            'primary_schools': 6,
            'other_schools': 0,
            'unknown_schools': 0,
            'total_schools': 8
        }]
        self.app = prediction_service.create_app(conn, prediction_service.HomeEvent(), None, 'test_model')
        self.client = self.app.test_client()
        data = {
            'property': {
                'lat': '47.6916',
                'long': '-122.341',
                'view': 0,
                'grade': 8,
                'floors': 3.0,
                'zipcode': '98103',
                'bedrooms': 3,
                'sqft_lot': 1448,
                'yr_built': 2005,
                'bathrooms': 2.25,
                'condition': 3,
                'sqft_above': 1430,
                'sqft_lot15': 1383,
                'waterfront': 2,
                'sqft_living': 1430,
                'yr_renovated': 0,
                'sqft_basement': 0,
                'sqft_living15': 1430,
                'event_timestamp': '2026-06-27T22:02:03.61179',
                'economic_conditions': 1.0
            }
        }
        
        response = self.client.post('/predicted-home-value', content_type='application/json', data=json.dumps(data))
        assert response.status == '400 BAD REQUEST'
        assert len(response.json['error_message']) > 0
        assert response.json['error_message']['waterfront'][0] == 'Must be greater than or equal to 0 and less than or equal to 1.'

    def test_first_good_payload(self):
        with open('model.pkl', 'rb') as fl:
            model = pickle.load(fl)
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value.fetchone.side_effect = [{'population':137733}, {
            'high_schools': 1,
            'middle_schools': 1,
            'primary_schools': 6,
            'other_schools': 0,
            'unknown_schools': 0,
            'total_schools': 8
        }]
        self.app = prediction_service.create_app(conn, prediction_service.HomeEvent(), model, 'test_model')
        self.client = self.app.test_client()
        data = {
            'property': {
                'lat': 47.6916,
                'long': -122.341,
                'view': 0,
                'grade': 8,
                'floors': 3.0,
                'zipcode': '98103',
                'bedrooms': 3,
                'sqft_lot': 1448,
                'yr_built': 2005,
                'bathrooms': 2.25,
                'condition': 3,
                'sqft_above': 1430,
                'sqft_lot15': 1383,
                'waterfront': 0,
                'sqft_living': 1430,
                'yr_renovated': 0,
                'sqft_basement': 0,
                'sqft_living15': 1430, 
                'event_timestamp': '2026-06-27T22:02:03.611797',
                'economic_conditions': 1.0
            }
        }
        
        response = self.client.post('/predicted-home-value', content_type='application/json', data=json.dumps(data))
        assert response.status == '200 OK'
        assert response.json['predicted_price'] == 391931.5696294401

    def test_second_good_payload(self):
        with open('model.pkl', 'rb') as fl:
            model = pickle.load(fl)
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value.fetchone.side_effect = [{'population':66723}, {
            'high_schools': 1,
            'middle_schools': 1,
            'primary_schools': 4,
            'other_schools': 0,
            'unknown_schools': 0,
            'total_schools': 6
        }]
        self.app = prediction_service.create_app(conn, prediction_service.HomeEvent(), model, 'test_model')
        self.client = self.app.test_client()
        data = {
            'property': {
                'lat': 47.5827,
                'long': -122.387,
                'view': 0,
                'grade': 8,
                'floors': 2.0,
                'zipcode': '98116',
                'bedrooms': 3,
                'sqft_lot': 1904,
                'yr_built': 2003,
                'bathrooms': 2.5,
                'condition': 3,
                'sqft_above': 1140,
                'sqft_lot15': 1316,
                'waterfront': 0,
                'sqft_living': 1710,
                'yr_renovated': 0,
                'sqft_basement': 570,
                'sqft_living15': 1260,
                'event_timestamp': '2026-06-27T22:01:35.390825',
                'economic_conditions': 1.0
            }
        }
        
        response = self.client.post('/predicted-home-value', content_type='application/json', data=json.dumps(data))
        assert response.status == '200 OK'
        assert response.json['predicted_price'] == 569833.7649397093
        
    def test_third_good_payload(self):
        with open('model.pkl', 'rb') as fl:
            model = pickle.load(fl)
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value.fetchone.side_effect = [{'population':101202}, {
            'high_schools': 1,
            'middle_schools': 1,
            'primary_schools': 7,
            'other_schools': 0,
            'unknown_schools': 0,
            'total_schools': 9
        }]
        self.app = prediction_service.create_app(conn, prediction_service.HomeEvent(), model, 'test_model')
        self.client = self.app.test_client()
        data = {
            'property': {
                'lat': 47.4781,
                'long': -122.294,
                'view': 0,
                'grade': 6,
                'floors': 1.0,
                'zipcode': '98168',
                'bedrooms': 2,
                'sqft_lot': 34133,
                'yr_built': 1950,
                'bathrooms': 1.0,
                'condition': 3,
                'sqft_above': 750,
                'sqft_lot15': 25792,
                'waterfront': 0,
                'sqft_living': 750,
                'yr_renovated': 0,
                'sqft_basement': 0,
                'sqft_living15': 1460,
                'event_timestamp': '2026-06-27T21:54:03.849353',
                'economic_conditions': 1.0
            }
        }
        
        response = self.client.post('/predicted-home-value', content_type='application/json', data=json.dumps(data))
        assert response.status == '200 OK'
        assert response.json['predicted_price'] == 210874.3305808779

    def test_fourth_good_payload(self):
        with open('model.pkl', 'rb') as fl:
            model = pickle.load(fl)
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value.fetchone.side_effect = [{'population':137733}, {
            'high_schools': 0,
            'middle_schools': 2,
            'primary_schools': 4,
            'other_schools': 1,
            'unknown_schools': 0,
            'total_schools': 7
        }]
        self.app = prediction_service.create_app(conn, prediction_service.HomeEvent(), model, 'test_model')
        self.client = self.app.test_client()
        data = {
            'property': {
                'lat': 47.3484,
                'long': -122.033,
                'view': 0,
                'grade': 7,
                'floors': 2.0,
                'zipcode': '98038',
                'bedrooms': 3,
                'sqft_lot': 6000,
                'yr_built': 1992,
                'bathrooms': 2.25,
                'condition': 4,
                'sqft_above': 1370,
                'sqft_lot15': 6200,
                'waterfront': 0,
                'sqft_living': 1370,
                'yr_renovated': 0,
                'sqft_basement': 0,
                'sqft_living15': 1370,
                'event_timestamp': '2026-06-29T03:10:22.790142',
                'economic_conditions': 1.0
            }
        }
        
        response = self.client.post('/predicted-home-value', content_type='application/json', data=json.dumps(data))
        assert response.status == '200 OK'
        assert response.json['predicted_price'] == 288637.277921544
        
    def test_fifth_good_payload(self):
        with open('model.pkl', 'rb') as fl:
            model = pickle.load(fl)
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value.fetchone.side_effect = [{'population':175326}, {
            'high_schools': 3,
            'middle_schools': 3,
            'primary_schools': 8,
            'other_schools': 1,
            'unknown_schools': 0,
            'total_schools': 15
        }]
        self.app = prediction_service.create_app(conn, prediction_service.HomeEvent(), model, 'test_model')
        self.client = self.app.test_client()
        data = {
            'property': {
                'lat': 47.6711,
                'long': -122.148,
                'view': 0,
                'grade': 7,
                'floors': 1.0,
                'zipcode': '98052',
                'bedrooms': 3,
                'sqft_lot': 7700,
                'yr_built': 1968,
                'bathrooms': 1.75,
                'condition': 4,
                'sqft_above': 1270,
                'sqft_lot15': 7700,
                'waterfront': 0,
                'sqft_living': 1270,
                'yr_renovated': 0,
                'sqft_basement': 0,
                'sqft_living15': 1510,
                'event_timestamp': '2026-06-29T03:09:54.566853',
                'economic_conditions': 1.0
            }
        }
        
        response = self.client.post('/predicted-home-value', content_type='application/json', data=json.dumps(data))
        assert response.status == '200 OK'
        assert response.json['predicted_price'] == 453658.770438422

    def test_sixth_good_payload(self):
        with open('model.pkl', 'rb') as fl:
            model = pickle.load(fl)
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value.fetchone.side_effect = [{'population':59058}, {
            'high_schools': 0,
            'middle_schools': 0,
            'primary_schools': 2,
            'other_schools': 0,
            'unknown_schools': 0,
            'total_schools': 2
        }]
        self.app = prediction_service.create_app(conn, prediction_service.HomeEvent(), model, 'test_model')
        self.client = self.app.test_client()
        data = {
            'property': {
                'lat': 47.6433, 
                'long': -122.403,
                'view': 0,
                'grade': 11,
                'floors': 2.0,
                'zipcode': '98199',
                'bedrooms': 4,
                'sqft_lot': 8580,
                'yr_built': 2007,
                'bathrooms': 3.5,
                'condition': 3,
                'sqft_above': 2500,
                'sqft_lot15': 7920,
                'waterfront': 0,
                'sqft_living': 3470,
                'yr_renovated': 0,
                'sqft_basement': 970,
                'sqft_living15': 1940,
                'event_timestamp': '2026-06-29T03:09:26.342589',
                'economic_conditions': 1.0
            }
        }
        
        response = self.client.post('/predicted-home-value', content_type='application/json', data=json.dumps(data))
        assert response.status == '200 OK'
        assert response.json['predicted_price'] == 1435353.1752920016

    def test_seventh_good_payload(self):
        with open('model.pkl', 'rb') as fl:
            model = pickle.load(fl)
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value.fetchone.side_effect = [{'population':73233}, {
            'high_schools': 1,
            'middle_schools': 1,
            'primary_schools': 6,
            'other_schools': 0,
            'unknown_schools': 0,
            'total_schools': 8
        }]
        self.app = prediction_service.create_app(conn, prediction_service.HomeEvent(), model, 'test_model')
        self.client = self.app.test_client()
        data = {
            'property': {
                'lat': 47.5803,
                'long': -122.119,
                'view': 0,
                'grade': 7,
                'floors': 1.0,
                'zipcode': '98008',
                'bedrooms': 5,
                'sqft_lot': 9636,
                'yr_built': 1964,
                'bathrooms': 2.5,
                'condition': 4,
                'sqft_above': 1690,
                'sqft_lot15': 10385,
                'waterfront': 0,
                'sqft_living': 2910,
                'yr_renovated': 0,
                'sqft_basement': 1220,
                'sqft_living15': 2830,
                'event_timestamp': '2026-06-29T03:08:58.120685',
                'economic_conditions': 1.0
            }
        }
        
        response = self.client.post('/predicted-home-value', content_type='application/json', data=json.dumps(data))
        assert response.status == '200 OK'
        assert response.json['predicted_price'] == 540236.0073330712

    def test_eigth_good_payload(self):
        with open('model.pkl', 'rb') as fl:
            model = pickle.load(fl)
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value.fetchone.side_effect = [{'population':175326}, {
            'high_schools': 3,
            'middle_schools': 3,
            'primary_schools': 8,
            'other_schools': 1,
            'unknown_schools': 0,
            'total_schools': 15
        }]
        self.app = prediction_service.create_app(conn, prediction_service.HomeEvent(), model, 'test_model')
        self.client = self.app.test_client()
        data = {
            'property': {
                'lat': 47.6301,
                'long': -122.107,
                'view': 0,
                'grade': 8,
                'floors': 1.0,
                'zipcode': '98052',
                'bedrooms': 3,
                'sqft_lot': 12630,
                'yr_built': 1969,
                'bathrooms': 2.75,
                'condition': 4,
                'sqft_above': 1230,
                'sqft_lot15': 12196,
                'waterfront': 0,
                'sqft_living': 1950,
                'yr_renovated': 0,
                'sqft_basement': 720,
                'sqft_living15': 1990,
                'event_timestamp': '2026-06-29T03:08:29.897090',
                'economic_conditions': 1.0
            }
        }
        
        response = self.client.post('/predicted-home-value', content_type='application/json', data=json.dumps(data))
        assert response.status == '200 OK'
        assert response.json['predicted_price'] == 513294.71775248734

    def test_ninth_good_payload(self):
        with open('model.pkl', 'rb') as fl:
            model = pickle.load(fl)
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value.fetchone.side_effect = [{'population':137733}, {
            'high_schools': 1,
            'middle_schools': 1,
            'primary_schools': 3,
            'other_schools': 0,
            'unknown_schools': 0,
            'total_schools': 5
        }]
        self.app = prediction_service.create_app(conn, prediction_service.HomeEvent(), model, 'test_model')
        self.client = self.app.test_client()
        data = {
            'property': {
                'lat': 47.7439,
                'long': -122.228,
                'view': 0,
                'grade': 7,
                'floors': 1.0,
                'zipcode': '98028',
                'bedrooms': 3,
                'sqft_lot': 8209,
                'yr_built': 1942,
                'bathrooms': 1.0,
                'condition': 3,
                'sqft_above': 1830,
                'sqft_lot15': 12000,
                'waterfront': 0,
                'sqft_living': 1830,
                'yr_renovated': 0,
                'sqft_basement': 0,
                'sqft_living15': 2150,
                'event_timestamp': '2026-06-29T03:08:01.671506',
                'economic_conditions': 1.0
            }
        }
        
        response = self.client.post('/predicted-home-value', content_type='application/json', data=json.dumps(data))
        assert response.status == '200 OK'
        assert response.json['predicted_price'] == 297208.80295314355

    def test_tenth_good_payload(self):
        with open('model.pkl', 'rb') as fl:
            model = pickle.load(fl)
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value.fetchone.side_effect = [{'population':137733}, {
            'high_schools': 1,
            'middle_schools': 2,
            'primary_schools': 5,
            'other_schools': 0,
            'unknown_schools': 0,
            'total_schools': 8
        }]
        self.app = prediction_service.create_app(conn, prediction_service.HomeEvent(), model, 'test_model')
        self.client = self.app.test_client()
        data = {
            'property': {
                'lat': 47.645,
                'long': -122.084,
                'view': 4,
                'grade': 8,
                'floors': 3.0,
                'zipcode': '98074',
                'bedrooms': 3,
                'sqft_lot': 4102,
                'yr_built': 1996,
                'bathrooms': 2.5,
                'condition': 3,
                'sqft_above': 1730,
                'sqft_lot15': 16994,
                'waterfront': 1,
                'sqft_living': 1730,
                'yr_renovated': 0,
                'sqft_basement': 0,
                'sqft_living15': 2340,
                'event_timestamp': '2026-06-29T03:07:33.442193',
                'economic_conditions': 1.0
            }
        }
        
        response = self.client.post('/predicted-home-value', content_type='application/json', data=json.dumps(data))
        assert response.status == '200 OK'
        assert response.json['predicted_price'] == 968269.2476343603

if __name__ == '__main__':
    unittest.main()