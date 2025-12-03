from app import app, db
from models import User

def create_admin():
    """
    Creates a default Administrator account if one doesn't exist.
    Uses the main smartserve.db database.
    """
    with app.app_context():
        # Check kung may admin na para iwas duplicate
        admin = User.query.filter_by(role='admin').first()
        if admin:
            print(f"Admin account already exists: {admin.username}")
            return

        print("Creating default Admin account...")
        
        # Create the Admin User object
        new_admin = User(
            username='admin',
            email='admin@smartserve.com',
            first_name='System',
            last_name='Admin',
            role='admin',
            phone='09123456789',
            address='Barangay Hall'
        )
        
        # Set the password (hashing is handled by the model)
        new_admin.set_password('admin123') 

        # Save to database
        db.session.add(new_admin)
        db.session.commit()
        
        print("SUCCESS! Admin account created.")
        print("Email: admin@smartserve.com")
        print("Password: admin123")

if __name__ == '__main__':
    create_admin()