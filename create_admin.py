from app import app, db
from models import User

def create_admin():
    """
    Utility Script: Creates a default Administrator account.
    Run this once to set up the system.
    """
    with app.app_context():
        # Check for existing admin to prevent duplicates
        admin = User.query.filter_by(role='admin').first()
        if admin:
            print(f"Admin account already exists: {admin.username}")
            return

        print("Creating default Admin account...")
        
        # Create Admin Object
        new_admin = User(
            username='admin',
            email='admin@smartserve.com',
            first_name='System',
            last_name='Admin',
            role='admin',
            phone='09123456789',
            address='Barangay Hall'
        )
        
        # Hash the password
        new_admin.set_password('admin123') 

        # Commit to Database
        db.session.add(new_admin)
        db.session.commit()
        
        print("SUCCESS! Admin account created.")
        print("Email: admin@smartserve.com")
        print("Password: admin123")

if __name__ == '__main__':
    create_admin()