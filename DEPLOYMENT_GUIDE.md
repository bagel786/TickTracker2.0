# TickTracker Deployment Guide

This guide covers deploying your FastAPI backend + Next.js frontend to production.

## Quick Overview

Your app has two parts:
- **Backend**: FastAPI (Python) on port 8000
- **Frontend**: Next.js (Node.js) on port 3000

## Deployment Options

### Option 1: VPS (DigitalOcean, Linode, AWS EC2) - Recommended for Full Control

#### Prerequisites
- Ubuntu 22.04 server with SSH access
- Domain name pointed to your server IP
- Root or sudo access

#### Step 1: Server Setup

```bash
# SSH into your server
ssh root@your-server-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11+
sudo apt install python3 python3-pip python3-venv -y

# Install Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Install Nginx
sudo apt install nginx -y

# Install Certbot for SSL
sudo apt install certbot python3-certbot-nginx -y
```

#### Step 2: Upload Your Code

```bash
# On your local machine, from project root
rsync -avz --exclude 'node_modules' --exclude '__pycache__' --exclude '.next' \
  ./ root@your-server-ip:/var/www/ticktracker/
```

Or use Git:
```bash
# On server
cd /var/www
git clone your-repo-url ticktracker
cd ticktracker
```

#### Step 3: Setup Backend

```bash
cd /var/www/ticktracker/ticktracker/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
cat > .env << EOF
DATABASE_URL=sqlite:///./ticktracker.db
TICKETMASTER_API_KEY=your_key_here
TICKETMASTER_SECRET=your_secret_here
EVENTBRITE_PRIVATE_TOKEN=your_token_here
SEATGEEK_CLIENT_ID=your_client_id_here
SEATGEEK_CLIENT_SECRET=your_secret_here
EOF

# Test backend
uvicorn main:app --host 0.0.0.0 --port 8000
# Press Ctrl+C after confirming it works
```

#### Step 4: Setup Frontend

```bash
cd /var/www/ticktracker/ticktracker/frontend

# Install dependencies
npm install

# Update API endpoint for production
# Edit app/lib/api.ts or wherever your API base URL is defined
# Change from http://localhost:8000 to https://api.yourdomain.com

# Build for production
npm run build

# Test production build
npm start
# Press Ctrl+C after confirming it works
```

#### Step 5: Create Systemd Services

**Backend Service:**
```bash
sudo nano /etc/systemd/system/ticktracker-backend.service
```

Paste this:
```ini
[Unit]
Description=TickTracker FastAPI Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/ticktracker/ticktracker/backend
Environment="PATH=/var/www/ticktracker/ticktracker/backend/venv/bin"
ExecStart=/var/www/ticktracker/ticktracker/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Frontend Service:**
```bash
sudo nano /etc/systemd/system/ticktracker-frontend.service
```

Paste this:
```ini
[Unit]
Description=TickTracker Next.js Frontend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/ticktracker/ticktracker/frontend
Environment="NODE_ENV=production"
Environment="PORT=3000"
ExecStart=/usr/bin/npm start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start services:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable ticktracker-backend
sudo systemctl enable ticktracker-frontend
sudo systemctl start ticktracker-backend
sudo systemctl start ticktracker-frontend

# Check status
sudo systemctl status ticktracker-backend
sudo systemctl status ticktracker-frontend
```

#### Step 6: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/ticktracker
```

Paste this configuration:
```nginx
# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Frontend
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable site and restart Nginx:**
```bash
sudo ln -s /etc/nginx/sites-available/ticktracker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 7: Setup SSL with Let's Encrypt

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com
```

Follow the prompts. Certbot will automatically configure SSL and set up auto-renewal.

#### Step 8: Update Frontend API URL

Edit your frontend API configuration to use the production API URL:

```bash
cd /var/www/ticktracker/ticktracker/frontend
```

Find where you define the API base URL (likely in `app/lib/api.ts` or similar) and update it to:
```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api.yourdomain.com';
```

Or create a `.env.local` file:
```bash
echo "NEXT_PUBLIC_API_URL=https://api.yourdomain.com" > .env.local
```

Rebuild and restart:
```bash
npm run build
sudo systemctl restart ticktracker-frontend
```

---

### Option 2: Platform-as-a-Service (Easier but Less Control)

#### Railway.app (Recommended for Beginners)

1. **Sign up at [railway.app](https://railway.app)**

2. **Deploy Backend:**
   - Create new project
   - Deploy from GitHub or upload code
   - Add environment variables in Railway dashboard
   - Railway will auto-detect FastAPI and deploy
   - Note your backend URL (e.g., `https://ticktracker-backend.up.railway.app`)

