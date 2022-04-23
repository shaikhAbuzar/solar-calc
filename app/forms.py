from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import InputRequired

STATES = (
    ('Select State', 'Select State'),
    ('Maharashtra', 'Maharashtra'),
    ('MadhyaPradesh', 'Madhya Pradesh'),
    ('Gujrat', 'Gujarat'),
)
CONNECTION_TYPES = (
    ('Residential', 'Residential'),
    ('Commercial', 'Commercial'),
    ('Industrial', 'Industrial'),
)
CONNECTION_TYPES_GUJRAT = (
    ('Residential General Purpose', 'Residential General Purpose'),
    ('Non Residential General Purpose', 'Non Residential General Purpose'),
)
COMMERCIAL_TYPES_MH = (
    ('default-c', 'Default'),
    ('LT2A', 'Commercial - LTIIA'),
    ('LT2B', 'Commercial - LTIIB'),
    ('LT2C', 'Commercial - LTIIC'),
)
INDUSTRIAL_TYPES_MH = (
    ('default-i', 'Default'),
    ('LT3A', 'Industrial - LTIIIA'),
    ('LT3B', 'Industrial - LTIIIB'),
)
COMMERCIAL_TYPES_MP = (
    ('default-c', 'Default'),
    ('small', 'Small'),
    ('medium', 'Medium'),
    ('large', 'Large'),
)
INDUSTRIAL_TYPES_MP = (
    ('default-i', 'Default'),
    ('small', 'Small'),
    ('medium', 'Medium'),
    ('heavy', 'Heavy'),
)


class UserInputForm(FlaskForm):
    state = SelectField(
        'State',
        choices=STATES,
        validators=[InputRequired()]
    )
    consumption = IntegerField(
        'Average monthly Consumption (KWhr)',
        validators=[InputRequired()]
    )
    connection = SelectField(
        'Connection Type',
        choices=CONNECTION_TYPES,
        validators=[InputRequired()]
    )
    connection_gujrat = SelectField(
        'Connection Type',
        choices=CONNECTION_TYPES_GUJRAT,
        validators=[InputRequired()]
    )
    commercial_type_mh = SelectField(
        'Commercial Type',
        choices=COMMERCIAL_TYPES_MH,
    )
    industrial_type_mh = SelectField(
        'Industrial Type',
        choices=INDUSTRIAL_TYPES_MH,
    )
    commercial_type_mp = SelectField(
        'Commercial Type',
        choices=COMMERCIAL_TYPES_MP,
    )
    industrial_type_mp = SelectField(
        'Industrial Type',
        choices=INDUSTRIAL_TYPES_MP,
    )
    connected_load = IntegerField(
        'Connected Load',
    )
    submit = SubmitField('Calculate')
