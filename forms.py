from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User

# ==================== AUTHENTICATION FORMS ====================
class RegisterForm(FlaskForm):
    """Form for new user registration."""
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone Number')
    address = StringField('Address')
    
    # Password Validation
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    
    submit = SubmitField('Register')
    
    # --- Custom Validators ---
    def validate_username(self, username):
        """Check if username already exists in DB."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists.')
    
    def validate_email(self, email):
        """Check if email already exists in DB."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    """Form for user login with role selection."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Login as', choices=[('resident', 'Resident'), ('admin', 'Administrator')], validators=[DataRequired()])
    submit = SubmitField('Login')

# ==================== TRANSACTION FORMS ====================
class RequestForm(FlaskForm):
    """Form for residents to submit document requests."""
    document_type = SelectField('Document Type', choices=[
        ('clearance_cert', 'Barangay Clearance Certificate'),
        ('residency_cert', 'Barangay Residency Certificate'),
        ('indigency_cert', 'Barangay Indigency Certificate'),
        ('good_moral_cert', 'Barangay Good Moral Character Certificate'),
        ('id_verification', 'ID Verification'),
        ('first_job_cert', 'First-time Job Seeker Certificate'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    
    description = TextAreaField('Description/Details', validators=[Length(min=10, max=500)])
    submit = SubmitField('Submit Request')

class AdminNoteForm(FlaskForm):
    """Form for admins to update request status and add notes."""
    admin_notes = TextAreaField('Admin Notes', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')
    ], validators=[DataRequired()])
    submit = SubmitField('Update Request')