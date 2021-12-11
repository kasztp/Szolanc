from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField
from wtforms.validators import DataRequired


class ConfigForm(FlaskForm):
    language = RadioField('Language',
                          choices=[('EN', 'English'), ('HU', 'Hungarian')],
                          validators=[DataRequired()])
    own_letterset = StringField('Letters:', validators=[DataRequired()])
    submit = SubmitField('Send')
