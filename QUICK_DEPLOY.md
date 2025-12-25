# Quick Deploy Reference

## 🚀 Fastest Way to Deploy

### Option 1: Railway.app (5 minutes)

1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub"
3. Connect your repo
4. Railway auto-detects and deploys both services
5. Add environment variables in dashboard
6. Get your URLs and you're live!

**Cost:** Free tier available, then $5/month per service

---

### Option 2: VPS with Script (15 minutes)

```bash
# 1. Get a server (DigitalOcean, Linode, etc.)
# 2. Point your domain to server IP
# 3. SSH into server

# 4. Clone your repo
git clone your-repo-url /var/www/ticktracker
cd /var/www/ticktracker

# 5. Run deployment script
./deploy.sh server
sudo ./deploy.sh systemd
sudo ./deploy.sh nginx yourdomain.com

# 6. Setup SSL
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com

# 7. Create .env file
nano ticktracker/backend/.env
# Add your API keys

# Done! Visit https://yourdomain.com
```

**Cost:** $6-12/month

---

### Option 3: Docker (10 minutes)

```bash
# 1. Install Docker on your server
curl -fsSL https://get.docker.com | sh

# 2. Clone repo
git clone your-repo-url ticktracker
cd ticktracker

# 3. Create .env file
cp ticktracker/backend/.env.example .env
# Edit .env with your API keys

# 4. Deploy
docker-compose up -d

# Done! App running on http://your-server-ip:3000
```

---

## 🔑 Required Environment Variables

Create `.env` file with:
```bash
TICKETMASTER_API_KEY=your_key
SEATGEEK_CLIENT_ID=your_key
EVENTBRITE_PRIVATE_TOKEN=your_key
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

---

## 🛠️ Common Commands

```bash
# Check service status
sudo systemctl status ticktracker-backend
sudo systemctl status ticktracker-frontend

# View logs
sudo journalctl -u ticktracker-backend -f
sudo journalctl -u ticktracker-frontend -f

# Restart services
sudo systemctl restart ticktracker-backend
sudo systemctl restart ticktracker-frontend

# Update app
./deploy.sh update

# Docker commands
docker-compose up -d          # Start
docker-compose down           # Stop
docker-compose logs -f        # View logs
docker-compose restart        # Restart
```

---

## 🌐 DNS Setup

Point these records to your server IP:

| Type | Name | Value |
|------|------|-------|
| A | @ | your.server.ip |
| A | www | your.server.ip |
| A | api | your.server.ip |

---

## ✅ Post-Deploy Checklist

- [ ] SSL certificate installed (https working)
- [ ] API keys configured in .env
- [ ] Frontend can reach backend API
- [ ] CORS configured for your domain
- [ ] Database file has write permissions
- [ ] Services auto-start on reboot
- [ ] Firewall allows ports 80, 443
- [ ] Backups configured

---

## 🆘 Troubleshooting

**502 Bad Gateway:**
```bash
sudo systemctl status ticktracker-backend
sudo systemctl status ticktracker-frontend
```

**CORS errors:**
Update `ticktracker/backend/main.py`:
```python
allow_origins=["https://yourdomain.com"]
```

**Can't connect to API:**
Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`

---

## 📊 Recommended Setup

**For beginners:** Railway.app  
**For control:** VPS + deploy.sh script  
**For scalability:** Docker + VPS  

**Best combo:** Vercel (frontend) + Railway (backend) = $5/month
