from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import InputRequired

STATES = (
    ('Maharashtra', 'Maharashtra'),
)
CONNECTION_TYPES = (
    ('Residential', 'Residential'),
    ('Commercial', 'Commercial'),
    ('Industrial', 'Industrial'),
)
COMMERCIAL_TYPES = (
    ('default-c', 'Default'),
    ('LT2A', 'Commercial - LTIIA'),
    ('LT2B', 'Commercial - LTIIB'),
    ('LT2C', 'Commercial - LTIIC'),
)
INDUSTRIAL_TYPES = (
    ('default-i', 'Default'),
    ('LT3A', 'Industrial - LTIIIA'),
    ('LT3B', 'Industrial - LTIIIB'),
)


class UserInputForm(FlaskForm):
    state = SelectField(
        'State',
        choices=STATES,
        validators=[InputRequired()]
    )
    consumption = IntegerField(
        'Average monthly Consumption (KW/hr)',
        validators=[InputRequired()]
    )
    connection = SelectField(
        'Connection Type',
        choices=CONNECTION_TYPES,
        validators=[InputRequired()]
    )
    commercial_type = SelectField(
        'Commercial Type',
        choices=COMMERCIAL_TYPES,
    )
    industrial_type = SelectField(
        'Industrial Type',
        choices=INDUSTRIAL_TYPES,
    )
    connected_load = IntegerField(
        'Connected Load (optional)',
    )
    submit = SubmitField('Calculate')
