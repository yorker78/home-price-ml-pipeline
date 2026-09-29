# Evaluation Job

This job runs every 15 minutes to evaluate 1000 Home Sale Events through the [prediction service](../prediction-service/README.md). It can point to either the static or dynamic one depending on the host and port configured when running the script / file.

## Running Standalone

First, make sure the environment variables are set. Replace the password with your own.

```bash
export PR_HOST="prediction-service"
export PR_PORT="8888"
export DB_USER="postgres"
export DB_PASS="change-me"
export DB_HOST="postgres"
```

Next, if there is not a virtual environment created, make one.

```bash
python -m venv ../.venv
source ../.venv/bin/activate
pip install -r ../requirements.txt
```

Lastly, run the script

```bash
python3 evaluation-job.py
```

## Using Docker

### Building the Docker Image

```bash
docker build --no-cache -t evaluation-job .
```

### Running the Docker Image

```bash
docker run --name evaluation-job --network home-sale-event-system -d -e PR_HOST="prediction-service" -e PR_PORT="8888" -e DB_USER="postgres" -e DB_PASS="change-me" -e DB_HOST="postgres" evaluation-job
```

## Database Schemas

### Evaluated Home Sale Events

```sql
CREATE TABLE evaluated_home_sale_events (
    id INTEGER PRIMARY KEY,
    sale_date TIMESTAMP WITHOUT TIME ZONE,
    true_price NUMERIC,
    predicted_price NUMERIC
);
```

### Evaluated Event Ids

```sql
CREATE TABLE evaluated_event_ids (
    id INTEGER PRIMARY KEY
)
```
