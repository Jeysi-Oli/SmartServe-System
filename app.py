from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from functools import wraps
from datetime import datetime
import os
import sqlite3  # <--- ADDED THIS

# --- MODULAR IMPORTS ---
from models import db, User, Request
from forms import RegisterForm, LoginForm, RequestForm, AdminNoteForm

# ==================== APP CONFIGURATION ====================
app = Flask(__name__)

# Security and Database Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-key-for-dev') # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smartserve.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Extensions
db.init_app(app)
csrf = CSRFProtect(app) # Protects forms against CSRF attacks

# ==================== HELPER FUNCTIONS ====================
def get_db_connection():
    """Helper function to connect to the database for raw SQL queries."""
    conn = sqlite3.connect('instance/smartserve.db')
    conn.row_factory = sqlite3.Row
    return conn

# ==================== CUSTOM DECORATORS ====================
def login_required(f):
    """Decorator to ensure user is logged in before accessing a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to restrict access to Administrators only."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        
        # Verify if current user is actually an admin
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin():
            flash('Access denied. Admin only.', 'danger')
            return redirect(url_for('resident_dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== PUBLIC ROUTES (Landing Page) ====================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Logic for sending email could be added here
        return jsonify({'success': True, 'message': 'Message received'})
    return render_template('contact.html')

# ==================== AUTHENTICATION ROUTES ====================
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Create new user object
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            address=form.address.data,
            role='resident' # Default role
        )
        user.set_password(form.password.data) # Hash password
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if user exists
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            # Verify role match
            if user.role != form.role.data:
                flash('Invalid role selected.', 'danger')
                return redirect(url_for('login'))
            
            # Set Session Variables
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            # Redirect based on role
            target = 'admin_dashboard' if user.is_admin() else 'resident_dashboard'
            return redirect(url_for(target))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    session.clear() # Clear all session data
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

# ==================== RESIDENT MODULE ROUTES ====================
@app.route('/resident/dashboard')
@login_required
def resident_dashboard():
    user = User.query.get(session['user_id'])
    # Security check: Prevent admin from accessing resident view
    if user.is_admin(): return redirect(url_for('admin_dashboard'))
    
    # Fetch requests for this specific user only
    requests = Request.query.filter_by(user_id=user.id).order_by(Request.created_at.desc()).all()
    
    # Calculate stats
    stats = {
        'total': len(requests),
        'pending': len([r for r in requests if r.status == 'pending']),
        'completed': len([r for r in requests if r.status == 'completed']),
        'approved': len([r for r in requests if r.status == 'approved'])
    }
    return render_template('resident_dashboard.html', user=user, requests=requests, stats=stats)

@app.route('/resident/submit-request', methods=['GET', 'POST'])
@login_required
def submit_request():
    user = User.query.get(session['user_id'])
    form = RequestForm()
    
    if form.validate_on_submit():
        # Create new request linked to current user
        new_request = Request(
            user_id=user.id,
            document_type=form.document_type.data,
            description=form.description.data
        )
        db.session.add(new_request)
        db.session.commit()
        
        flash('Request submitted!', 'success')
        return redirect(url_for('resident_dashboard'))
    return render_template('submit_request.html', user=user, form=form)

@app.route('/resident/request/<int:request_id>')
@login_required
def view_request(request_id):
    req = Request.query.get_or_404(request_id)
    
    # Authorization Check: Ensure user owns this request
    if req.user_id != session['user_id']:
        flash('Permission denied.', 'danger')
        return redirect(url_for('resident_dashboard'))
        
    return render_template('view_request.html', request=req)

@app.route('/profile')
def profile():
    # 1. Security Check: Dapat naka-login
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 2. Get User from DB
    user_id = session['user_id']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    
    # 3. Show Page
    if user is None:
        return redirect(url_for('login'))
        
    return render_template('profile.html', user=user)

# ==================== ADMIN MODULE ROUTES ====================
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    # Fetch all data for oversight
    all_requests = Request.query.order_by(Request.created_at.desc()).all()
    all_users = User.query.filter_by(role='resident').all()
    
    stats = {
        'total_requests': len(all_requests),
        'pending': len([r for r in all_requests if r.status == 'pending']),
        'completed': len([r for r in all_requests if r.status == 'completed']),
        'total_residents': len(all_users)
    }
    return render_template('admin_dashboard.html', stats=stats, requests=all_requests, users=all_users)

@app.route('/admin/requests')
@admin_required
def admin_requests():
    all_requests = Request.query.order_by(Request.created_at.desc()).all()
    return render_template('admin_requests.html', requests=all_requests)

@app.route('/admin/request/<int:request_id>', methods=['GET', 'POST'])
@admin_required
def process_request(request_id):
    req = Request.query.get_or_404(request_id)
    form = AdminNoteForm()
    
    if form.validate_on_submit():
        # Update Request Status and Notes
        req.status = form.status.data
        req.admin_notes = form.admin_notes.data
        req.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Request updated.', 'success')
        return redirect(url_for('admin_requests'))
    return render_template('process_request.html', request=req, form=form)

@app.route('/admin/residents')
@admin_required
def admin_residents():
    residents = User.query.filter_by(role='resident').all()
    return render_template('admin_residents.html', residents=residents)

@app.route('/admin/resident/<int:resident_id>')
@admin_required
def view_resident(resident_id):
    resident = User.query.get_or_404(resident_id)
    # Fetch specific requests for this resident
    requests = Request.query.filter_by(user_id=resident_id).all()
    return render_template('view_resident.html', resident=resident, requests=requests)

# ==================== GLOBAL CONTEXT & STARTUP ====================
@app.context_processor
def inject_user():
    """Makes 'current_user' available in ALL HTML templates automatically."""
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return dict(current_user=user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Checks and creates tables if they don't exist
    app.run(debug=True)