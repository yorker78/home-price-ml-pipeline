import datetime as dt
import os
from time import perf_counter

import dill as pickle
import pandas as pd
import psycopg
from psycopg.rows import dict_row
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    mean_absolute_percentage_error,
    r2_score,
    root_mean_squared_error,
)
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from transformers import CombinedTransformer


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

def debug(old_df, y=None):
    print('Made it!')
    print(type(old_df))
    return old_df

class PricePipeline:
    def __init__(self, df, n_splits=5, regressor=None, regressor_name='None', engineered_features=[]):
        self.df = df
        self.tss = TimeSeriesSplit(n_splits=n_splits)
        self.regressor = regressor
        self.regressor_name = regressor_name
        self.transformers = []
        self.transformers.append(('engineered', CombinedTransformer()))
        self.transformers.append(('impute', ColumnTransformer(remainder='passthrough', transformers=[('imputer', SimpleImputer(), ['zipcode', 'sqft_living', 'sqft_above'])])))
        self.transformers.append(('scale', StandardScaler()))
        self.transformers.append(('predict', regressor))
        self.pipeline = Pipeline(self.transformers)

    def train(self):
        for i, (train_idx, test_idx) in enumerate(self.tss.split(self.df)):
            train_df = self.df.iloc[train_idx]
            test_df = self.df.iloc[test_idx]
        train_y = train_df['price']
        test_y = test_df['price']
        train_X = train_df.drop(labels='price', axis=1)
        test_X = test_df.drop(labels='price', axis=1)
        
        start = perf_counter()
        self.pipeline.fit(train_X, train_y)
        y_pred = self.pipeline.predict(test_X)
        end = perf_counter()
        
        self.r2_score = r2_score(test_y, y_pred)
        self.mape = mean_absolute_percentage_error(test_y, y_pred)
        self.rmse = root_mean_squared_error(test_y, y_pred)
        self.time = end - start

    def fit(self):
        y = self.df['price']
        X = self.df.drop(labels='price', axis=1)
        self.pipeline.fit(X, y)

    def get_pipeline(self):
        return self.pipeline

    def get_stats(self):
        return (self.r2_score, self.mape, self.rmse, self.time)


def run_job():
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')
    host = os.getenv('DB_HOST')
    conn_string = f'postgresql://{user}:{password}@{host}:5432/house_price_prediction_service'
    print('Job Starting...')
    with psycopg.connect(conn_string, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM cleaned_home_sale_events;')
            rows = cur.fetchall()
            df = pd.DataFrame.from_records(rows)
            df = df.drop(labels=['id', 'event_timestamp'], axis=1)
            df = df.astype({'economic_conditions': 'float64', 'price': 'float64', 'lat': 'float64', 'long': 'float64'})
            cmb = PricePipeline(df=df, n_splits=3, regressor=RandomForestRegressor(random_state=42, max_depth=25, n_estimators=100, min_samples_split=5, min_samples_leaf=5), regressor_name='Combined Engineered Features Random Forest Regression', engineered_features=['polar', 'relative', 'reno', 'pop', 'ohe'])
            cmb.train()
            cmb_r2, cmb_mape, cmb_rmse, cmb_time = cmb.get_stats()
            cmb.fit()
            model = '\'\\x' + pickle.dumps(cmb.get_pipeline(), byref=True).hex() + '\''
            date = dt.datetime.now()
            version = f'\'{date.year}.{date.month}.{date.day}\''
            cur.execute(f'''INSERT INTO trained_models
                        (model_id, r2, mape, rmse, time, model)
                        VALUES
                        ({version}, {cmb_r2}, {cmb_mape}, {cmb_rmse}, {cmb_time}, {model});
                        ''')
            conn.commit()
    print('Job Finished')

if __name__ == "__main__":
    if check_environment() == 0:
        run_job()
    print('Environment Variables are not set.')