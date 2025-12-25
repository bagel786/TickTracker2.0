# 🎯 Railway Root Directory - Exact Steps

## Where to Find Root Directory Setting

### Method 1: During Initial Setup (Recommended)

When you first add a service from GitHub:

1. Click **"New Service"**
2. Select **"GitHub Repo"**
3. Choose your repo: **TickTracker2.0**
4. **BEFORE clicking Deploy**, look for a section that says:
   - **"Root Directory"** or
   - **"Source"** or
   - **"Build Settings"**
5. Click on it and enter: `ticktracker/backend` (or `ticktracker/frontend`)
6. Then click **"Deploy"**

### Method 2: After Service is Created

If you already created the service:

1. Click on your service name in Railway
2. Click the **"Settings"** tab (top navigation)
3. Scroll down to find **"Source"** or **"Build"** section
4. Look for **"Root Directory"** field
5. Enter: `ticktracker/backend` (or `ticktracker/frontend`)
6. Changes save automatically and trigger redeploy

---

## 🚨 Can't Find It? Try This Alternative

If Railway's UI doesn't show the Root Directory option, you can specify it in the repo itself (which I already did!):

### The files I created will work automatically:
- `ticktracker/backend/railway.toml` ✅
- `ticktracker/backend/nixpacks.toml` ✅
- `ticktracker/frontend/railway.toml` ✅
- `ticktracker/frontend/nixpacks.toml` ✅

### So here's the EASIER way:

## 🎯 Easiest Method - Use Monorepo Detection

Railway should now auto-detect the services! Try this:

### Step 1: Delete Failed Service
1. Go to your Railway project
2. Click the failed service
3. Settings → Scroll to bottom → **"Remove Service from Project"**

### Step 2: Let Railway Auto-Detect

1. Click **"New Service"**
2. Click **"GitHub Repo"**
3. Select **TickTracker2.0**
4. Railway should now show: **"Multiple services detected"**
5. It should list:
   - `ticktracker/backend` (Python)
   - `ticktracker/frontend` (Node.js)
6. Select **backend** first
7. Click **"Add Service"**

### Step 3: Add Environment Variables to Backend

1. Click on the backend service
2. Go to **"Variables"** tab
3. Click **"New Variable"** and add each one:

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

4. Service will auto-deploy

### Step 4: Generate Backend Domain

1. Stay in backend service
2. Go to **"Settings"** tab
3. Find **"Networking"** section
4. Click **"Generate Domain"**
5. **Copy the URL** (you'll need it for frontend)

### Step 5: Add Frontend Service

1. Go back to project view (click project name at top)
2. Click **"New Service"**
3. Click **"GitHub Repo"**
4. Select **TickTracker2.0** again
5. This time select **frontend**
6. Click **"Add Service"**

### Step 6: Add Frontend Environment Variable

1. Click on frontend service
2. Go to **"Variables"** tab
3. Add one variable:
```
NEXT_PUBLIC_API_URL=https://your-backend-url-from-step-4.up.railway.app
```
(Replace with your actual backend URL)

4. Service will auto-deploy

### Step 7: Generate Frontend Domain

1. Stay in frontend service
2. Go to **"Settings"** tab
3. Find **"Networking"** section
4. Click **"Generate Domain"**
5. **Copy the URL** - this is your app!

### Step 8: Update Backend CORS

1. Go back to backend service
2. Go to **"Variables"** tab
3. Find `CORS_ORIGINS` variable
4. Click to edit it
5. Change from `*` to your frontend URL:
```
CORS_ORIGINS=https://your-frontend-url.up.railway.app
```
6. Backend will auto-redeploy

---

## 🎉 Done!

Visit your frontend URL and your app should work!

---

## 🆘 Still Not Working?

### If Railway doesn't show "Multiple services detected":

Try deploying with a direct path in the service name:

1. When creating service, after selecting the repo
2. Look for **"Service Name"** field
3. Name it: `backend` or `frontend`
4. Railway might then ask for the path

### Or use Railway CLI:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Deploy backend
cd ticktracker/backend
railway up

# Deploy frontend (in new terminal)
cd ticktracker/frontend
railway up
```

---

## 📸 What You're Looking For

The Root Directory setting might be labeled as:
- **"Root Directory"**
- **"Source Directory"**
- **"Working Directory"**
- **"Build Path"**
- **"Service Root"**

It's usually in:
- Settings → Source section
- Settings → Build section
- Initial setup wizard

---

## 💡 Current Railway UI (as of Dec 2024)

Railway's UI has changed recently. The setting is now in:

**Settings → Service → Source → Root Directory**

Or during setup, it's in the configuration step before you click "Deploy".

If you're still stuck, share a screenshot of your Railway screen and I can point you to exactly where to click!
