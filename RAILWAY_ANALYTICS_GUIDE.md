# Railway Analytics & User Tracking Guide

## 🚂 Railway Built-in Analytics

Railway provides **basic infrastructure metrics** out of the box:

### What Railway Tracks (Free):
- ✅ **HTTP Request Count** - Total requests to your app
- ✅ **Response Times** - Average latency
- ✅ **CPU Usage** - Server resource usage
- ✅ **Memory Usage** - RAM consumption
- ✅ **Network Traffic** - Bandwidth in/out
- ✅ **Deployment History** - Build logs and deploy times
- ✅ **Error Logs** - Application crashes and errors

### What Railway DOESN'T Track:
- ❌ Individual user sessions
- ❌ User behavior/clicks
- ❌ Page views per user
- ❌ User demographics
- ❌ Conversion funnels
- ❌ A/B testing

---

## 📊 Adding User Analytics to Your App

For detailed user tracking, you need to add analytics tools. Here are the best options:

### Option 1: Google Analytics (Free, Most Popular)

**Setup (5 minutes):**

1. Go to [analytics.google.com](https://analytics.google.com)
2. Create a property and get your Measurement ID (G-XXXXXXXXXX)
3. Add to your Next.js app:

```bash
cd ticktracker/frontend
npm install @next/third-parties
```

Update `app/layout.tsx`:
```typescript
import { GoogleAnalytics } from '@next/third-parties/google'

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
        <GoogleAnalytics gaId="G-XXXXXXXXXX" />
      </body>
    </html>
  )
}
```

**What you get:**
- Real-time users
- Page views
- User demographics
- Traffic sources
- User flow
- Conversion tracking

---

### Option 2: Plausible Analytics (Privacy-Focused, Paid)

**Why Plausible:**
- No cookies, GDPR compliant
- Lightweight (< 1KB script)
- Simple, beautiful dashboard
- $9/month for 10k pageviews

**Setup:**
```typescript
// In app/layout.tsx, add to <head>
<Script
  defer
  data-domain="yourdomain.com"
  src="https://plausible.io/js/script.js"
/>
```

---

### Option 3: PostHog (Open Source, Self-Hosted or Cloud)

**Best for:** Product analytics, feature flags, session recording

**Setup:**
```bash
npm install posthog-js
```

```typescript
// app/providers.tsx
'use client'
import posthog from 'posthog-js'
import { PostHogProvider } from 'posthog-js/react'

if (typeof window !== 'undefined') {
  posthog.init('YOUR_PROJECT_API_KEY', {
    api_host: 'https://app.posthog.com'
  })
}

export function PHProvider({ children }) {
  return <PostHogProvider client={posthog}>{children}</PostHogProvider>
}
```

**What you get:**
- Session recordings
- Heatmaps
- Feature flags
- A/B testing
- Funnels
- Free tier: 1M events/month

---

### Option 4: Custom Analytics (Build Your Own)

Add tracking to your FastAPI backend:

```python
# ticktracker/backend/models.py
class PageView(Base):
    __tablename__ = "page_views"
    
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String)
    user_id = Column(String, nullable=True)
    ip_address = Column(String)
    user_agent = Column(String)
    referrer = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    user_id = Column(String, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    page_count = Column(Integer, default=0)
```

```python
# ticktracker/backend/main.py
from fastapi import Request
import uuid

@app.middleware("http")
async def track_requests(request: Request, call_next):
    # Track page view
    db = next(database.get_db())
    
    page_view = models.PageView(
        path=request.url.path,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        referrer=request.headers.get("referer")
    )
    db.add(page_view)
    db.commit()
    
    response = await call_next(request)
    return response

@app.get("/analytics/stats")
def get_analytics_stats(db: Session = Depends(database.get_db)):
    """Get basic analytics stats"""
    total_views = db.query(models.PageView).count()
    unique_ips = db.query(models.PageView.ip_address).distinct().count()
    
    # Views by path
    views_by_path = db.query(
        models.PageView.path,
        func.count(models.PageView.id)
    ).group_by(models.PageView.path).all()
    
    return {
        "total_views": total_views,
        "unique_visitors": unique_ips,
        "views_by_path": dict(views_by_path)
    }
```

---

## 🎯 Recommended Setup

### For Most Users:
**Google Analytics** (free) + **Railway metrics** (free)
- Total cost: $0
- Covers 90% of analytics needs

### For Privacy-Conscious:
**Plausible** ($9/month) + **Railway metrics** (free)
- Total cost: $9/month
- GDPR compliant, no cookies

### For Product Teams:
**PostHog** (free tier) + **Railway metrics** (free)
- Total cost: $0 (up to 1M events)
- Session recordings, funnels, A/B testing

### For Full Control:
**Custom analytics** (build your own) + **Railway metrics** (free)
- Total cost: $0
- Complete data ownership

---

## 📈 Key Metrics to Track

### Essential Metrics:
1. **Daily Active Users (DAU)**
2. **Page Views**
3. **Bounce Rate**
4. **Average Session Duration**
5. **Top Pages**

### TickTracker-Specific Metrics:
1. **Event Searches** - How many searches per day
2. **Price Predictions Requested** - ML model usage
3. **User Price Reports** - Community contributions
4. **Events Viewed** - Most popular events
5. **Conversion Rate** - Search → View → External link click

---

## 🚀 Quick Implementation

I can add Google Analytics to your app right now. Want me to:

1. ✅ Add Google Analytics integration
2. ✅ Add custom event tracking (searches, predictions, etc.)
3. ✅ Create an analytics dashboard endpoint in your API
4. ✅ Add privacy policy page (required for analytics)

Just provide your Google Analytics Measurement ID, or I can set it up with a placeholder you can update later.

---

## 📊 Railway Dashboard Access

To view Railway metrics:
1. Go to your Railway dashboard
2. Click on your service
3. Go to "Metrics" tab
4. View real-time graphs for:
   - Request rate
   - Response time
   - CPU/Memory usage
   - Network traffic

---

## 💡 Pro Tips

1. **Start simple** - Google Analytics is enough for most apps
2. **Track events** - Not just page views, but user actions (searches, clicks)
3. **Set up goals** - Define what success looks like
4. **Monitor Railway logs** - Catch errors early
5. **Add health checks** - Use Railway's built-in monitoring
6. **Set up alerts** - Get notified when things break

---

## 🔒 Privacy Considerations

If using analytics, you should:
- ✅ Add a privacy policy
- ✅ Add cookie consent banner (if using cookies)
- ✅ Anonymize IP addresses
- ✅ Allow users to opt-out
- ✅ Comply with GDPR/CCPA if applicable

Want me to generate a privacy policy template for you?
