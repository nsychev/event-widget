from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    name = StringField('Как вас зовут?', validators=[DataRequired()])
