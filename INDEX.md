# 📧 Email OTP Verification Microservice

## 🎉 Welcome!

Your production-grade Email OTP Verification Microservice is complete and ready to use. This is a standalone REST API that handles email verification using One-Time Passwords (OTPs).

---

## ⚡ Quick Navigation

### 🚀 New to This Project?
1. **Start Here**: [QUICKSTART.md](QUICKSTART.md) - 5 minute setup guide
2. **See Examples**: [README.md](README.md#-api-usage-examples) - API usage examples
3. **Full Details**: [README.md](README.md) - Comprehensive documentation

### 🔧 Setup & Configuration
- **SMTP Setup**: [SMTP_SETUP.md](SMTP_SETUP.md) - Configure email (Gmail recommended)
- **Environment**: [.env.example](.env.example) - All configuration options
- **Testing**: Run `pytest tests/ -v`

### 🚢 Deployment
- **Railway** (Recommended): [README.md](README.md#-railway-deployment)
- **Docker**: [Dockerfile](Dockerfile) + [DEPLOYMENT.md](DEPLOYMENT.md#docker-deployment)
- **AWS EC2**: [DEPLOYMENT.md](DEPLOYMENT.md#aws-ec2-deployment)
- **Heroku**: [DEPLOYMENT.md](DEPLOYMENT.md#heroku-deployment-alternative)

### 📚 Reference
- **Architecture**: [IMPLEMENTATION.md](IMPLEMENTATION.md)
- **All Files**: [PROJECT_REFERENCE.md](PROJECT_REFERENCE.md)
- **Endpoints**: [README.md](README.md#-api-endpoints) or http://localhost:8000/docs

---

## ✨ What You Get

### ✅ Core Features
- 5 REST API endpoints (send OTP, verify OTP, check status, health, info)
- API Key authentication on all protected endpoints
- 6-digit random OTP generation
- 10-minute expiration window
- One-time use enforcement (reuse prevention)
- Email sending via SMTP (Gmail, SendGrid, etc.)
- SQLite development + PostgreSQL production support
- Comprehensive error handling and validation

### ✅ Production Ready
- Clean, well-documented code
- Comprehensive test suite (13+ tests)
- Docker containerization
- Railway one-click deployment
- AWS EC2 deployment guide
- Heroku deployment guide
- Security best practices implemented
- Logging and monitoring support
- CORS configured

### ✅ Documentation
- [README.md](README.md) - Complete documentation
- [QUICKSTART.md](QUICKSTART.md) - 5-minute setup
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
- [SMTP_SETUP.md](SMTP_SETUP.md) - Email configuration
- [IMPLEMENTATION.md](IMPLEMENTATION.md) - Architecture details
- [PROJECT_REFERENCE.md](PROJECT_REFERENCE.md) - File reference
- API docs at http://localhost:8000/docs

---

## 🎯 5-Minute Quick Start

```bash
# 1. Setup Python environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and set: API_KEY, SMTP_EMAIL, SMTP_PASSWORD
# (Get Gmail App Password at: https://support.google.com/accounts/answer/185833)

# 4. Run the service
python main.py

# 5. Test an endpoint
curl -X POST "http://localhost:8000/send-otp" \
  -H "X-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"email": "your-email@gmail.com"}'

# 6. Check documentation
# Open: http://localhost:8000/docs
```

---

## 📋 File Structure

```
email-otp-api/
├── main.py                    # FastAPI application with endpoints
├── models.py                  # Database and request/response models  
├── database.py                # Database operations and ORM utilities
├── email_utils.py             # Email sending logic
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Poetry configuration
├── Dockerfile                 # Docker containerization
├── railway.toml               # Railway deployment config
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── README.md                  # Full documentation (400+ lines)
├── QUICKSTART.md              # 5-minute setup guide
├── DEPLOYMENT.md              # Production deployment guides
├── SMTP_SETUP.md              # Gmail SMTP setup guide
├── IMPLEMENTATION.md          # Architecture and implementation details
├── PROJECT_REFERENCE.md       # File reference guide
├── INDEX.md                   # This file
└── tests/
    └── test_api.py            # Comprehensive test suite
```

---

## 🔌 API Endpoints

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| GET | `/health` | ❌ | Health check |
| GET | `/` | ❌ | Service info |
| POST | `/send-otp` | ✅ | Send OTP to email |
| POST | `/verify-otp` | ✅ | Verify OTP code |
| GET | `/verification-status/{email}` | ✅ | Check if email verified |

**✅ = Requires X-API-KEY header**

---

## 📡 Usage Example (Python)

```python
import requests

API_URL = "http://localhost:8000"
API_KEY = "your-api-key"

# Send OTP
response = requests.post(
    f"{API_URL}/send-otp",
    headers={"X-API-KEY": API_KEY},
    json={"email": "user@example.com"}
)
print(response.json())

# Verify OTP (after user enters it)
response = requests.post(
    f"{API_URL}/verify-otp",
    headers={"X-API-KEY": API_KEY},
    json={"email": "user@example.com", "otp": "123456"}
)
print(response.json())

# Check verification status
response = requests.get(
    f"{API_URL}/verification-status/user@example.com",
    headers={"X-API-KEY": API_KEY}
)
print(response.json())
```

---

## 🌐 Deployment Options

### 1. Railway (Recommended) ⭐
- **Time**: ~2 minutes
- **Cost**: Free tier available
- **Benefits**: HTTPS, auto-scaling, easy environment setup
- **Guide**: See [README.md](README.md#-railway-deployment)

### 2. Docker
- **Time**: ~5 minutes
- **Cost**: Your infrastructure
- **Benefits**: Portable, reproducible
- **Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md#docker-deployment)

### 3. AWS EC2
- **Time**: ~20 minutes
- **Cost**: Small instance = ~$5/month
- **Benefits**: Full control, scalable
- **Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md#aws-ec2-deployment)

### 4. Heroku
- **Time**: ~5 minutes
- **Cost**: Free tier available
- **Benefits**: Simple, good for small apps
- **Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md#heroku-deployment-alternative)

---

## 🔐 Security Features

- ✅ API Key authentication (X-API-KEY header)
- ✅ Email format validation (RFC 5322)
- ✅ OTP: 6-digit random generation
- ✅ OTP: 10-minute expiration enforcement
- ✅ OTP: One-time use only (cannot be reused)
- ✅ OTP: Only one active per email
- ✅ HTTPS ready for production
- ✅ Environment variables for secrets
- ✅ Error handling without exposing internals
- ✅ CORS configured (adjustable for production)
- ✅ Logging for audit trail

---

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=.
```

**Test Coverage**:
- Health endpoints ✅
- Send OTP functionality ✅
- OTP verification ✅
- OTP expiration ✅
- One-time use enforcement ✅
- Verification status ✅
- Authentication ✅
- Error handling ✅

---

## 💻 Development

### Local Development
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
python main.py

# Or with hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Code Quality
```bash
# Format code
black main.py models.py database.py email_utils.py

# Lint
flake8 main.py models.py database.py email_utils.py

# Type check
mypy main.py models.py database.py email_utils.py
```

---

## 🐛 Troubleshooting

### Setup Issues
1. **"Module not found"**: Run `pip install -r requirements.txt`
2. **"Port 8000 in use"**: Change port or kill process (see [QUICKSTART.md](QUICKSTART.md))
3. **"Missing .env"**: Copy `.env.example` to `.env` and edit

### Email Issues
1. **"OTP not received"**: Check [SMTP_SETUP.md](SMTP_SETUP.md)
2. **"Authentication failed"**: Verify Gmail App Password (not account password)
3. **"SMTP connection error"**: Check SMTP_SERVER and SMTP_PORT

### API Issues
1. **"401 Unauthorized"**: Include `X-API-KEY` header in requests
2. **"400 Bad Request"**: Check JSON format and email validity
3. **"500 Error"**: Check logs, ensure SMTP is configured

**More troubleshooting**: See [README.md](README.md#-troubleshooting)

---

## 🚀 Next Steps

### 👤 For New Users
1. Read [QUICKSTART.md](QUICKSTART.md) - Setup in 5 minutes
2. Test locally at http://localhost:8000/docs
3. Try the API examples in [README.md](README.md#-api-usage-examples)

### 👨‍💻 For Developers
1. Review [IMPLEMENTATION.md](IMPLEMENTATION.md) - Architecture details
2. Explore source code - all well documented
3. Run tests: `pytest tests/ -v`
4. Customize as needed

### 🚢 For Deployment
1. Choose platform: [README.md](README.md#-railway-deployment) or [DEPLOYMENT.md](DEPLOYMENT.md)
2. Configure environment variables
3. Deploy! Get public HTTPS URL
4. Integrate with main application

### 🔗 For Integration
1. See [README.md](README.md#-usage-in-your-application) - Integration examples
2. Call `/send-otp` during signup
3. Call `/verify-otp` when user submits OTP
4. Use `/verification-status` to check anytime

---

## 📚 Documentation Index

| Document | Purpose | Audience |
|----------|---------|----------|
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup | Everyone |
| [README.md](README.md) | Full documentation | Developers |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production setup | DevOps/Developers |
| [SMTP_SETUP.md](SMTP_SETUP.md) | Email configuration | Everyone |
| [IMPLEMENTATION.md](IMPLEMENTATION.md) | Architecture details | Developers |
| [PROJECT_REFERENCE.md](PROJECT_REFERENCE.md) | File reference | Developers |
| [INDEX.md](INDEX.md) | Navigation (this file) | Everyone |

---

## ✅ Features Checklist

Implementation status of all requirements:

- ✅ REST APIs - 5 endpoints, FastAPI, well-documented
- ✅ API Key Authentication - X-API-KEY header on all protected endpoints
- ✅ SQL Database - SQLAlchemy ORM, SQLite dev, PostgreSQL ready
- ✅ Database Schema - users and otp_verifications tables
- ✅ OTP Management - 6-digit, 10-min expiry, one-time use, single per email
- ✅ API Endpoints - send-otp, verify-otp, verification-status
- ✅ Email SMTP - Gmail, SendGrid, Mailgun, AWS SES supported
- ✅ Environment Variables - All secrets externalized
- ✅ SQLAlchemy ORM - Full ORM implementation with proper models
- ✅ Auto Table Creation - Database initialized on startup
- ✅ HTTP Status Codes - 200, 400, 401, 500 as appropriate
- ✅ Error Handling - Comprehensive validation and error messages
- ✅ Clean Structure - Separate files for app, DB, models, email
- ✅ Deployment Ready - Railway, Docker, AWS, Heroku guides included

---

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)
- [Pydantic Validation](https://docs.pydantic.dev)
- [Railway Deployment](https://docs.railway.app)
- [Docker Documentation](https://docs.docker.com)

---

## 💡 Tips & Tricks

### Development
- Use http://localhost:8000/docs for interactive API testing
- Check logs in terminal for debugging
- Use `pytest tests/ -v -s` to see print statements in tests

### Production
- Use environment variables for all secrets
- Enable HTTPS/SSL
- Setup monitoring and alerts
- Use PostgreSQL instead of SQLite
- Consider rate limiting
- Monitor API usage

### Integration
- Keep API_KEY secret (don't expose in frontend)
- Implement retry logic for failed OTP sends
- Cache verification status for performance
- Set appropriate CORS origins

---

## 📞 Support

### If You Get Stuck
1. Check the troubleshooting section of relevant document
2. Review the API docs: http://localhost:8000/docs
3. Check application logs for error details
4. Verify all environment variables are set
5. Run tests to verify functionality

### Common Questions
- **"How do I get Gmail App Password?"** → See [SMTP_SETUP.md](SMTP_SETUP.md)
- **"How do I deploy?"** → See [DEPLOYMENT.md](DEPLOYMENT.md)
- **"How do I integrate this?"** → See [README.md](README.md#-usage-in-your-application)
- **"How do I run tests?"** → Run `pytest tests/ -v`
- **"Where's the API documentation?"** → http://localhost:8000/docs

---

## 🎉 You're All Set!

Your Email OTP Verification Microservice is ready to:
- ✅ Run locally for development
- ✅ Deploy to production
- ✅ Scale to millions of users
- ✅ Integrate with your application
- ✅ Handle email verification securely

**Get started now:**
1. Follow [QUICKSTART.md](QUICKSTART.md) - 5 minutes
2. Deploy to [Railway](README.md#-railway-deployment) - 2 minutes
3. Integrate with your app - depends on your app

---

**Happy OTP Verification! 🚀**

Questions? Check the documentation files listed above.
