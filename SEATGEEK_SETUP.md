# SeatGeek API Setup Instructions

## What is SeatGeek?
SeatGeek is a ticket marketplace API that provides **much better price data** than Ticketmaster. While Ticketmaster only includes prices for ~30-40% of events, SeatGeek provides:
- `lowest_price` - The cheapest ticket available
- `average_price` - Average ticket price
- `highest_price` - Most expensive ticket
- `listing_count` - Number of tickets available

## How to Get Your Free API Key

### Step 1: Sign Up
1. Go to https://seatgeek.com/account/develop
2. Click "Sign up" or "Log in" if you already have a SeatGeek account
3. Create an account (it's free!)

### Step 2: Generate Client ID
1. Once logged in, you'll see your developer dashboard
2. Click "Create New Application" or similar button
3. Fill in application details:
   - **Name**: TickTracker (or any name you want)
   - **Description**: Ticket price tracking application
   - **Website**: http://localhost:3000 (or your domain)
4. Click "Create" or "Save"
5. You'll receive:
   - **Client ID** - This is what you need!
   - **Client Secret** - Optional, not required for basic usage

### Step 3: Add to TickTracker

#### Option A: Using Environment Variables (Recommended)
Create a `.env` file in the `ticktracker/backend/` directory:

```bash
cd ticktracker/backend
nano .env  # or use any text editor
```

Add this line:
```
SEATGEEK_CLIENT_ID=your_client_id_here
```

#### Option B: Direct Configuration
Edit `ticktracker/backend/settings.py` and replace the empty string:

```python
SEATGEEK_CLIENT_ID: str = "your_client_id_here"
```

### Step 4: Restart Backend
The backend server will automatically reload if you're using `--reload` flag:

```bash
# If not already running with --reload, restart:
uvicorn ticktracker.backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 5: Test It!
Search for events and you should now see price data from SeatGeek!

## What You'll Get

### Before SeatGeek:
```
Event: Taylor Swift Concert
Price: N/A - N/A
Source: ticketmaster
```

### After SeatGeek:
```
Event: Taylor Swift Concert
Price: $89 - $1,200
Source: seatgeek
```

## API Limits
- **Free Tier**: 5,000 requests per day
- **Rate Limit**: No strict limit for free tier
- **Cost**: Completely free!

## Troubleshooting

### "SeatGeek client ID not configured"
- Make sure you added your client ID to settings.py or .env
- Restart the backend server

### "SeatGeek API returned 403"
- Double-check your client ID is correct
- Make sure there are no extra spaces or quotes

### Still No Price Data?
- SeatGeek might not have listings for that specific event
- Try searching for popular events (concerts, sports games)
- The app will fall back to Ticketmaster data if SeatGeek has no results

## Next Steps
Once SeatGeek is configured, TickTracker will automatically:
1. Search Ticketmaster, Eventbrite, AND SeatGeek
2. Merge results and remove duplicates
3. Prefer events with price data from SeatGeek
4. Display accurate price ranges to users
