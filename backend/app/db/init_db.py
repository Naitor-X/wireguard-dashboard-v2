from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.models.user import User

def init_db(db: Session) -> None:
    # Erstelle einen Admin-Benutzer
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_superuser=True,
            is_active=True,
            subnet_access="10.10.10.0/24"
        )
        db.add(admin)
        db.commit()
        db.refresh(admin) 