3. **Deploy Frontend:**
   - Create another service in same project
   - Add environment variable: `NEXT_PUBLIC_API_URL=your-backend-url`
   - Railway will auto-detect Next.js and deploy

4. **Add Custom Domain:**
   - Go to Settings → Domains
   - Add your domain and update DNS records

#### Render.com

Similar to Railway:
1. Create Web Service for backend (Python)
2. Create Web Service for frontend (Node)
3. Link them via environment variables
4. Add custom domain

#### Vercel (Frontend) + Railway/Render (Backend)

1. **Deploy Frontend to Vercel:**
   ```bash
   cd ticktracker/frontend
   npm install -g vercel
   vercel
   ```
   - Add environment variable: `NEXT_PUBLIC_API_URL`

2. **Deploy Backend to Railway/Render** (see above)

---

### Option 3: Docker Deployment

Create these files in your project root:

**Backend Dockerfile:**
```dockerfile
# ticktracker/backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile:**
```dockerfile
# ticktracker/frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

CMD ["npm", "start"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  backend:
    build: ./ticktracker/backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./ticktracker.db
      - TICKETMASTER_API_KEY=${TICKETMASTER_API_KEY}
      - SEATGEEK_CLIENT_ID=${SEATGEEK_CLIENT_ID}
    volumes:
      - ./data:/app/data

  frontend:
    build: ./ticktracker/frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend
```

Deploy with:
```bash
docker-compose up -d
```

---

## Post-Deployment Checklist

- [ ] Update CORS settings in backend to only allow your domain
- [ ] Move API keys to environment variables (remove from settings.py)
- [ ] Set up database backups
- [ ] Configure monitoring (UptimeRobot, etc.)
- [ ] Test all API endpoints
- [ ] Test frontend functionality
- [ ] Set up error logging (Sentry)
- [ ] Configure firewall (UFW on Ubuntu)
- [ ] Set up automated backups for SQLite database

## Security Hardening

```bash
# Update CORS in main.py to restrict origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com", "https://www.yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Monitoring & Logs

```bash
# View backend logs
sudo journalctl -u ticktracker-backend -f

# View frontend logs
sudo journalctl -u ticktracker-frontend -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Updating Your App

```bash
# Pull latest code
cd /var/www/ticktracker
git pull

# Update backend
cd ticktracker/backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart ticktracker-backend

# Update frontend
cd ../frontend
npm install
npm run build
sudo systemctl restart ticktracker-frontend
```

## Troubleshooting

**Backend won't start:**
```bash
sudo systemctl status ticktracker-backend
sudo journalctl -u ticktracker-backend -n 50
```

**Frontend won't start:**
```bash
sudo systemctl status ticktracker-frontend
sudo journalctl -u ticktracker-frontend -n 50
```

**502 Bad Gateway:**
- Check if services are running: `sudo systemctl status ticktracker-*`
- Check Nginx config: `sudo nginx -t`
- Check firewall: `sudo ufw status`

## Cost Estimates

- **VPS (DigitalOcean/Linode)**: $6-12/month for basic droplet
- **Railway.app**: $5/month per service (free tier available)
- **Render.com**: Free tier available, paid starts at $7/month
- **Vercel**: Free for frontend, unlimited bandwidth
- **Domain**: $10-15/year

## Recommended Setup for Production

**Best Balance (Cost vs Control):**
- Frontend: Vercel (free, fast CDN)
- Backend: Railway.app ($5/month, easy management)
- Database: Upgrade to PostgreSQL on Railway
- Domain: Namecheap/Cloudflare

**Total: ~$5-10/month**
