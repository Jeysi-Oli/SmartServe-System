from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy (We connect this in app.py later)
db = SQLAlchemy()

class User(db.Model):
    """User Model for Residents and Admins"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='resident')
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship: One User has Many Requests
    requests = db.relationship('Request', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def is_admin(self):
        return self.role == 'admin'

class Request(db.Model):
    """Request Model for Document Transactions"""
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    document_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    admin_notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Request {self.id} - {self.document_type}>'