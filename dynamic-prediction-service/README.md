# Prediction Service

This service provides the endpoint `/predicted-home-value` to predict the value of a home described in the request's JSON payload using the most recently trained model.

## Running Standalone

First, make sure the environment variables are set. Replace the password with your own.

```bash
export SERVICE_HOST="0.0.0.0"
export SERVICE_PORT="8889"
export POSTGRES_USERNAME="postgres"
export POSTGRES_PASSWORD="change-me"
export POSTGRES_HOST="postgres"
```

Next, if there is not a virtual environment created, make one.

```bash
python -m venv ../.venv
source ../.venv/bin/activate
pip install -r ../requirements.txt
```

Lastly, run the script

```bash
python3 prediction-service.py
```

## Using Docker

### Building the Docker Image

```bash
docker build --no-cache -t dynamic-prediction-service .
```

### Running the Docker Image

```bash
docker run --name dynamic-prediction-service --network home-sale-event-system -d -e SERVICE_HOST="0.0.0.0" -e SERVICE_PORT="8889" -e POSTGRES_USERNAME="postgres" -e POSTGRES_PASSWORD="change-me" -e POSTGRES_HOST="postgres" dynamic-prediction-service:latest
```

## JSON Schema

```json
{
    "property": {
        "lat": 0.0, // Float, Required
        "long": 0.0, // Float, Required
        "zipcode": "12345", // 5 Character Numeric String, Required
        "sqft_lot": 0, // Integer between [1:500000], Required
        "sqft_living": 0, // Integer between [1:8000], Required
        "sqft_basement": 0, // Integer
        "sqft_lot15": 0, // Integer between [1:200000], Required
        "sqft_living15": 0, // Integer between [1:5000], Required
        "yr_built": 0, // Integer, Required
        "yr_renovated": 0, // Integer
        "condition": 0, // Integer between [2:13], Required
        "grade": 0, // Integer between [2:13], Required
        "floors": 0.0, // Float between [1:4], Required
        "bedrooms": 0, // Integer between [0:6], Required
        "bathrooms": 0.0, // Float between [0.75:6], Required
        "view": 0, // Integer between [0:4], Required
        "waterfront": 0, // Integer between [0:1]
        "event_timestampt": "1970-01-01T00:00:00.0", // DateTime String, Required
        "economic_conditions": 0.0 // Float, Required
    }
}
```

## Database Schema

### Predicted Price Schema

```sql
CREATE TABLE predicted_prices (
    id SERIAL PRIMARY KEY,
    model_id TEXT NOT NULL,
    request_timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    predicted_price REAL NOT NULL
)
```
