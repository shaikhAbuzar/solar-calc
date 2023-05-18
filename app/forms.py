from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField, FloatField
from wtforms.validators import InputRequired
from countryinfo import CountryInfo

STATES = (
    ('Select State', 'Select State'),
    *((state, state) for state in CountryInfo('India').provinces())
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
    tariff = FloatField(
        'Tariff'
    )
    submit = SubmitField('Calculate')
