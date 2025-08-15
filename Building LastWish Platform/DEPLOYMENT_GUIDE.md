# LastWish.eth Deployment Guide

## Overview

This guide covers deploying the LastWish.eth Web3 estate planning platform to various environments, from local development to production deployment on decentralized infrastructure.

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Production Deployment](#production-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Decentralized Deployment (IPFS/ICP)](#decentralized-deployment)
5. [ENS Domain Configuration](#ens-domain-configuration)
6. [Environment Configuration](#environment-configuration)
7. [Database Setup](#database-setup)
8. [Monitoring and Logging](#monitoring-and-logging)
9. [Security Considerations](#security-considerations)
10. [Troubleshooting](#troubleshooting)

## Local Development Setup

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Git**
- **WalletConnect Project ID** from [WalletConnect Cloud](https://cloud.walletconnect.com/)

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/lastwish-eth.git
cd lastwish-eth
```

### 2. Backend Setup

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your configuration
```

### 3. Frontend Setup

```bash
cd lastwish-frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env
# Edit .env with your configuration
```

### 4. Database Initialization

```bash
cd src
python main.py
# Database tables will be created automatically
```

### 5. Start Development Servers

**Terminal 1 - Backend:**
```bash
cd src
python main.py
# Backend runs on http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd lastwish-frontend
npm run dev
# Frontend runs on http://localhost:5173
```

### 6. Verify Setup

- Frontend: http://localhost:5173
- Backend API: http://localhost:5000/api/health
- Test wallet connection functionality

## Production Deployment

### Option 1: Traditional Cloud Hosting

#### 1. Prepare Production Build

```bash
# Build frontend
cd lastwish-frontend
npm run build

# Copy to backend static directory
cp -r dist/* ../src/static/
```

#### 2. Configure Production Environment

```bash
# Set production environment variables
export FLASK_ENV=production
export SECRET_KEY=your-secure-secret-key
export WALLETCONNECT_PROJECT_ID=your-project-id
export DATABASE_URL=postgresql://user:pass@host:port/dbname
```

#### 3. Deploy to Cloud Provider

**AWS/DigitalOcean/Heroku:**
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name lastwish.eth;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static {
        alias /path/to/lastwish-eth/src/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Option 2: Serverless Deployment

#### Vercel Deployment

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy frontend
cd lastwish-frontend
vercel --prod

# Deploy backend (separate service)
cd ../src
vercel --prod
```

#### Netlify Deployment

```bash
# Build frontend
cd lastwish-frontend
npm run build

# Deploy to Netlify
netlify deploy --prod --dir=dist
```

## Docker Deployment

### 1. Create Dockerfile

```dockerfile
# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY lastwish-frontend/dist/ ./src/static/

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.main:app"]
```

### 2. Create Docker Compose

```yaml
version: '3.8'

services:
  lastwish-app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - WALLETCONNECT_PROJECT_ID=${WALLETCONNECT_PROJECT_ID}
      - DATABASE_URL=postgresql://postgres:password@db:5432/lastwish
    depends_on:
      - db
    volumes:
      - ./data:/app/data

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=lastwish
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - lastwish-app

volumes:
  postgres_data:
```

### 3. Deploy with Docker

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Scale application
docker-compose up -d --scale lastwish-app=3
```

## Decentralized Deployment

### IPFS Deployment

#### 1. Prepare Static Build

```bash
# Build frontend for IPFS
cd lastwish-frontend
npm run build

# Optimize for IPFS
# Ensure all paths are relative
# Remove absolute URLs
```

#### 2. Deploy to IPFS

```bash
# Install IPFS CLI
# https://docs.ipfs.io/install/

# Add to IPFS
ipfs add -r dist/

# Pin to ensure availability
ipfs pin add QmYourHashHere

# Update DNS with IPFS hash
# _dnslink.lastwish.eth TXT "dnslink=/ipfs/QmYourHashHere"
```

#### 3. Configure IPFS Gateway

```javascript
// Update API base URL for IPFS
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://api.lastwish.eth'  // Separate API service
  : 'http://localhost:5000';
```

### Internet Computer (ICP) Deployment

#### 1. Install DFX

```bash
# Install DFX (Internet Computer SDK)
sh -ci "$(curl -fsSL https://sdk.dfinity.org/install.sh)"
```

#### 2. Configure for ICP

```bash
# Initialize ICP project
dfx new lastwish-icp
cd lastwish-icp

# Copy frontend build
cp -r ../lastwish-frontend/dist/* src/lastwish_frontend/assets/
```

#### 3. Deploy to ICP

```bash
# Start local replica (development)
dfx start --background

# Deploy locally
dfx deploy

# Deploy to mainnet
dfx deploy --network ic
```

## ENS Domain Configuration

### 1. Register ENS Domain

```bash
# Use ENS Manager or programmatically
# https://app.ens.domains/
```

### 2. Configure DNS Records

```bash
# A Record (for traditional hosting)
lastwish.eth A 192.168.1.100

# CNAME Record (for cloud hosting)
lastwish.eth CNAME your-app.herokuapp.com

# IPFS Content Hash (for decentralized hosting)
# Set content hash to IPFS hash in ENS manager
```

### 3. Configure Subdomains

```bash
# API subdomain
api.lastwish.eth CNAME api-service.herokuapp.com

# Documentation
docs.lastwish.eth CNAME lastwish-docs.netlify.app

# Test environment
test.lastwish.eth CNAME test-lastwish.vercel.app
```

## Environment Configuration

### Production Environment Variables

```bash
# Flask Configuration
SECRET_KEY=your-super-secure-secret-key-here
FLASK_ENV=production
FLASK_DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# WalletConnect
WALLETCONNECT_PROJECT_ID=your-walletconnect-project-id

# Blockchain RPC URLs
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_INFURA_KEY
POLYGON_RPC_URL=https://polygon-rpc.com/
BSC_RPC_URL=https://bsc-dataseed.binance.org/
AVALANCHE_RPC_URL=https://api.avax.network/ext/bc/C/rpc

# NLWeb Integration
NLWEB_API_KEY=your-nlweb-api-key
NLWEB_API_BASE=https://your-nlweb-instance.com

# Security
CORS_ORIGINS=https://lastwish.eth,https://www.lastwish.eth
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# Monitoring
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO

# Email (for notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Payment Processing
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### Frontend Environment Variables

```bash
# API Configuration
REACT_APP_API_BASE_URL=https://api.lastwish.eth

# WalletConnect
REACT_APP_WALLETCONNECT_PROJECT_ID=your-project-id

# Blockchain Configuration
REACT_APP_ETHEREUM_RPC=https://mainnet.infura.io/v3/YOUR_INFURA_KEY
REACT_APP_POLYGON_RPC=https://polygon-rpc.com/
REACT_APP_BSC_RPC=https://bsc-dataseed.binance.org/
REACT_APP_AVALANCHE_RPC=https://api.avax.network/ext/bc/C/rpc

# Analytics
REACT_APP_GOOGLE_ANALYTICS_ID=GA-XXXXXXXXX
REACT_APP_MIXPANEL_TOKEN=your-mixpanel-token

# Feature Flags
REACT_APP_ENABLE_CRYPTO_FEATURES=true
REACT_APP_ENABLE_AI_FEATURES=true
REACT_APP_ENABLE_PAYMENTS=true
```

## Database Setup

### PostgreSQL Production Setup

```sql
-- Create database
CREATE DATABASE lastwish_production;

-- Create user
CREATE USER lastwish_user WITH PASSWORD 'secure_password';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE lastwish_production TO lastwish_user;

-- Connect to database
\c lastwish_production;

-- Grant schema permissions
GRANT ALL ON SCHEMA public TO lastwish_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO lastwish_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO lastwish_user;
```

### Database Migration

```bash
# Install Flask-Migrate
pip install Flask-Migrate

# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

### Database Backup

```bash
# Backup database
pg_dump -h localhost -U lastwish_user -d lastwish_production > backup.sql

# Restore database
psql -h localhost -U lastwish_user -d lastwish_production < backup.sql

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U lastwish_user -d lastwish_production > "backup_$DATE.sql"
aws s3 cp "backup_$DATE.sql" s3://your-backup-bucket/
```

## Monitoring and Logging

### Application Monitoring

```python
# Install monitoring tools
pip install sentry-sdk flask-monitoring-dashboard

# Configure Sentry
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

### Log Configuration

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/lastwish.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('LastWish.eth startup')
```

### Health Checks

```python
@app.route('/health')
def health_check():
    """Comprehensive health check"""
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        
        # Check external services
        # ... additional checks
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0',
            'database': 'connected',
            'services': 'operational'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500
```

## Security Considerations

### SSL/TLS Configuration

```bash
# Obtain SSL certificate (Let's Encrypt)
sudo certbot --nginx -d lastwish.eth -d www.lastwish.eth

# Configure automatic renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Security Headers

```python
from flask_talisman import Talisman

# Configure security headers
Talisman(app, {
    'force_https': True,
    'strict_transport_security': True,
    'content_security_policy': {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline' https://cdn.walletconnect.com",
        'style-src': "'self' 'unsafe-inline'",
        'img-src': "'self' data: https:",
        'connect-src': "'self' https://api.walletconnect.com wss://relay.walletconnect.com"
    }
})
```

### Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per hour"]
)

@app.route('/api/auth/wallet-connect', methods=['POST'])
@limiter.limit("10 per minute")
def wallet_connect():
    # ... implementation
```

### Input Validation

```python
from marshmallow import Schema, fields, validate

class WalletConnectSchema(Schema):
    address = fields.Str(required=True, validate=validate.Regexp(r'^0x[a-fA-F0-9]{40}$'))
    network = fields.Str(required=True, validate=validate.OneOf(['ethereum', 'polygon', 'bsc', 'avalanche']))
    ens_domain = fields.Str(validate=validate.Regexp(r'^[a-zA-Z0-9-]+\.eth$'))
```

## Troubleshooting

### Common Issues

#### 1. WalletConnect Not Loading

```bash
# Check project ID configuration
echo $REACT_APP_WALLETCONNECT_PROJECT_ID

# Verify network connectivity
curl -I https://cdn.walletconnect.com/

# Check browser console for errors
# Ensure CORS is properly configured
```

#### 2. Database Connection Issues

```bash
# Test database connection
python -c "
import psycopg2
conn = psycopg2.connect('postgresql://user:pass@host:port/db')
print('Database connection successful')
"

# Check database logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

#### 3. Frontend Build Issues

```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check for version conflicts
npm ls

# Build with verbose output
npm run build -- --verbose
```

#### 4. SSL Certificate Issues

```bash
# Check certificate status
sudo certbot certificates

# Renew certificate manually
sudo certbot renew --dry-run

# Check nginx configuration
sudo nginx -t
```

### Performance Optimization

#### Database Optimization

```sql
-- Add indexes for common queries
CREATE INDEX idx_user_wallet_address ON users(wallet_address);
CREATE INDEX idx_assets_user_id ON assets(user_id);
CREATE INDEX idx_beneficiaries_user_id ON beneficiaries(user_id);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM assets WHERE user_id = 1;
```

#### Frontend Optimization

```bash
# Analyze bundle size
npm run build -- --analyze

# Optimize images
npm install imagemin imagemin-webp

# Enable gzip compression in nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

#### Caching Strategy

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@app.route('/api/estate/dashboard')
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_dashboard():
    # ... implementation
```

### Monitoring Commands

```bash
# Check application status
curl -f http://localhost:5000/health || echo "Application down"

# Monitor logs
tail -f logs/lastwish.log

# Check resource usage
htop
df -h
free -m

# Monitor database
psql -c "SELECT * FROM pg_stat_activity;"

# Check SSL certificate expiry
echo | openssl s_client -servername lastwish.eth -connect lastwish.eth:443 2>/dev/null | openssl x509 -noout -dates
```

## Support

For deployment support:

- **Documentation**: [https://docs.lastwish.eth](https://docs.lastwish.eth)
- **GitHub Issues**: [https://github.com/lastwish-eth/issues](https://github.com/lastwish-eth/issues)
- **Discord**: [https://discord.gg/lastwish](https://discord.gg/lastwish)
- **Email**: devops@lastwish.eth

## Changelog

### v1.0.0 (2024-01-01)
- Initial production release
- Web3 wallet integration
- Estate planning features
- AI-powered assistance
- Subscription management
- Decentralized deployment support

