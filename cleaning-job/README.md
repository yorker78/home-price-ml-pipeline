# Cleaning and Enrichment Job

This job is run every 15 minutes to process 10000 records from the raw events table, clean them, and add data from the population and schools tables.

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
python3 cleaning-job.py
```

## Using Docker

### Building the Docker Image

```bash
docker build --no-cache -t cleaning-and-enrichment-job .
```

### Running the Docker Image

```bash
docker run --name cleaning-and-enrichment-job --network home-sale-event-system -d -e DB_USER="postgres" -e DB_PASS="change-me" -e DB_HOST="postgres" cleaning-and-enrichment-job:latest
```

## Database Schemas

### Cleaned Home Event Schema

```sql
CREATE TABLE home_sale_event (
    lat NUMERIC NOT NULL,
    long NUMERIC NOT NULL,
    zipcode INTEGER NOT NULL,
    sqft_lot INTEGER NOT NULL CHECK (sqft_lot > 0 AND sqft_lot <= 500000),
    sqft_living INTEGER NOT NULL CHECK (sqft_living > 0 AND sqft_living <= 8000),
    sqft_above INTEGER NOT NULL CHECK (sqft_above > 0),
    sqft_basement INTEGER, --Removed NOT NULL--
    has_basement BOOLEAN GENERATED ALWAYS AS (sqft_basement > 0), --New Column--
    sqft_lot15 INTEGER NOT NULL CHECK (sqft_lot15 > 0 AND sqft_lot15 <= 200000),
    sqft_living15 INTEGER NOT NULL CHECK (sqft_living15 > 0 AND sqft_living <= 5000),
    yr_built INTEGER NOT NULL CHECK (yr_built >= 1900), --Add Check for yr_built--
    yr_renovated INTEGER, --Removed NOT NULL--
    was_renovated BOOLEAN GENERATED ALWAYS AS (yr_renovated > 0), --New Column-- 
    condition INTEGER NOT NULL CHECK (condition > 1),
    grade INTEGER NOT NULL CHECK (grade > 1),
    floors FLOAT NOT NULL CHECK (floors >= 1),
    bedrooms INTEGER NOT NULL CHECK ((bedrooms > 0 AND bedrooms <= 6) OR (bedrooms == 0 AND bathrooms >= 0.75)), --Add Check for Studios--
    bathrooms FLOAT NOT NULL CHECK (bathrooms >= 0.75 AND bathrooms <= 6), --Increase Lower Limit--
    view INTEGER NOT NULL,
    waterfront INTEGER NOT NULL CHECK (waterfront == 0 OR waterfront ==1),
    price NUMERIC NOT NULL CHECK (price > 0 AND price <= 4000000), --Add Check--
    event_timestamp DATETIME NOT NULL,
    economic_conditions NUMERIC NOT NULL, --INTEGER -> NUMERIC--
    id INTEGER PRIMARY KEY REFERENCES raw_home_sale_events(id), --Add foreign key reference--
);
```
