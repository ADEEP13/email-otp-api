from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models import Base, User, OTPVerification, engine, SessionLocal
from typing import Optional, Tuple


def init_db():
    """
    Initialize database: create all tables if they don't exist.
    This is called on application startup.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Get database session dependency for FastAPI.
    Yields a SQLAlchemy session that will be automatically closed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_or_create(db: Session, email: str) -> User:
    """
    Get existing user by email or create a new one.
    Returns the User object.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, is_verified=False)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def store_otp(db: Session, email: str, otp_code: str, expiry_minutes: int = 10) -> OTPVerification:
    """
    Store OTP in database. If an active OTP exists for this email, replace it.
    Only one active OTP per email is allowed.
    
    Args:
        db: Database session
        email: Email address
        otp_code: 6-digit OTP code
        expiry_minutes: Minutes until OTP expires (default: 10)
    
    Returns:
        The created OTPVerification record
    """
    # Delete any existing unverified OTPs for this email
    db.query(OTPVerification).filter(
        OTPVerification.email == email,
        OTPVerification.verified == False
    ).delete()
    
    expires_at = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    
    otp_record = OTPVerification(
        email=email,
        otp=otp_code,
        expires_at=expires_at,
        verified=False
    )
    db.add(otp_record)
    db.commit()
    db.refresh(otp_record)
    return otp_record


def verify_otp(db: Session, email: str, otp_code: str) -> Tuple[bool, str]:
    """
    Verify OTP for a given email.
    
    Checks:
    1. OTP exists and is not already verified
    2. OTP has not expired
    3. OTP matches the provided code
    
    On success:
    - Marks OTP as verified (one-time use)
    - Marks user as verified
    
    Args:
        db: Database session
        email: Email address
        otp_code: OTP code to verify
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    # Get the most recent unverified OTP for this email
    otp_record = db.query(OTPVerification).filter(
        OTPVerification.email == email,
        OTPVerification.verified == False
    ).order_by(OTPVerification.created_at.desc()).first()
    
    # Check if OTP record exists
    if not otp_record:
        return False, "No active OTP found for this email. Please request a new OTP."
    
    # Check if OTP has expired
    if datetime.utcnow() > otp_record.expires_at:
        otp_record.verified = False  # Mark as expired indirectly
        db.commit()
        return False, "OTP has expired. Please request a new OTP."
    
    # Check if OTP matches
    if otp_record.otp != otp_code:
        return False, "Invalid OTP. Please check and try again."
    
    # OTP is valid - mark as verified (one-time use)
    otp_record.verified = True
    
    # Update user as verified
    user = get_user_or_create(db, email)
    user.is_verified = True
    
    db.commit()
    return True, "Email verified successfully!"


def is_user_verified(db: Session, email: str) -> bool:
    """
    Check if a user's email is verified.
    
    Args:
        db: Database session
        email: Email address
    
    Returns:
        True if user is verified, False otherwise
    """
    user = db.query(User).filter(User.email == email).first()
    return user.is_verified if user else False
