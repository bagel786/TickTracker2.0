# 🚂 Railway Deployment Checklist

## ✅ Pre-Deployment (Done!)
- [x] API keys secured in environment variables
- [x] Code pushed to GitHub
- [x] .env file excluded from git
- [x] CORS configuration ready
- [x] Deployment guides created

---

## 🚀 Deploy to Railway (15 minutes)

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Authorize Railway to access your repos

### Step 2: Deploy Backend
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repo: `TickTracker2.0`
4. **IMPORTANT:** Set **Root Directory** to: `ticktracker/backend`
5. Railway will detect it's a Python app
6. Click **"Add variables"** and add these:

```
TICKETMASTER_API_KEY=wAuWTTAqVrinFxhiIICRxvBwi9yGITx8
TICKETMASTER_SECRET=O6FS15jiQfB0kRS7
EVENTBRITE_API_KEY=QLG3DZ2MCKEKDPPJ2F
EVENTBRITE_CLIENT_SECRET=PBT7A4BOO6JP62LBW6NBLVMKDNVUFQ5GNXURBL7IUHQOXALLRK
EVENTBRITE_PRIVATE_TOKEN=CGNUNTMTDEFCPGVZMORP
EVENTBRITE_PUBLIC_TOKEN=ZDSNSVD4JID5ZI24DXEV
SEATGEEK_CLIENT_ID=NTQ1NDE0ODN8MTc2Mzg0NTI3OC43MjQ0OTE4
SEATGEEK_CLIENT_SECRET=e81000383a0cb87a6d01f008b34d7e3dfea876c973ddbab5c1f2543edacac2c9
DATABASE_URL=sqlite:///./ticktracker.db
```

6. Set **Root Directory** to: `ticktracker/backend`
6. Click **"Deploy"** (or it may auto-deploy)
7. Wait for build to complete (~2-3 minutes)
8. Once deployed, click **"Settings"** → **"Networking"** → **"Generate Domain"**
9. Copy your backend URL (e.g., `https://ticktracker-backend.up.railway.app`)

### Step 3: Deploy Frontend
1. In same project, click **"New Service"** → **"GitHub Repo"**
2. Select the same repo: `TickTracker2.0`
3. **IMPORTANT:** Set **Root Directory** to: `ticktracker/frontend`
4. Railway will detect it's a Node.js app
5. Click **"Add variables"** and add:

```
NEXT_PUBLIC_API_URL=https://your-backend-url.up.railway.app
```
(Replace with your actual backend URL from Step 2)

5. Set **Root Directory** to: `ticktracker/frontend`
6. Click **"Deploy"** (or it may auto-deploy)
7. Wait for build (~3-4 minutes)
8. Once deployed, click **"Settings"** → **"Networking"** → **"Generate Domain"**
9. Copy your frontend URL

### Step 4: Update CORS
1. Go back to backend service
2. Add environment variable:
```
CORS_ORIGINS=https://your-frontend-url.up.railway.app
```
3. Backend will auto-redeploy

### Step 5: Add Custom Domain (Optional)
1. Click on frontend service
2. Go to **Settings** → **Domains**
3. Click **"Custom Domain"**
4. Enter your domain (e.g., `ticktracker.com`)
5. Update your DNS records as shown
6. Wait for SSL certificate (~5 minutes)

### Step 6: Update Backend CORS for Custom Domain
If you added a custom domain:
```
CORS_ORIGINS=https://ticktracker.com,https://www.ticktracker.com
```

---

## 📊 Railway Analytics - What You Get

### Built-in Metrics (Free):
- ✅ **Request count** - Total HTTP requests
- ✅ **Response time** - Average latency
- ✅ **CPU usage** - Server load
- ✅ **Memory usage** - RAM consumption
- ✅ **Network traffic** - Bandwidth usage
- ✅ **Build logs** - Deployment history
- ✅ **Application logs** - Real-time logs

### To View Metrics:
1. Click on your service
2. Go to **"Metrics"** tab
3. View real-time graphs

### What Railway DOESN'T Track:
- ❌ Individual user sessions
- ❌ User behavior/page views
- ❌ Demographics
- ❌ Conversion funnels

**For user analytics, see:** `RAILWAY_ANALYTICS_GUIDE.md`

---

## 🎯 Recommended: Add Google Analytics

Quick setup for user tracking:

1. Get Google Analytics ID from [analytics.google.com](https://analytics.google.com)
2. Add to Railway frontend environment variables:
```
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```
3. I can add the code integration - just ask!

---

## 💰 Pricing

### Free Tier:
- $5 credit per month
- Enough for small projects
- No credit card required

### Paid Plans:
- **Hobby**: $5/month per service
- **Pro**: $20/month (team features)

### Your App Cost:
- Backend: ~$5/month
- Frontend: ~$5/month
- **Total: ~$10/month** (or free tier if low traffic)

---

## 🔍 Monitoring & Logs

### View Logs:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# View logs
railway logs
```

Or view in dashboard:
1. Click on service
2. Go to **"Deployments"** tab
3. Click on latest deployment
4. View build and runtime logs

---

## 🚨 Troubleshooting

### Backend won't start:
- Check environment variables are set
- View logs in Railway dashboard
- Ensure `requirements.txt` is in backend folder

### Frontend can't reach backend:
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check CORS_ORIGINS includes frontend URL
- View network tab in browser dev tools

### Database issues:
- SQLite works but consider upgrading to PostgreSQL
- Railway offers free PostgreSQL database
- Add as new service, get connection URL

---

## 🎉 Post-Deployment

Once deployed, test:
- [ ] Visit your frontend URL
- [ ] Search for events
- [ ] Check if API calls work
- [ ] View Railway metrics
- [ ] Set up custom domain (optional)
- [ ] Add Google Analytics (recommended)
- [ ] Share with users!

---

## 📈 Next Steps

1. **Monitor usage** - Check Railway metrics daily
2. **Add analytics** - Install Google Analytics for user tracking
3. **Upgrade database** - Move from SQLite to PostgreSQL for production
4. **Set up alerts** - Get notified of errors
5. **Add monitoring** - Consider Sentry for error tracking
6. **Scale up** - Upgrade plan if you get traffic

---

## 🆘 Need Help?

- Railway Docs: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Your deployment guides: `DEPLOYMENT_GUIDE.md`
- Analytics setup: `RAILWAY_ANALYTICS_GUIDE.md`

---

## 🎊 You're Ready!

Your code is secured and pushed to GitHub. Now just follow the steps above to deploy to Railway in ~15 minutes!

**Quick Start:**
1. Go to [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Add environment variables
4. Deploy!
