# 🔧 Railway Deployment Fix

## The Problem
Railway couldn't detect which app to build because it saw both `backend/` and `frontend/` folders.

## The Solution
Deploy backend and frontend as **separate services** with specific root directories.

---

## 🚀 Step-by-Step Fix

### 1. Delete Current Deployment
1. Go to your Railway project
2. Click on the failed service
3. Go to **Settings** → scroll down → **Delete Service**

### 2. Deploy Backend First

1. Click **"New Service"** in your project
2. Select **"GitHub Repo"**
3. Choose: `TickTracker2.0`
4. **CRITICAL:** Click **"Settings"** → **"Service"** → Set **Root Directory** to:
   ```
   ticktracker/backend
   ```
5. Go to **"Variables"** tab and add:
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
   CORS_ORIGINS=*
   ```
6. Go to **"Deployments"** tab - it should auto-deploy
7. Wait for "Success" status (~2-3 minutes)
8. Go to **"Settings"** → **"Networking"** → Click **"Generate Domain"**
9. **Copy your backend URL** (e.g., `https://web-production-abc123.up.railway.app`)

### 3. Deploy Frontend Second

1. Click **"New Service"** in the same project
2. Select **"GitHub Repo"**
3. Choose: `TickTracker2.0` (same repo)
4. **CRITICAL:** Click **"Settings"** → **"Service"** → Set **Root Directory** to:
   ```
   ticktracker/frontend
   ```
5. Go to **"Variables"** tab and add:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url-from-step-2.up.railway.app
   ```
   (Replace with your actual backend URL from step 2.9)
6. Go to **"Deployments"** tab - it should auto-deploy
7. Wait for "Success" status (~3-4 minutes)
8. Go to **"Settings"** → **"Networking"** → Click **"Generate Domain"**
9. **Copy your frontend URL**

### 4. Update Backend CORS

1. Go back to your **backend service**
2. Go to **"Variables"** tab
3. Update `CORS_ORIGINS` to:
   ```
   CORS_ORIGINS=https://your-frontend-url.up.railway.app
   ```
   (Replace with your actual frontend URL from step 3.9)
4. Backend will auto-redeploy (~1 minute)

### 5. Test Your App! 🎉

Visit your frontend URL and test:
- Search for events
- View event details
- Check if API calls work

---

## 📸 Visual Guide

### Setting Root Directory:
```
Project → Service → Settings → Service Settings → Root Directory
```

### Generating Domain:
```
Service → Settings → Networking → Generate Domain
```

---

## 🐛 Still Having Issues?

### Backend Build Fails:
- Check that Root Directory is exactly: `ticktracker/backend`
- Verify all environment variables are set
- Check build logs for specific errors

### Frontend Build Fails:
- Check that Root Directory is exactly: `ticktracker/frontend`
- Verify `NEXT_PUBLIC_API_URL` is set
- Check build logs for specific errors

### CORS Errors:
- Make sure `CORS_ORIGINS` in backend includes your frontend URL
- No trailing slashes in URLs
- Use https:// not http://

### Can't Connect to Backend:
- Verify backend has a generated domain
- Check `NEXT_PUBLIC_API_URL` matches backend domain exactly
- Open browser dev tools → Network tab to see actual errors

---

## 💡 Pro Tips

1. **Name your services** - Click service name to rename (e.g., "Backend API", "Frontend")
2. **Watch logs** - Go to Deployments → Click deployment → View logs
3. **Environment variables** - Changes trigger auto-redeploy
4. **Free tier** - You get $5 credit/month, should be enough for testing

---

## ✅ Success Checklist

- [ ] Backend service created with root directory `ticktracker/backend`
- [ ] Backend has all environment variables
- [ ] Backend deployed successfully
- [ ] Backend domain generated
- [ ] Frontend service created with root directory `ticktracker/frontend`
- [ ] Frontend has `NEXT_PUBLIC_API_URL` variable
- [ ] Frontend deployed successfully
- [ ] Frontend domain generated
- [ ] Backend CORS updated with frontend URL
- [ ] App works when visiting frontend URL

---

## 🆘 Need More Help?

Share the error from your build logs and I can help debug!
