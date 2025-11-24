# Price Estimation Logic

Since public APIs (Ticketmaster, SeatGeek) often hide price data, TickTracker now uses a **Smart Estimation Engine** to provide realistic pricing when real data is missing.

## How It Works

The logic is located in `backend/utils/fetch_events.py` inside `generate_mock_price()`.

### 1. Base Price by Event Type
We analyze the event name to set a baseline:
- **Festivals**: $200
- **NFL/Football**: $150
- **Broadway/Musicals** (Hamilton, Wicked, etc.): $140
- **NBA/Basketball**: $120
- **Major Concerts/Tours**: $85
- **Symphony/Orchestra**: $60
- **Default**: $45

### 2. City Multiplier
Prices are adjusted based on the location. Major hubs get a **1.4x multiplier**:
- New York
- Los Angeles
- Chicago
- San Francisco
- Las Vegas

### 3. Variance & Randomness
To make prices look natural, we apply:
- **Variance**: +/- 20% on the base price
- **Range**: The "High" price is set to 1.5x - 3.0x the "Low" price

### 4. Transparency
All estimated prices are clearly marked with source: `seatgeek (Est.)` or `ticketmaster (Est.)`.

## Customizing the Logic

You can tweak the values in `backend/utils/fetch_events.py`:

```python
def generate_mock_price(event: schemas.Event) -> schemas.Event:
    # ...
    if any(k in name_lower for k in ['your_keyword']):
        base_price = 100.0
    # ...
```

## Why Not Scrape?
We chose estimation over scraping because:
1.  **Reliability**: Scraping breaks frequently when sites change.
2.  **Speed**: Scraping is slow; estimation is instant.
3.  **Legality**: Scraping violates Terms of Service and gets IPs banned.
4.  **Consistency**: Estimation guarantees data for every event.
