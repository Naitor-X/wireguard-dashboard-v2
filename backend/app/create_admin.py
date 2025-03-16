from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def create_admin_user(db: Session):
    admin_user = User(
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),
        is_active=True,
        is_superuser=True,
        subnet_access="*"
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    return admin_user

if __name__ == "__main__":
    db = SessionLocal()
    try:
        admin = create_admin_user(db)
        print(f"Admin user created successfully: {admin.email}")
    except Exception as e:
        print(f"Error creating admin user: {e}")
    finally:
        db.close() 