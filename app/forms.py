from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User, Student
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
    patronymic = StringField('Patronymic', validators=[Length(max=100)])
    course = StringField('Course', validators=[DataRequired(), Length(min=1, max=20)])
    profession = StringField('Profession', validators=[Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=100)])
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    created_at = DateField('Дата поступления', format='%Y-%m-%d')
    submit = SubmitField('Save')

    def __init__(self, original_email=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and self.original_email != email.data:
            raise ValidationError('Email already exists for a user.')

        student = Student.query.filter_by(email=email.data).first()
        if student and self.original_email != email.data:
            raise ValidationError('Email already exists for another student')


class EditUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=100)])
    is_admin = BooleanField('Is Admin')
    submit = SubmitField('Save')

    def __init__(self, original_email=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if self.original_email != email.data:
            user = User.query.filter_by(email=email.data).first()
            student = Student.query.filter_by(email=email.data).first()
            if user or student:
                raise ValidationError('Email already exists for another user or student')
