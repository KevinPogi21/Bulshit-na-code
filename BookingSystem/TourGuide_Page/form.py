from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from BookingSystem.models import User  # Adjust the import according to your project structure

class UserTourGuideForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact_number = StringField('Contact Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters long.")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])
    submit = SubmitField('Create Account')
    
    def validate_email(self, email):
        # Check if the email is already used by a traveler
        traveler = User.query.filter_by(email=email.data).first()
        if traveler:
            raise ValidationError('That email is already in use. Please choose a different one.')
