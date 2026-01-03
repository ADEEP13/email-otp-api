# Email OTP Verification Microservice

A production-grade Email OTP (One-Time Password) Verification Microservice built with **FastAPI** and **SQLAlchemy**. This service handles email verification using OTP tokens and can be easily integrated into any application during user signup or authentication flows.

## 🎯 Features

✅ **RESTful API** - Clean, well-documented endpoints following REST conventions  
✅ **API Key Authentication** - Secure all endpoints with X-API-KEY header  
✅ **SQLAlchemy ORM** - Database-agnostic (SQLite for dev, PostgreSQL for production)  
✅ **Email SMTP Integration** - Send OTPs via Gmail or any SMTP provider  
✅ **OTP Management**:
   - Generate random 6-digit OTPs
   - 10-minute expiration window
   - One-time use enforcement
   - Only one active OTP per email

✅ **Comprehensive Error Handling** - Proper HTTP status codes and error messages  
✅ **Logging** - Full request/response logging for debugging  
✅ **CORS Enabled** - Ready for cross-origin requests  
✅ **Docker & Railway Ready** - Deploy with one command  
✅ **Well-Documented** - Clean code with detailed comments

---

## 📋 System Architecture

### Database Schema

**users table**
```
- id: Primary key
- email: Unique email address
- is_verified: Boolean flag for verification status
- created_at: Timestamp
```

**otp_verifications table**
```
- id: Primary key
- email: Associated email
- otp: 6-digit OTP code
- expires_at: Expiration timestamp (10 minutes)
- verified: Boolean (one-time use enforcement)
- created_at: Timestamp
```

### API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/health` | ❌ | Health check for monitoring |
| GET | `/` | ❌ | API info endpoint |
| POST | `/send-otp` | ✅ | Send OTP to email |
| POST | `/verify-otp` | ✅ | Verify OTP and mark user as verified |
| GET | `/verification-status/{email}` | ✅ | Check verification status |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip or Poetry
- Gmail account (for SMTP) or other email provider

### 1. Clone & Setup

```bash
# Navigate to project directory
cd email-otp-api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env with your configuration
# IMPORTANT: Set API_KEY, SMTP_EMAIL, SMTP_PASSWORD
```

**For Gmail SMTP:**
1. Enable 2-factor authentication on your Gmail account
2. Generate an [App Password](https://support.google.com/accounts/answer/185833)
3. Use the generated 16-character password in `SMTP_PASSWORD`

### 3. Run the Service

```bash
# Development server
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### 4. Access Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📡 API Usage Examples

### 1. Send OTP

```bash
curl -X POST "http://localhost:8000/send-otp" \
  -H "X-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "OTP sent successfully. Check your email.",
  "email": "user@example.com"
}
```

### 2. Verify OTP

```bash
curl -X POST "http://localhost:8000/verify-otp" \
  -H "X-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "otp": "123456"}'
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Email verified successfully!",
  "email": "user@example.com"
}
```

### 3. Check Verification Status

```bash
curl -X GET "http://localhost:8000/verification-status/user@example.com" \
  -H "X-API-KEY: your-api-key"
```

**Response (200 OK):**
```json
{
  "email": "user@example.com",
  "is_verified": true,
  "message": "Verified"
}
```

### 4. Health Check

```bash
curl http://localhost:8000/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "Email OTP Verification API"
}
```

---

## 🔐 Security Features

### API Key Authentication
- All OTP endpoints require `X-API-KEY` header
- Validate on every protected request
- Return 401 Unauthorized for missing/invalid keys

### OTP Security
- Random 6-digit generation (0-999999)
- 10-minute expiration enforcement
- One-time use - automatically marked as verified after use
- Only one active OTP per email at any time

### Email Validation
- RFC 5322 compliant email validation via Pydantic
- Case-insensitive email handling
- Duplicate OTP prevention

---

## 🗄️ Database Setup

### Development (SQLite)
Automatic setup - no configuration needed. Database file created as `otp_service.db`

### Production (PostgreSQL)

```bash
# Update .env
DATABASE_URL=postgresql://user:password@localhost:5432/otp_service

# Install PostgreSQL driver
pip install psycopg2-binary
```

**Create PostgreSQL database:**
```sql
CREATE DATABASE otp_service;
CREATE USER otp_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE otp_service TO otp_user;
```

---

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t email-otp-api:1.0 .
```

### Run Container

```bash
docker run -d \
  -e API_KEY=your-secure-key \
  -e SMTP_EMAIL=your-email@gmail.com \
  -e SMTP_PASSWORD=your-app-password \
  -p 8000:8000 \
  email-otp-api:1.0
```

---

## 🚂 Railway Deployment

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Connect Railway

