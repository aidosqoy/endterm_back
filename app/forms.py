from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User
from flask_wtf.file import FileAllowed

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class StudentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=100)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=100)])
    course = StringField('Course', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=100)])
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Save')

    def validate_email(self, email):
        student = User.query.filter_by(email=email.data).first()
        if student:
            raise ValidationError('Email already exists for another student.')

class EditUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=100)])
    is_admin = BooleanField('Is Admin')
    submit = SubmitField('Save')
