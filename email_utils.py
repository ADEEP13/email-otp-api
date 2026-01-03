import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import logging
from sqlalchemy.orm import Session
from database import store_otp

load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Mailgun SMTP Configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.mailgun.org")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "otp@sandboxe684275e3d7c4f19b35b99c01272c447.mailgun.org")


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
    Generate OTP, store it in database, and send via Mailgun SMTP.
    
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
        
        # Validate SMTP credentials are configured
        if not SMTP_USERNAME or not SMTP_PASSWORD:
            logger.error("SMTP_USERNAME or SMTP_PASSWORD not configured")
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
        
        # Create MIME message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your OTP Verification Code"
        message["From"] = SENDER_EMAIL
        message["To"] = recipient_email
        
        # Attach text and HTML parts
        message.attach(MIMEText(text, "plain"))
        message.attach(MIMEText(html, "html"))
        
        # Send via Mailgun SMTP
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()  # Enable TLS encryption
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(message)
        
        logger.info(f"OTP email sent successfully to {recipient_email}")
        return True
    
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP authentication failed. Check SMTP_USERNAME and SMTP_PASSWORD.")
        return False
    
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred: {str(e)}")
        return False
    
    except Exception as e:
        logger.error(f"Error sending OTP email: {str(e)}")
        return False
