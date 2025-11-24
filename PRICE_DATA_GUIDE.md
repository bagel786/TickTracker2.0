# Price Data Access Guide for TickTracker

## Overview
Getting real-time ticket price data is challenging because most ticket platforms restrict this information. Here's what's available and how to access it.

---

## 1. Ticketmaster Discovery API (Currently Implemented)

### What's Available
- **Price Ranges**: Some events include `priceRanges` with min/max prices
- **Availability**: Inconsistent - only ~30-40% of events have price data
- **Access**: Already implemented in our code

### API Response Example
```json
{
  "priceRanges": [
    {
      "type": "standard",
      "currency": "USD",
      "min": 49.50,
      "max": 299.00
    }
  ]
}
```

### Current Implementation
See: `ticktracker/backend/utils/fetch_events.py` lines 32-34

```python
price_ranges = item.get("priceRanges", [])
price_low = price_ranges[0].get("min") if price_ranges else None
price_high = price_ranges[0].get("max") if price_ranges else None
```

---

## 2. Alternative APIs with Better Price Data

### A. SeatGeek API
**Best for**: Actual ticket prices (not just ranges)

**Setup**:
1. Sign up at https://platform.seatgeek.com/
2. Get API credentials
3. Add to `backend/settings.py`:
```python
SEATGEEK_CLIENT_ID: str = "your_client_id"
SEATGEEK_CLIENT_SECRET: str = "your_secret"
```

**API Endpoint**:
```bash
GET https://api.seatgeek.com/2/events
?client_id=YOUR_CLIENT_ID
&q=Taylor+Swift
&venue.city=New+York
```

**Response includes**:
```json
{
  "stats": {
    "lowest_price": 89,
    "average_price": 245,
    "highest_price": 1200,
    "listing_count": 450
  }
}
```

### B. StubHub API
**Best for**: Secondary market prices

**Setup**:
- Requires partnership/business account
- More restrictive than others
- Best for established businesses

### C. Vivid Seats API
**Best for**: Real-time pricing

**Setup**:
1. Apply for API access at https://www.vividseats.com/
2. Requires business verification
3. Provides real-time inventory and pricing

---

## 3. Web Scraping (Alternative Approach)

### ⚠️ Legal Considerations
- Check each site's Terms of Service
- Respect robots.txt
- Use rate limiting
- Consider using official APIs when available

### Example: Scraping Ticketmaster Event Pages
```python
import httpx
from bs4 import BeautifulSoup

async def scrape_ticket_prices(event_url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(event_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find price elements (structure varies by site)
        price_elements = soup.find_all(class_='price-range')
        # Parse and return prices
```

---

## 4. Building Historical Price Data

### Strategy: Track Prices Over Time
Since real-time price data is limited, we can build our own database:

1. **Scheduled Scraping**: Run daily checks on tracked events
2. **Store in Database**: Save price snapshots
3. **Build Trends**: Use historical data for ML predictions

### Implementation Example
```python
# Add to backend/utils/price_tracker.py
from datetime import datetime
from ..models import PriceHistory, Event
from ..database import SessionLocal

async def track_event_prices():
    db = SessionLocal()
    events = db.query(Event).filter(Event.date > datetime.utcnow()).all()
    
    for event in events:
        # Fetch current price from API
        current_price = await get_current_price(event.id)
        
        if current_price:
            # Store in price history
            price_entry = PriceHistory(
                event_id=event.id,
                price=current_price,
                timestamp=datetime.utcnow()
            )
            db.add(price_entry)
    
    db.commit()
    db.close()
```

---

## 5. Recommended Approach for TickTracker

### Short-term (Immediate)
1. ✅ Use Ticketmaster API (already implemented)
2. ✅ Handle missing data gracefully (already implemented)
3. 🔄 Add SeatGeek API for better coverage

### Medium-term (1-2 weeks)
1. Implement scheduled price tracking
2. Build historical database
3. Add multiple API sources

### Long-term (1+ months)
1. Consider web scraping for specific high-demand events
2. Partner with ticket platforms for better API access
3. Build ML model with sufficient historical data

---

## 6. Code Changes to Add SeatGeek

### Step 1: Update settings.py
```python
SEATGEEK_CLIENT_ID: str = ""
SEATGEEK_CLIENT_SECRET: str = ""
```

### Step 2: Add to fetch_events.py
```python
async def fetch_seatgeek_events(query: str, location: str, start_date: datetime, end_date: datetime):
    url = "https://api.seatgeek.com/2/events"
    params = {
        "client_id": settings.SEATGEEK_CLIENT_ID,
        "q": query,
        "venue.city": location,
        "datetime_utc.gte": start_date.isoformat() if start_date else None,
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
        
        events = []
        for item in data.get("events", []):
            events.append(schemas.Event(
                id=f"sg_{item['id']}",
                name=item["title"],
                venue=item["venue"]["name"],
                city=item["venue"]["city"],
                date=datetime.fromisoformat(item["datetime_utc"]),
                price_low=item["stats"].get("lowest_price"),
                price_high=item["stats"].get("highest_price"),
                url=item["url"],
                source="seatgeek",
                created_at=datetime.utcnow()
            ))
        return events
```

### Step 3: Update search_all_events()
```python
sg_task = fetch_seatgeek_events(query, location, start_date, end_date)
results = await asyncio.gather(tm_task, eb_task, sg_task)
all_events = results[0] + results[1] + results[2]
```

---

## Summary

**Current Status**: 
- ✅ Ticketmaster API integrated (limited price data)
- ❌ No secondary market data yet

**Best Next Steps**:
1. Sign up for SeatGeek API (free tier available)
2. Implement SeatGeek integration (better price coverage)
3. Add scheduled price tracking to build historical data
4. Use historical data to improve ML predictions

**Why Prices Are Missing**:
- Ticketmaster doesn't always publish prices in their Discovery API
- Prices may be dynamic or restricted to checkout pages
- Some events don't have tickets on sale yet
- Secondary market APIs (SeatGeek, StubHub) have better price data
