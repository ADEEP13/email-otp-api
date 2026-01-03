from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./otp_service.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ============== Database Models ==============

class User(Base):
    """User model for tracking verified email addresses"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class OTPVerification(Base):
    """OTP Verification model for tracking OTP requests and verifications"""
    __tablename__ = "otp_verifications"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    otp = Column(String, nullable=False)  # 6-digit OTP
    expires_at = Column(DateTime, nullable=False)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# ============== Pydantic Request/Response Models ==============

class SendOTPRequest(BaseModel):
    """Request model for sending OTP"""
    email: EmailStr


class VerifyOTPRequest(BaseModel):
    """Request model for verifying OTP"""
    email: EmailStr
    otp: str


class OTPResponse(BaseModel):
    """Response model for OTP operations"""
    success: bool
    message: str
    email: Optional[str] = None

    class Config:
        from_attributes = True


class VerificationStatusResponse(BaseModel):
    """Response model for verification status"""
    email: str
    is_verified: bool
    message: str

    class Config:
        from_attributes = True
