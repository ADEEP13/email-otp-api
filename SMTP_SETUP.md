"""
Gmail SMTP Setup Guide - Step by Step

This file provides detailed instructions for setting up Gmail SMTP
for the Email OTP Verification Service.
"""

# ============================================================================
# OPTION 1: Gmail App Password (RECOMMENDED - More Secure)
# ============================================================================

"""
Gmail App Passwords are 16-character, application-specific passwords that
provide secure access to your Gmail account without exposing your main password.

Step 1: Enable 2-Step Verification
  1. Go to https://myaccount.google.com
  2. Click "Security" in the left menu
  3. Under "How you sign in to Google", find "2-Step Verification"
  4. Click "Get Started" and follow the prompts
  5. Confirm your phone number and verify the code
  
Step 2: Create App Password
  1. Go to https://myaccount.google.com/apppasswords
  2. Select "Mail" from the dropdown
  3. Select "Windows Computer" (or your platform)
  4. Google will generate a 16-character password
  5. Copy the password (e.g., "abcd efgh ijkl mnop")
  
Step 3: Add to .env File
  SMTP_EMAIL=your-email@gmail.com
  SMTP_PASSWORD=abcdefghijklmnop
  
Note: Remove spaces from the password when adding to .env

This is the RECOMMENDED method for production.
"""


# ============================================================================
# OPTION 2: Gmail Less Secure App Access (NOT RECOMMENDED)
# ============================================================================

"""
This method is less secure but simpler for development/testing.

WARNING: Google is phasing out this option. Use Option 1 for new accounts.

Steps:
  1. Go to https://myaccount.google.com/u/0/security?hl=en
  2. Find "Less secure app access"
  3. Click "Turn on access (not recommended)"
  4. Enable "Allow less secure apps"
  
Then in .env:
  SMTP_EMAIL=your-email@gmail.com
  SMTP_PASSWORD=your-gmail-password

Do NOT use this method for production!
"""


# ============================================================================
# OPTION 3: Gmail OAuth2 (For Advanced Users)
# ============================================================================

"""
OAuth2 is the most secure method but requires additional setup.

This project currently uses username/password authentication.
To implement OAuth2, you would need:

1. Setup Google Cloud Project
2. Enable Gmail API
3. Create OAuth2 credentials
4. Implement XOAUTH2 authentication in email_utils.py

For now, use Option 1 (App Password) for the best balance of
security and simplicity.
"""


# ============================================================================
# ALTERNATIVE: Other Email Providers
# ============================================================================

"""
If you prefer not to use Gmail, you can use other email providers.
Update these values in .env:

SENDGRID:
  SMTP_SERVER=smtp.sendgrid.net
  SMTP_PORT=587
  SMTP_EMAIL=apikey (literal)
  SMTP_PASSWORD=SG.your-sendgrid-api-key

MAILGUN:
  SMTP_SERVER=smtp.mailgun.org
  SMTP_PORT=587
  SMTP_EMAIL=postmaster@your-domain.mailgun.org
  SMTP_PASSWORD=your-mailgun-password

AWS SES:
  SMTP_SERVER=email-smtp.region.amazonaws.com
  SMTP_PORT=587
  SMTP_EMAIL=your-aws-email@example.com
  SMTP_PASSWORD=your-aws-smtp-password

OFFICE 365:
  SMTP_SERVER=smtp.office365.com
  SMTP_PORT=587
  SMTP_EMAIL=your-email@outlook.com
  SMTP_PASSWORD=your-password
"""


# ============================================================================
# SETUP VERIFICATION
# ============================================================================

"""
After configuring your SMTP settings, verify they work:

1. Create a test .env file with your SMTP settings
2. Run a test script:

    python -c "
    import smtplib
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_EMAIL = os.getenv('SMTP_EMAIL')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
        print('✅ SMTP Configuration is correct!')
    except Exception as e:
        print(f'❌ Error: {e}')
    "

3. Start the application:
    python main.py

4. Send a test OTP:
    curl -X POST "http://localhost:8000/send-otp" \
      -H "X-API-KEY: your-api-key" \
      -H "Content-Type: application/json" \
      -d '{"email": "your-email@gmail.com"}'

5. Check your email for the OTP (check spam folder too)
"""


