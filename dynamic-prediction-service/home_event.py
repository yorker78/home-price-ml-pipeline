from datetime import datetime

from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validate,
    validates,
    validates_schema,
)


class HomeEvent(Schema):
    lat = fields.Float(required=True)
    long = fields.Float(required=True)
    zipcode = fields.Integer(required=True)
    sqft_lot = fields.Integer(required=True, validate=validate.Range(min=1, max=500000))
    sqft_living = fields.Integer(required=True, validate=validate.Range(min=1, max=8000))
    sqft_above = fields.Integer(required=True)
    sqft_basement = fields.Integer()
    sqft_lot15 = fields.Integer(required=True, validate=validate.Range(min=1, max=200000))
    sqft_living15 = fields.Integer(required=True, validate=validate.Range(min=1, max=5000))
    yr_built = fields.Integer(required=True)
    yr_renovated = fields.Integer()
    condition = fields.Integer(required=True, validate=validate.Range(min=2, max=13))
    grade = fields.Integer(required=True, validate=validate.Range(min=2, max=13))
    floors = fields.Float(required=True, validate=validate.Range(min=1, max=4))
    bedrooms = fields.Integer(required=True, validate=validate.Range(min=0, max=6))
    bathrooms = fields.Float(required=True, validate=validate.Range(min=0.75, max=6))
    view = fields.Integer(required=True, validate=validate.Range(min=0, max=4))
    waterfront = fields.Integer(required=True, validate=validate.Range(min=0, max=1))
    price = fields.Decimal(required=False, validate=validate.Range(min=1, max=4000000))
    event_timestamp = fields.DateTime(required=True)
    economic_conditions = fields.Float(required=True)
    id = fields.Integer(required=False)
    zipcode_population = fields.Integer(required=True, validate=validate.Range(min=0, max=450000))
    zipcode_public_high_schools = fields.Integer(required=True, validate=validate.Range(min=0, max=25))
    zipcode_public_middle_schools = fields.Integer(required=True, validate=validate.Range(min=0, max=25))
    zipcode_public_primary_schools = fields.Integer(required=True, validate=validate.Range(min=0, max=50))
    zipcode_public_other_schools = fields.Integer(required=True, validate=validate.Range(min=0, max=25))
    zipcode_public_unknown_schools = fields.Integer(required=True, validate=validate.Range(min=0, max=25))
    zipcode_public_total_schools = fields.Integer(required=True, validate=validate.Range(min=0, max=75))

    @validates('yr_built')
    def validate_yr_built(self, value, data_key):
        if value < 1900 or value > datetime.now().year:
            raise ValidationError('Year Built is Out of Bounds')

    @validates_schema
    def validate_bedrooms(self, data, **kwargs):
        if data['bedrooms'] < 0 or data['bedrooms'] > 6 or (data['bedrooms'] == 0 and data['bathrooms'] < 0.75):
            raise ValidationError('Condition is Out of Bounds')