1. Visit [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Add environment variables:
   - `API_KEY`
   - `SMTP_EMAIL`
   - `SMTP_PASSWORD`
   - `DATABASE_URL` (optional - uses SQLite by default)

5. Deploy and get public HTTPS URL

### 3. Test Deployment

```bash
curl -X POST "https://your-railway-url.railway.app/send-otp" \
  -H "X-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

---

## 📊 Project Structure

```
email-otp-api/
├── main.py                 # FastAPI application & endpoints
├── models.py               # SQLAlchemy & Pydantic models
├── database.py             # Database operations & ORM utilities
├── email_utils.py          # SMTP email sending logic
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── Dockerfile              # Docker configuration
├── railway.toml            # Railway deployment config
├── README.md               # This file
└── otp_service.db          # SQLite database (auto-created)
```

---

## 🛠️ Development

### Install Dev Dependencies

```bash
pip install pytest pytest-asyncio httpx black flake8
```

### Code Formatting

```bash
black main.py models.py database.py email_utils.py
flake8 main.py models.py database.py email_utils.py
```

### Run Tests

```bash
pytest tests/
```

---

## 🔧 Configuration Reference

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_KEY` | - | **REQUIRED** - API authentication key |
| `DATABASE_URL` | `sqlite:///./otp_service.db` | Database connection string |
| `SMTP_SERVER` | `smtp.gmail.com` | SMTP server address |
| `SMTP_PORT` | `587` | SMTP port (587 for TLS) |
| `SMTP_EMAIL` | - | **REQUIRED** - Sender email address |
| `SMTP_PASSWORD` | - | **REQUIRED** - SMTP password or app password |
| `PORT` | `8000` | Application port |
| `LOG_LEVEL` | `INFO` | Logging level |

---

## 📝 Usage in Your Application

### Integration Example (Python)

```python
import requests

OTP_API_URL = "https://your-otp-service.com"
API_KEY = "your-api-key"

def send_user_otp(email: str):
    """Send OTP to user email"""
    response = requests.post(
        f"{OTP_API_URL}/send-otp",
        headers={"X-API-KEY": API_KEY},
        json={"email": email}
    )
    return response.json()

def verify_user_otp(email: str, otp: str):
    """Verify user OTP"""
    response = requests.post(
        f"{OTP_API_URL}/verify-otp",
        headers={"X-API-KEY": API_KEY},
        json={"email": email, "otp": otp}
    )
    return response.json()

def check_verification_status(email: str):
    """Check if user is verified"""
    response = requests.get(
        f"{OTP_API_URL}/verification-status/{email}",
        headers={"X-API-KEY": API_KEY}
    )
    return response.json()
```

### Integration Example (JavaScript/Node.js)

```javascript
const OTP_API_URL = "https://your-otp-service.com";
const API_KEY = "your-api-key";

async function sendUserOTP(email) {
  const response = await fetch(`${OTP_API_URL}/send-otp`, {
    method: "POST",
    headers: {
      "X-API-KEY": API_KEY,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email })
  });
  return response.json();
}

async function verifyUserOTP(email, otp) {
  const response = await fetch(`${OTP_API_URL}/verify-otp`, {
    method: "POST",
    headers: {
      "X-API-KEY": API_KEY,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email, otp })
  });
  return response.json();
}
```

---

## 🐛 Troubleshooting

### SMTP Authentication Failed
- ✅ Verify SMTP_EMAIL and SMTP_PASSWORD in .env
- ✅ For Gmail, use [App Passwords](https://support.google.com/accounts/answer/185833), not your actual password
- ✅ Enable "Less secure app access" if not using App Passwords

### OTP Not Received
- ✅ Check SMTP configuration
- ✅ Verify recipient email is valid
- ✅ Check spam folder
- ✅ View logs: `docker logs <container_id>`

### Database Errors
- ✅ Ensure DATABASE_URL is correct
- ✅ Check PostgreSQL credentials for production
- ✅ Verify file permissions for SQLite

### API Key Issues
- ✅ Ensure X-API-KEY header is set in requests
- ✅ Verify API key matches environment variable
- ✅ Check for extra whitespace in environment variables

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)
- [Pydantic Validation](https://docs.pydantic.dev)
- [Railway Deployment Guide](https://docs.railway.app)

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## ✉️ Support

For issues, questions, or suggestions:
- Open an [GitHub Issue](https://github.com/yourusername/email-otp-api/issues)
- Check existing issues and documentation
- Provide detailed error messages and environment details

---

## 🎉 Happy OTP Verification!

This service is production-ready and optimized for:
- ✅ High availability
- ✅ Easy scaling
- ✅ Security best practices
- ✅ Enterprise deployments

**Get started in 5 minutes!**
