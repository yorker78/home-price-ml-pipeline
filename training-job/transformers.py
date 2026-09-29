from sklearn.base import BaseEstimator, TransformerMixin


class PolarTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        # Coords from https://www.seattletimes.com/pacific-nw-magazine/the-center-of-seattle/
        from numpy import atan2, sqrt
        center_lat = 47.62101388888889
        center_long = -122.33328888888889
        df = X.copy()
        df['lat'] = df['lat'] - center_lat
        df['long'] = df['long'] - center_long
        df['radius'] = sqrt((df['lat'] ** 2) + (df['long'] ** 2))
        df['theta'] = atan2(df['long'], df['lat'])
        df = df.drop(labels=['lat', 'long'], axis=1)
        return X

class RelativeNNTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        df = X.copy()
        df['relative_lot'] = df['sqft_lot'] - df['sqft_lot15']
        df['relative_living'] = df['sqft_living'] - df['sqft_living15']
        df = df.drop(labels=['sqft_lot15', 'sqft_living15'], axis=1)
        return df

class BuildRenoTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        from datetime import datetime
        df = X.copy()
        df['yrs_since_last_construction'] = datetime.now().year - df[['yr_built', 'yr_renovated']].values.max(1)
        # df = df.drop(labels='yr_renovated', axis=1)
        df['yr_renovated'] = df[['yr_built', 'yr_renovated']].values.max(1)
        return df

class OneHotEncodeTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        from pandas import CategoricalDtype, get_dummies
        df = X.copy()
        if 'has_basement' not in df.columns:
            df['has_basement'] = df['sqft_basement'] > 0
        if 'was_renovated' not in df.columns:
            df['was_renovated'] = df['yr_built'] < df['yr_renovated']
        cols_to_encode = {
            'condition': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            'grade': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            'floors': [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0],
            'bedrooms': [0, 1, 2, 3, 4, 5, 6],
            'bathrooms': [0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0, 5.25, 5.5, 5.75, 6.0],
            'view': [0, 1, 2, 3, 4]}
        
        for col in cols_to_encode.keys():
            df = df.drop(labels=col, axis=1).join(get_dummies(df[col].astype(CategoricalDtype(categories=cols_to_encode[col])), prefix=col))
        return df

class PopSchoolRatioTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        df = X.copy()
        df['pop_school_ratio'] = df['zipcode_population'] / df['zipcode_public_total_schools']
        df = df.drop(labels=['zipcode_population', 'zipcode_public_total_schools'], axis=1)
        return df
    
class CombinedTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        from datetime import datetime

        from numpy import atan2, sqrt
        from pandas import CategoricalDtype, get_dummies

        center_lat = 47.62101388888889
        center_long = -122.33328888888889
        df = X.copy()
        df['lat'] = df['lat'] - center_lat
        df['long'] = df['long'] - center_long
        df['radius'] = sqrt((df['lat'] ** 2) + (df['long'] ** 2))
        df['theta'] = atan2(df['long'], df['lat'])
        
        df['relative_lot'] = df['sqft_lot'] - df['sqft_lot15']
        df['relative_living'] = df['sqft_living'] - df['sqft_living15']
        
        df['yrs_since_last_construction'] = datetime.now().year - df[['yr_built', 'yr_renovated']].values.max(1)
        df['yr_renovated'] = df[['yr_built', 'yr_renovated']].values.max(1)
        
        if 'has_basement' not in df.columns:
            df['has_basement'] = df['sqft_basement'] > 0
        if 'was_renovated' not in df.columns:
            df['was_renovated'] = df['yr_built'] < df['yr_renovated']
        cols_to_encode = {
            'condition': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            'grade': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            'floors': [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0],
            'bedrooms': [0, 1, 2, 3, 4, 5, 6],
            'bathrooms': [0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0, 5.25, 5.5, 5.75, 6.0],
            'view': [0, 1, 2, 3, 4]}
        for col in cols_to_encode.keys():
            df = df.drop(labels=col, axis=1).join(get_dummies(df[col].astype(CategoricalDtype(categories=cols_to_encode[col])), prefix=col))
            
        df['pop_school_ratio'] = df['zipcode_population'] / df['zipcode_public_total_schools']

        df = df.drop(labels=['lat', 'long', 'sqft_lot15', 'sqft_living15', 'zipcode_population', 'zipcode_public_total_schools'], axis=1)
        return df