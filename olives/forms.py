from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, SelectField, validators
from olives import models

acids = [(x, x) for x in models.get_acids()]


class AcidSelForm(Form):
    acid1 = SelectField("Acid 1:", choices=acids)
    acid2 = SelectField("Acid 2:", choices=acids)
