# Quick Start Guide - Email OTP Verification Service

## 🚀 Get Running in 5 Minutes

### Step 1: Install Dependencies (1 minute)

```bash
# Activate virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install requirements
pip install -r requirements.txt
```

### Step 2: Setup Environment (1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# Key settings to update:
# - API_KEY: Generate a random secure key (use: python -c "import secrets; print(secrets.token_urlsafe(32))")
# - SMTP_EMAIL: Your Gmail address
# - SMTP_PASSWORD: Your Gmail App Password (https://support.google.com/accounts/answer/185833)
```

**Getting Gmail App Password:**
1. Enable 2-factor authentication on your Gmail account
2. Visit: https://myaccount.google.com/apppasswords
3. Select "Mail" and "Windows Computer"
4. Generate password and copy the 16-character password
5. Paste into SMTP_PASSWORD in .env

### Step 3: Run the Service (1 minute)

```bash
# Start the service
python main.py

# You'll see:
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 4: Test the API (1 minute)

```bash
# In another terminal, test sending OTP:
curl -X POST "http://localhost:8000/send-otp" \
  -H "X-API-KEY: your-api-key-from-env" \
  -H "Content-Type: application/json" \
  -d '{"email": "your-email@gmail.com"}'

# Expected response:
# {
#   "success": true,
#   "message": "OTP sent successfully. Check your email.",
#   "email": "your-email@gmail.com"
# }
```

### Step 5: Access Documentation (1 minute)

- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

---

## 📊 API Reference

### Send OTP

```bash
POST /send-otp
Headers: X-API-KEY: your-api-key
Body: {"email": "user@example.com"}
Response: 200 OK
```

### Verify OTP

```bash
POST /verify-otp
Headers: X-API-KEY: your-api-key
Body: {"email": "user@example.com", "otp": "123456"}
Response: 200 OK
```

### Check Verification Status

```bash
GET /verification-status/{email}
Headers: X-API-KEY: your-api-key
Response: 200 OK
```

### Health Check

```bash
GET /health
Response: 200 OK (No auth required)
```

---

## 🐛 Troubleshooting

### OTP Not Received?

1. Check SMTP_EMAIL and SMTP_PASSWORD in .env
2. Verify it's the correct Gmail App Password (not your account password)
3. Check your email spam folder
4. Verify Gmail account has 2FA enabled
5. View logs in the terminal for error messages

### API Key Issues?

```bash
# Generate a new secure API key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Update in .env file
# Restart the service
```

### Database Issues?

```bash
# Delete the existing database file
rm otp_service.db

# Restart - it will recreate automatically
python main.py
```

### Port Already in Use?

```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port
uvicorn main:app --port 8001
```

---

## 💡 Testing with Python

```python
import requests
import json

API_URL = "http://localhost:8000"
API_KEY = "your-api-key"

def send_otp(email):
    response = requests.post(
        f"{API_URL}/send-otp",
        headers={"X-API-KEY": API_KEY},
        json={"email": email}
    )
    print(f"Send OTP: {response.json()}")
    return response.json()

def verify_otp(email, otp):
    response = requests.post(
        f"{API_URL}/verify-otp",
        headers={"X-API-KEY": API_KEY},
        json={"email": email, "otp": otp}
    )
    print(f"Verify OTP: {response.json()}")
    return response.json()

def check_status(email):
    response = requests.get(
        f"{API_URL}/verification-status/{email}",
        headers={"X-API-KEY": API_KEY}
    )
    print(f"Status: {response.json()}")
    return response.json()

# Test flow
if __name__ == "__main__":
    email = "test@example.com"
    
    # Step 1: Send OTP
    send_otp(email)
    
    # Step 2: Check status (should be unverified)
    check_status(email)
    
    # Step 3: Verify OTP (after user enters it)
    # Note: Get the actual OTP from email
    verify_otp(email, "123456")  # Replace with actual OTP
    
    # Step 4: Check status (should be verified)
    check_status(email)
```

---

## 🚀 Next Steps

1. **Development**: Check [README.md](README.md) for full documentation
2. **Testing**: Run `pytest tests/` to execute test suite
3. **Deployment**: Follow [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
4. **Integration**: Integrate with your main application using API calls

---

## 📚 Full Documentation

- **README.md** - Complete feature list and documentation
- **DEPLOYMENT.md** - Production deployment guides (Railway, AWS, Heroku, Docker)
- **API Docs** - Available at http://localhost:8000/docs when running

---

## ✅ Checklist Before Production

- [ ] Generated secure API_KEY
- [ ] Gmail App Password configured
- [ ] SMTP credentials verified (OTP sends successfully)
- [ ] Database working (can create users and OTPs)
- [ ] Tests passing (`pytest tests/`)
- [ ] All endpoints tested manually
- [ ] CORS settings configured for your domain
- [ ] Error handling verified
- [ ] Logs configured
- [ ] Ready for deployment

---

## 🆘 Need Help?

1. Check the full [README.md](README.md)
2. Review [DEPLOYMENT.md](DEPLOYMENT.md) for setup guides
3. Check application logs for errors
4. Verify all environment variables are set correctly
5. Test health endpoint: `curl http://localhost:8000/health`

---

**Congratulations! Your Email OTP Verification Service is ready to use! 🎉**
