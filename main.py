from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import os
import logging

from database import init_db, get_db, is_user_verified, verify_otp as verify_otp_db, get_user_or_create
from models import (
    SendOTPRequest,
    VerifyOTPRequest,
    OTPResponse,
    VerificationStatusResponse
)
from email_utils import send_otp_email

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load API key from environment
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    logger.warning("API_KEY not set in environment variables. Please set it for production.")

# FastAPI app initialization
app = FastAPI(
    title="Email OTP Verification Service",
    description="A production-grade microservice for email OTP verification",
    version="1.0.0"
)

# CORS middleware - Allow requests from any origin (configurable for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Authentication ==============

def verify_api_key(x_api_key: str = Header(None)) -> str:
    """
    Verify API key from X-API-KEY header.
    This dependency is used on all protected endpoints.
    
    Args:
        x_api_key: API key from request header
    
    Returns:
        The API key if valid
    
    Raises:
        HTTPException: 401 if API key is missing or invalid
    """
    if not x_api_key:
        logger.warning("Request rejected: Missing API key")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing. Please provide X-API-KEY header."
        )
    
    if API_KEY and x_api_key != API_KEY:
        logger.warning(f"Request rejected: Invalid API key attempt")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key."
        )
    
    return x_api_key


# ============== Startup & Shutdown ==============

@app.on_event("startup")
async def startup_event():
    """
    Initialize database on application startup.
    Creates all tables if they don't exist.
    """
    logger.info("Starting Email OTP Verification Service...")
    init_db()
    logger.info("Database initialized successfully.")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown handler.
    """
    logger.info("Email OTP Verification Service shutting down.")


# ============== API Endpoints ==============

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint (no authentication required).
    Used for monitoring and load balancer checks.
    
    Returns:
        JSON with status
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "healthy", "service": "Email OTP Verification API"}
    )


@app.post(
    "/send-otp",
    response_model=OTPResponse,
    status_code=status.HTTP_200_OK,
    tags=["OTP Operations"]
)
async def send_otp(
    request: SendOTPRequest,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """
    Send OTP to the provided email address.
    
    This endpoint:
    1. Validates email format (done by Pydantic)
    2. Generates a random 6-digit OTP
    3. Stores OTP with 10-minute expiry in database
    4. Replaces any existing active OTP for this email
    5. Sends OTP via email using SMTP
    
    **Security**: Requires valid X-API-KEY header
    
    Args:
        request: SendOTPRequest containing email
        api_key: API key (verified by dependency)
        db: Database session
    
    Returns:
        OTPResponse with success status and message
    
    Raises:
        HTTPException 400: If email is invalid
        HTTPException 401: If API key is missing or invalid
        HTTPException 500: If email sending fails
    """
    try:
        email = request.email.lower().strip()
        
        # Ensure user exists in database
        get_user_or_create(db, email)
        
        # Send OTP email
        if not send_otp_email(db, email):
            logger.error(f"Failed to send OTP email to {email}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send OTP email. Please check your SMTP configuration."
            )
        
        logger.info(f"OTP sent successfully to {email}")
        
        return OTPResponse(
            success=True,
            message="OTP sent successfully. Check your email.",
            email=email
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error in send_otp: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


@app.post(
    "/verify-otp",
    response_model=OTPResponse,
    status_code=status.HTTP_200_OK,
    tags=["OTP Operations"]
)
async def verify_otp(
    request: VerifyOTPRequest,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """
    Verify OTP for the provided email address.
    
    This endpoint:
    1. Validates OTP exists and hasn't expired
    2. Checks if OTP matches the provided code
    3. Marks OTP as verified (one-time use)
    4. Marks user email as verified
    
    **Security**: Requires valid X-API-KEY header
    
    Args:
        request: VerifyOTPRequest containing email and otp
        api_key: API key (verified by dependency)
        db: Database session
    
    Returns:
        OTPResponse with verification status
    
    Raises:
        HTTPException 401: If API key is missing or invalid
        HTTPException 400: If OTP is invalid or expired
    """
    try:
        email = request.email.lower().strip()
        otp_code = request.otp.strip()
        
        # Validate OTP format (should be 6 digits)
        if not otp_code.isdigit() or len(otp_code) != 6:
            logger.warning(f"Invalid OTP format for {email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP must be a 6-digit number."
            )
        
        # Verify OTP
        success, message = verify_otp_db(db, email, otp_code)
        
        if not success:
            logger.warning(f"OTP verification failed for {email}: {message}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        logger.info(f"OTP verified successfully for {email}")
        
        return OTPResponse(
            success=True,
            message=message,
            email=email
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error in verify_otp: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


@app.get(
    "/verification-status/{email}",
    response_model=VerificationStatusResponse,
    status_code=status.HTTP_200_OK,
    tags=["OTP Operations"]
)
async def get_verification_status(
    email: str,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """
    Get email verification status for a user.
    
    **Security**: Requires valid X-API-KEY header
    
    Args:
        email: Email address to check
        api_key: API key (verified by dependency)
        db: Database session
    
    Returns:
        VerificationStatusResponse with verification status
    
    Raises:
        HTTPException 401: If API key is missing or invalid
    """
    try:
        email = email.lower().strip()
        is_verified = is_user_verified(db, email)
        
        return VerificationStatusResponse(
            email=email,
            is_verified=is_verified,
            message="Verified" if is_verified else "Not verified"
        )
    
    except Exception as e:
        logger.error(f"Error in get_verification_status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )


@app.get("/", tags=["Info"])
async def root():
    """
    API root endpoint with service information.
    """
    return {
        "service": "Email OTP Verification API",
        "version": "1.0.0",
        "description": "A production-grade microservice for email OTP verification",
        "endpoints": {
            "health": "/health (GET)",
            "send_otp": "/send-otp (POST) - Protected",
            "verify_otp": "/verify-otp (POST) - Protected",
            "verification_status": "/verification-status/{email} (GET) - Protected"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        log_level="info"
    )
