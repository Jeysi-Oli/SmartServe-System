from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy (This will be linked to the app in app.py)
db = SQLAlchemy()

# ==================== USER ENTITY ====================
class User(db.Model):
    """
    User Model: Represents residents and administrators in the system.
    Stores login credentials and personal profile information.
    """
    __tablename__ = 'user'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Authentication Fields
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Stores Hashed Password
    role = db.Column(db.String(20), default='resident')   # 'admin' or 'resident'

    # Personal Information
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship: One User can have Multiple Requests (One-to-Many)
    # cascade='all, delete-orphan' ensures requests are deleted if user is deleted
    requests = db.relationship('Request', backref='user', lazy=True, cascade='all, delete-orphan')
    
    # --- Password Security Methods ---
    def set_password(self, password):
        """Hashes the password before saving to DB."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifies the password against the stored hash."""
        return check_password_hash(self.password, password)
    
    # --- Helper Methods ---
    def is_admin(self):
        """Checks if the user has administrative privileges."""
        return self.role == 'admin'

# ==================== REQUEST ENTITY ====================
class Request(db.Model):
    """
    Request Model: Represents a document request transaction.
    Linked to a specific User via Foreign Key.
    """
    __tablename__ = 'request'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Key (Links to User Table)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Request Details
    document_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending') # Options: pending, approved, rejected, completed
    
    # Tracking Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Admin Feedback
    admin_notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Request {self.id} - {self.document_type}>'