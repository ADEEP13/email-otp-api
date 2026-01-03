"""
Test suite for Email OTP Verification Service

Run tests with: pytest tests/test_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from main import app, get_db, verify_api_key
from models import Base, User, OTPVerification, SessionLocal
from database import store_otp, verify_otp as verify_otp_db, get_user_or_create

# Create in-memory SQLite database for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_verify_api_key(x_api_key: str = None):
    """Override API key verification for testing"""
    return x_api_key or "test-key"


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[verify_api_key] = override_verify_api_key

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints"""

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "service" in response.json()


class TestSendOTP:
    """Test send OTP endpoint"""

    def test_send_otp_success(self):
        """Test successful OTP sending"""
        response = client.post(
            "/send-otp",
            headers={"X-API-KEY": "test-key"},
            json={"email": "test@example.com"},
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "test@example.com" in response.json()["email"]

    def test_send_otp_invalid_email(self):
        """Test OTP sending with invalid email"""
        response = client.post(
            "/send-otp",
            headers={"X-API-KEY": "test-key"},
            json={"email": "invalid-email"},
        )
        assert response.status_code == 422  # Validation error

    def test_send_otp_missing_api_key(self):
        """Test OTP sending without API key"""
        response = client.post(
            "/send-otp",
            json={"email": "test@example.com"},
        )
        assert response.status_code == 401

    def test_send_otp_replaces_existing(self):
        """Test that new OTP replaces existing one for same email"""
        db = TestingSessionLocal()
        
        # Send first OTP
        response1 = client.post(
            "/send-otp",
            headers={"X-API-KEY": "test-key"},
            json={"email": "duplicate@example.com"},
        )
        assert response1.status_code == 200
        
        # Get first OTP
        first_otp = db.query(OTPVerification).filter(
            OTPVerification.email == "duplicate@example.com"
        ).first()
        first_otp_code = first_otp.otp
        
        # Send second OTP
        response2 = client.post(
            "/send-otp",
            headers={"X-API-KEY": "test-key"},
            json={"email": "duplicate@example.com"},
        )
        assert response2.status_code == 200
        
        # Verify only one unverified OTP exists
        otps = db.query(OTPVerification).filter(
            OTPVerification.email == "duplicate@example.com",
            OTPVerification.verified == False
        ).all()
        assert len(otps) == 1
        
        # Verify OTP code changed
        assert otps[0].otp != first_otp_code
        
        db.close()


class TestVerifyOTP:
    """Test verify OTP endpoint"""

    def test_verify_otp_success(self):
        """Test successful OTP verification"""
        db = TestingSessionLocal()
        
        email = "verify@example.com"
        otp_code = "123456"
        
        # Create user and store OTP
        get_user_or_create(db, email)
        store_otp(db, email, otp_code)
        
        # Verify OTP
        response = client.post(
            "/verify-otp",
            headers={"X-API-KEY": "test-key"},
            json={"email": email, "otp": otp_code},
        )
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        
        # Check user is now verified
        user = db.query(User).filter(User.email == email).first()
        assert user.is_verified is True
        
        db.close()

    def test_verify_otp_invalid_code(self):
        """Test OTP verification with invalid code"""
        db = TestingSessionLocal()
        
        email = "invalid@example.com"
        otp_code = "123456"
        
        # Create user and store OTP
        get_user_or_create(db, email)
        store_otp(db, email, otp_code)
        db.close()
        
        # Try to verify with wrong OTP
        response = client.post(
            "/verify-otp",
            headers={"X-API-KEY": "test-key"},
            json={"email": email, "otp": "654321"},
        )
        
        assert response.status_code == 400
        assert "Invalid OTP" in response.json()["detail"]

    def test_verify_otp_expired(self):
        """Test OTP verification with expired OTP"""
        db = TestingSessionLocal()
        
        email = "expired@example.com"
        otp_code = "123456"
        
        # Create user and store expired OTP
        get_user_or_create(db, email)
        otp_record = OTPVerification(
            email=email,
            otp=otp_code,
            expires_at=datetime.utcnow() - timedelta(minutes=1),
            verified=False
        )
        db.add(otp_record)
        db.commit()
        db.close()
        
        # Try to verify expired OTP
        response = client.post(
            "/verify-otp",
            headers={"X-API-KEY": "test-key"},
            json={"email": email, "otp": otp_code},
        )
        
        assert response.status_code == 400
        assert "expired" in response.json()["detail"].lower()

    def test_verify_otp_one_time_use(self):
        """Test that OTP is one-time use"""
        db = TestingSessionLocal()
        
        email = "onetime@example.com"
        otp_code = "123456"
        
        # Create user and store OTP
        get_user_or_create(db, email)
        store_otp(db, email, otp_code)
        db.close()
        
        # First verification
        response1 = client.post(
            "/verify-otp",
            headers={"X-API-KEY": "test-key"},
            json={"email": email, "otp": otp_code},
        )
        assert response1.status_code == 200
        
        # Try to use same OTP again
        response2 = client.post(
            "/verify-otp",
            headers={"X-API-KEY": "test-key"},
            json={"email": email, "otp": otp_code},
        )
        assert response2.status_code == 400
        assert "No active OTP" in response2.json()["detail"]

    def test_verify_otp_invalid_format(self):
        """Test OTP verification with invalid format"""
        response = client.post(
            "/verify-otp",
            headers={"X-API-KEY": "test-key"},
            json={"email": "test@example.com", "otp": "abcdef"},
        )
        
        assert response.status_code == 400
        assert "6-digit" in response.json()["detail"]


class TestVerificationStatus:
    """Test verification status endpoint"""

    def test_get_verification_status_verified(self):
        """Test getting verification status for verified user"""
        db = TestingSessionLocal()
        
        email = "status@example.com"
        user = User(email=email, is_verified=True)
        db.add(user)
        db.commit()
        db.close()
        
        response = client.get(
            f"/verification-status/{email}",
            headers={"X-API-KEY": "test-key"},
        )
        
        assert response.status_code == 200
        assert response.json()["is_verified"] is True

    def test_get_verification_status_not_verified(self):
        """Test getting verification status for unverified user"""
        response = client.get(
            "/verification-status/nonexistent@example.com",
            headers={"X-API-KEY": "test-key"},
        )
        
        assert response.status_code == 200
        assert response.json()["is_verified"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
