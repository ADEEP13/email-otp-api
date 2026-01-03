# Deployment Guide

## Local Development

### 1. Setup

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# Important: Set API_KEY, SMTP_EMAIL, SMTP_PASSWORD
```

### 3. Run Locally

```bash
python main.py
```

Access at: `http://localhost:8000`

---

## Docker Deployment

### Build & Run Locally

```bash
# Build image
docker build -t email-otp-api:1.0 .

# Run container
docker run -d \
  --name otp-api \
  -e API_KEY=your-secure-key \
  -e SMTP_EMAIL=your-email@gmail.com \
  -e SMTP_PASSWORD=your-app-password \
  -p 8000:8000 \
  email-otp-api:1.0

# View logs
docker logs otp-api

# Stop container
docker stop otp-api
```

### Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Tag image
docker tag email-otp-api:1.0 yourusername/email-otp-api:1.0

# Push
docker push yourusername/email-otp-api:1.0
```

---

## Railway Deployment (Recommended)

### Prerequisites
- GitHub account with repository
- Railway account (free tier available)

### Step 1: Push Code to GitHub

```bash
# Initialize Git
git init
git add .
git commit -m "Initial commit: Email OTP Verification Service"

# Create repository on GitHub and push
git remote add origin https://github.com/yourusername/email-otp-api.git
git push -u origin main
```

### Step 2: Create Railway Project

1. Go to [Railway.app](https://railway.app)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize GitHub and select your repository
5. Railway will auto-detect it's a Python project

### Step 3: Configure Environment Variables

In Railway dashboard:

1. Click **"Variables"**
2. Add the following:

```
API_KEY=your-very-secure-random-key
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password-here
DATABASE_URL=sqlite:///./otp_service.db
PORT=8000
```

### Step 4: Deploy

1. Railway will automatically build and deploy
2. Once deployment completes, you'll get a public URL
3. Your service is now live!

### Step 5: Test Deployment

```bash
# Get your Railway URL from dashboard
export RAILWAY_URL="https://your-app-name.railway.app"
export API_KEY="your-api-key"

# Test health
curl $RAILWAY_URL/health

# Test send OTP
curl -X POST $RAILWAY_URL/send-otp \
  -H "X-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

---

## AWS EC2 Deployment

### 1. Launch EC2 Instance

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-venv -y

# Install Git
sudo apt install git -y
```

### 2. Clone Repository

```bash
git clone https://github.com/yourusername/email-otp-api.git
cd email-otp-api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Environment

```bash
# Create .env file
nano .env

# Add configuration (press Ctrl+O to save, Ctrl+X to exit)
API_KEY=your-secure-key
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
DATABASE_URL=postgresql://user:password@localhost:5432/otp_service
PORT=8000
```

### 4. Setup PostgreSQL (for production)

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Connect to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE otp_service;
CREATE USER otp_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE otp_service TO otp_user;
\q
```

### 5. Setup Systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/otp-api.service

# Add the following content:
```

```ini
[Unit]
Description=Email OTP Verification API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/email-otp-api
ExecStart=/home/ubuntu/email-otp-api/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10
Environment="PATH=/home/ubuntu/email-otp-api/venv/bin"

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable otp-api
sudo systemctl start otp-api

# Check status
sudo systemctl status otp-api

# View logs
sudo journalctl -u otp-api -f
```

### 6. Setup Nginx Reverse Proxy

```bash
# Install Nginx
sudo apt install nginx -y

# Create Nginx config
sudo nano /etc/nginx/sites-available/otp-api
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/otp-api /etc/nginx/sites-enabled/

# Test Nginx config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### 7. Setup SSL (HTTPS)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is enabled by default
```

---

## Heroku Deployment (Alternative)

### 1. Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

### 2. Create Procfile

```bash
# In project root
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile
```

### 3. Deploy

```bash
# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set API_KEY=your-secure-key
heroku config:set SMTP_EMAIL=your-email@gmail.com
heroku config:set SMTP_PASSWORD=your-app-password

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

---

## Monitoring & Maintenance

### Health Checks

```bash
# Setup monitoring endpoint
curl -X GET https://your-domain.com/health

# Use with monitoring services:
# - UptimeRobot
# - Datadog
# - New Relic
# - CloudWatch
```

### Database Backups

```bash
# PostgreSQL backup
pg_dump otp_service > backup.sql

# Restore
psql otp_service < backup.sql
```

### Log Analysis

```bash
# View application logs
tail -f logs/app.log

# Check API usage
grep "POST /send-otp" logs/app.log | wc -l
```

---

## Performance Optimization

### Database Indexing

```sql
-- Add indexes for common queries
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_otp_email ON otp_verifications(email);
CREATE INDEX idx_otp_verified ON otp_verifications(verified);
```

### Caching

```python
# Add Redis caching
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_verification_status_cached(email: str):
    # Cached verification status
    pass
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/send-otp")
@limiter.limit("5/minute")
async def send_otp(...):
    # Limit to 5 requests per minute
    pass
```

---

## Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Find and kill process on port 8000
# Linux/macOS:
lsof -i :8000
kill -9 <PID>

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**SMTP Authentication Failed**
- Check SMTP_EMAIL and SMTP_PASSWORD
- For Gmail, use App Passwords, not the account password
- Enable "Less secure app access" if needed

**Database Connection Error**
- Verify DATABASE_URL format
- Check PostgreSQL is running
- Verify credentials

**Module Not Found**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## Scaling Considerations

### Horizontal Scaling
- Deploy multiple instances behind load balancer
- Use PostgreSQL instead of SQLite
- Add caching layer (Redis)

### Database Optimization
- Add connection pooling
- Use read replicas
- Archive old OTP records

### API Optimization
- Add rate limiting
- Implement request caching
- Use CDN for static content

---

## Security Checklist

Before production deployment:

- [ ] Change default API_KEY to strong random value
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS/SSL
- [ ] Setup CORS for specific origins
- [ ] Enable request rate limiting
- [ ] Add request validation
- [ ] Setup monitoring and alerts
- [ ] Regular security updates
- [ ] Database backups
- [ ] API authentication logging

---

## Support & Resources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Railway Documentation](https://docs.railway.app/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [AWS EC2 Guide](https://docs.aws.amazon.com/ec2/)
