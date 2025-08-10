from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class UpdateProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(min=4)])
    phone_number = StringField('Phone Number')
    city = StringField('City')
    state = StringField('State')
    tags = StringField('Tags')
    interests = StringField('Interests')
    seo = StringField('SEO Programs')
    submit = SubmitField('Update Profile')
