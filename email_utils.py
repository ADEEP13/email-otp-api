import random
import string
import requests
from dotenv import load_dotenv
import os
import logging
from sqlalchemy.orm import Session
from database import store_otp

load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Resend Email Configuration (Real email delivery - no domain needed)
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "noreply@otpservice.com")


def generate_otp(length: int = 6) -> str:
    """
    Generate a random 6-digit OTP.
    
    Args:
        length: Length of OTP to generate (default: 6)
    
    Returns:
        String containing only digits
    """
    return ''.join(random.choices(string.digits, k=length))


def send_otp_email(db: Session, recipient_email: str, otp_code: str = None) -> bool:
    """
    Generate OTP, store it in database, and send via Resend API.
    
    Args:
        db: Database session
        recipient_email: Email address to send OTP to
        otp_code: Optional pre-generated OTP (for testing). If None, generates new OTP.
    
    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        # Generate OTP if not provided
        if otp_code is None:
            otp_code = generate_otp()
        
        # Store OTP in database
        store_otp(db, recipient_email, otp_code)
        
        # Validate Resend API key is configured
        if not RESEND_API_KEY:
            logger.error("RESEND_API_KEY not configured")
            return False
        
        # HTML email body
        html = f"""\
<!DOCTYPE html>
<html>
  <head>
    <style>
      body {{
        font-family: Arial, sans-serif;
        line-height: 1.6;
        color: #333;
      }}
      .container {{
        max-width: 500px;
        margin: 0 auto;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 5px;
      }}
      .otp-code {{
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        letter-spacing: 5px;
        background-color: #f0f0f0;
        padding: 15px;
        border-radius: 5px;
        margin: 20px 0;
        color: #2c3e50;
      }}
      .footer {{
        font-size: 12px;
        color: #999;
        margin-top: 20px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <h2>Email OTP Verification</h2>
      <p>Your OTP verification code is:</p>
      <div class="otp-code">{otp_code}</div>
      <p style="color: #e74c3c; font-weight: bold;">This code will expire in 10 minutes.</p>
      <p>If you did not request this code, please ignore this email.</p>
      <div class="footer">
        <p>Email OTP Verification Service</p>
      </div>
    </div>
  </body>
</html>
"""
        
        # Plain text email body
        text = f"""Email OTP Verification

Your OTP verification code is: {otp_code}

This code will expire in 10 minutes.

If you did not request this code, please ignore this email.

Regards,
Email OTP Verification Service
"""
        
        # Resend API request
        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "from": SENDER_EMAIL,
            "to": recipient_email,
            "subject": "Your OTP Verification Code",
            "html": html,
            "text": text
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code in [200, 201]:
            logger.info(f"OTP email sent successfully to {recipient_email}")
            return True
        else:
            logger.error(f"Resend API error: {response.status_code} - {response.text}")
            return False
    
    except Exception as e:
        logger.error(f"Error sending OTP email: {str(e)}")
        return False
    
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP authentication failed. Check SMTP_USERNAME and SMTP_PASSWORD.")
        return False
    
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred: {str(e)}")
        return False
    
    except Exception as e:
        logger.error(f"Error sending OTP email: {str(e)}")
        return False
