# Training Job

This job runs once per day to train a new RandomForestRegressor and store it in the database. It is versioned as `year.month.day` of the day of its training.

## Running Standalone

First, make sure the environment variables are set. Replace the password with your own.

```bash
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
python3 training-job.py
```

## Using Docker

### Building the Docker Image

```bash
docker build --no-cache -t training-job .
```

### Running the Docker Image

```bash
docker run --name training-job --network home-sale-event-system -d -e DB_USER="postgres" -e DB_PASS="change-me" -e DB_HOST="postgres" training-job
```

## Database Schemas

### Trained Model Schema

```sql
CREATE TABLE trained_models (
    id SERIAL NOT NULL,
    model_id TEXT NOT NULL,
    r2 DOUBLE PRECISION NOT NULL,
    mape DOUBLE PRECISION NOT NULL,
    rmse DOUBLE PRECISION NOT NULL,
    model BYTEA
);
```
