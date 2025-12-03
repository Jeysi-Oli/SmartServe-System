from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone Number')
    address = StringField('Address')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Login as', choices=[('resident', 'Resident'), ('admin', 'Administrator')], validators=[DataRequired()])
    submit = SubmitField('Login')

class RequestForm(FlaskForm):
    document_type = SelectField('Document Type', choices=[
        ('birth_certificate', 'Birth Certificate'),
        ('marriage_certificate', 'Marriage Certificate'),
        ('death_certificate', 'Death Certificate'),
        ('residency_cert', 'Residency Certificate'),
        ('id_verification', 'ID Verification'),
        ('income_cert', 'Income Certificate'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    description = TextAreaField('Description/Details', validators=[Length(min=10, max=500)])
    submit = SubmitField('Submit Request')

class AdminNoteForm(FlaskForm):
    admin_notes = TextAreaField('Admin Notes', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')
    ], validators=[DataRequired()])
    submit = SubmitField('Update Request')