# ============================================================================
# TROUBLESHOOTING
# ============================================================================

"""
Problem: "Authentication failed"
  Solution:
    1. Verify SMTP_EMAIL is correct
    2. For Gmail: Use App Password, not your account password
    3. Remove spaces from App Password in .env
    4. Ensure 2FA is enabled on your Gmail account

Problem: "Connection refused"
  Solution:
    1. Check SMTP_SERVER address is correct
    2. Check SMTP_PORT is correct (usually 587)
    3. Verify no firewall is blocking port 587
    4. Check your internet connection

Problem: "Invalid sender address"
  Solution:
    1. Ensure SMTP_EMAIL matches the email you're sending from
    2. For Gmail, use your full Gmail address
    3. For other providers, use the email associated with that account

Problem: "OTP not received"
  Solution:
    1. Verify SMTP connection first (run test script above)
    2. Check email spam folder
    3. Check application logs for SMTP errors
    4. Verify recipient email is valid format

Problem: ".env file not loading"
  Solution:
    1. Ensure .env file exists in project root
    2. Restart the application after editing .env
    3. Use absolute paths if needed
    4. Verify no syntax errors in .env file
"""


# ============================================================================
# SECURITY BEST PRACTICES
# ============================================================================

"""
1. Never commit .env file to Git
   - Add to .gitignore (already done in this project)
   - Use .env.example as template

2. Rotate credentials regularly
   - Update Gmail App Password every 90 days
   - Change API keys periodically

3. Use App Passwords instead of account password
   - More secure
   - Can be revoked individually
   - Can be used only by specific apps

4. Monitor email sending
   - Check logs for failed attempts
   - Set up alerts for unusual activity
   - Review Gmail Account Activity

5. Use environment variables in production
   - Never hardcode credentials
   - Use Railway/Heroku/AWS secrets management
   - Encrypt sensitive data at rest

6. CORS Configuration
   - In production, set specific allowed origins
   - Don't use allow_origins=["*"] in production
   - Example:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["https://yourdomain.com"],
        )
"""


# ============================================================================
# TESTING YOUR SETUP
# ============================================================================

"""
Complete verification checklist:

1. ✅ Gmail Account
   - 2FA enabled
   - App Password generated
   - No "Less secure apps" enabled

2. ✅ .env File
   - SMTP_EMAIL set to your Gmail
   - SMTP_PASSWORD is the 16-char App Password (no spaces)
   - SMTP_SERVER is "smtp.gmail.com"
   - SMTP_PORT is "587"

3. ✅ Application
   - Start with: python main.py
   - No startup errors
   - Database created
   - API responds to health check

4. ✅ API Key
   - API_KEY set in .env
   - X-API-KEY header included in requests

5. ✅ Email Sending
   - curl test request successful
   - Email received in inbox (or spam)
   - OTP is 6 digits
   - OTP works for verification

If all steps pass, you're ready for production! 🚀
"""


# ============================================================================
# DEPLOYMENT CONSIDERATIONS
# ============================================================================

"""
When deploying to production:

1. Use email service provider's SMTP
   - Gmail may have rate limits
   - Consider SendGrid, Mailgun, or AWS SES for high volume
   
2. Set up email signing
   - SPF record
   - DKIM record
   - DMARC policy
   
3. Configure delivery retry logic
   - Handle temporary SMTP failures
   - Implement exponential backoff
   
4. Monitor delivery status
   - Track bounce rates
   - Monitor complaints
   - Review logs
   
5. Setup dedicated sending domain
   - Improves deliverability
   - Separates OTP emails from transactional
   
6. Implement rate limiting
   - Limit OTPs per email per hour
   - Prevent abuse and spam
   - See DEPLOYMENT.md for examples
"""
