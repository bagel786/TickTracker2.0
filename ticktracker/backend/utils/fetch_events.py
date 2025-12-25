import httpx
from datetime import datetime, timedelta
from typing import List, Optional
import schemas
from settings import settings
import asyncio
from utils import pricing_heuristics

async def fetch_ticketmaster_events(query: str, location: str, start_date: datetime, end_date: datetime) -> List[schemas.Event]:
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": settings.TICKETMASTER_API_KEY,
        "keyword": query,
        "city": location,
        "startDateTime": start_date.strftime("%Y-%m-%dT%H:%M:%SZ") if start_date else None,
        "endDateTime": end_date.strftime("%Y-%m-%dT%H:%M:%SZ") if end_date else None,
        "size": 50,
        "sort": "date,asc"
    }
    
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            events = []
            if "_embedded" in data and "events" in data["_embedded"]:
                for item in data["_embedded"]["events"]:
                    try:
                        price_ranges = item.get("priceRanges", [])
                        price_low = price_ranges[0].get("min") if price_ranges else None
                        price_high = price_ranges[0].get("max") if price_ranges else None
                        
                        # Safely extract venue and city
                        venue = "Unknown Venue"
                        city = "Unknown City"
                        if "_embedded" in item and "venues" in item["_embedded"] and len(item["_embedded"]["venues"]) > 0:
                            venue_data = item["_embedded"]["venues"][0]
                            venue = venue_data.get("name", "Unknown Venue")
                            if "city" in venue_data:
                                city = venue_data["city"].get("name", "Unknown City")
                        
                        # Safely extract date
                        event_date = datetime.utcnow()
                        if "dates" in item and "start" in item["dates"]:
                            if "dateTime" in item["dates"]["start"]:
                                event_date = datetime.fromisoformat(item["dates"]["start"]["dateTime"].replace("Z", "+00:00"))
                            elif "localDate" in item["dates"]["start"]:
                                # If only date is available, use it with midnight time
                                event_date = datetime.fromisoformat(item["dates"]["start"]["localDate"] + "T00:00:00+00:00")
                        
                        # Safely extract URL
                        event_url = item.get("url", f"https://www.ticketmaster.com/event/{item['id']}")

                        # Extract timezone
                        timezone = None
                        if "dates" in item and "timezone" in item["dates"]:
                            timezone = item["dates"]["timezone"]

                        events.append(schemas.Event(
                            id=f"tm_{item['id']}",
                            name=item["name"],
                            venue=venue,
                            city=city,
                            date=event_date,
                            price_low=price_low,
                            price_high=price_high,
                            url=event_url,
                            source="ticketmaster",
                            timezone=timezone,
                            created_at=datetime.utcnow()
                        ))
                    except Exception as e:
                        print(f"Error parsing Ticketmaster event {item.get('id', 'unknown')}: {e}")
                        continue
            return events
        except Exception as e:
            print(f"Error fetching Ticketmaster events: {e}")
            return []

async def fetch_eventbrite_events(query: str, location: str, start_date: datetime, end_date: datetime) -> List[schemas.Event]:
    # Eventbrite API requires organization ID for events usually, or search endpoint which is deprecated/restricted.
    # Assuming we have access to a search endpoint or similar.
    # For this implementation, we will mock it if the API key doesn't work for public search directly without more setup.
    # However, let's try to use the /v3/events/search/ if available or similar.
    # Note: Eventbrite Public API for search is often restricted.
    
    url = "https://www.eventbriteapi.com/v3/events/search/" 
    headers = {"Authorization": f"Bearer {settings.EVENTBRITE_PRIVATE_TOKEN}"}
    params = {
        "q": query,
        "location.address": location,
        "start_date.range_start": start_date.strftime("%Y-%m-%dT%H:%M:%SZ") if start_date else None,
        "start_date.range_end": end_date.strftime("%Y-%m-%dT%H:%M:%SZ") if end_date else None,
    }
    params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            # response.raise_for_status() # Eventbrite might return 403 if not allowed
            if response.status_code != 200:
                print(f"Eventbrite API returned {response.status_code}")
                return []
                
            data = response.json()
            events = []
            if "events" in data:
                for item in data["events"]:
                    events.append(schemas.Event(
                        id=f"eb_{item['id']}",
                        name=item["name"]["text"],
                        venue="Unknown Venue", # Requires separate call usually
                        city="Unknown City",
                        date=datetime.fromisoformat(item["start"]["utc"].replace("Z", "+00:00")),
                        price_low=None, # Often hidden
                        price_high=None,
                        url=item["url"],
                        source="eventbrite",
                        timezone=item["start"].get("timezone"),
                        created_at=datetime.utcnow()
                    ))
            return events
        except Exception as e:
            print(f"Error fetching Eventbrite events: {e}")
            return []

async def fetch_seatgeek_events(query: str, location: str, start_date: datetime, end_date: datetime) -> List[schemas.Event]:
    """
    Fetch events from SeatGeek API.
    SeatGeek provides better price data than Ticketmaster!
    Sign up at https://platform.seatgeek.com/ to get your free client ID.
    """
    if not settings.SEATGEEK_CLIENT_ID:
        print("SeatGeek client ID not configured. Skipping SeatGeek API.")
        return []
    
    url = "https://api.seatgeek.com/2/events"
    params = {
        "client_id": settings.SEATGEEK_CLIENT_ID,
        "q": query,
        "venue.city": location,
        "datetime_utc.gte": start_date.strftime("%Y-%m-%dT%H:%M:%S") if start_date else None,
        "datetime_utc.lte": end_date.strftime("%Y-%m-%dT%H:%M:%S") if end_date else None,
        "per_page": 50,
        "sort": "datetime_utc.asc"
    }
    params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            if response.status_code != 200:
                print(f"SeatGeek API returned {response.status_code}: {response.text}")
                return []
                
            data = response.json()
            events = []
            if "events" in data:
                for item in data["events"]:
                    try:
                        # SeatGeek provides excellent price data!
                        stats = item.get("stats", {})
                        price_low = stats.get("lowest_price")
                        price_high = stats.get("highest_price")
                        
                        # Extract venue info
                        venue_data = item.get("venue", {})
                        venue = venue_data.get("name", "Unknown Venue")
                        city = venue_data.get("city", "Unknown City")
                        timezone = venue_data.get("timezone")
                        
                        events.append(schemas.Event(
                            id=f"sg_{item['id']}",
                            name=item["title"],
                            venue=venue,
                            city=city,
                            date=datetime.fromisoformat(item["datetime_utc"].replace("Z", "+00:00")),
                            price_low=price_low,
                            price_high=price_high,
                            url=item["url"],
                            source="seatgeek",
                            timezone=timezone,
                            created_at=datetime.utcnow()
                        ))
                    except Exception as e:
                        print(f"Error parsing SeatGeek event {item.get('id', 'unknown')}: {e}")
                        continue
            return events
        except Exception as e:
            print(f"Error fetching SeatGeek events: {e}")
            return []

async def search_all_events(query: str, location: str, start_date: Optional[datetime], end_date: Optional[datetime]) -> List[schemas.Event]:
    # Default to upcoming events if no date provided
    if not start_date:
        start_date = datetime.utcnow()
    
    # Limit to 18 months if not specified
    if not end_date:
        end_date = start_date + timedelta(days=18*30)

    # Fetch from all APIs concurrently
    tm_task = fetch_ticketmaster_events(query, location, start_date, end_date)
    eb_task = fetch_eventbrite_events(query, location, start_date, end_date)
    sg_task = fetch_seatgeek_events(query, location, start_date, end_date)
    
    results = await asyncio.gather(tm_task, eb_task, sg_task)
    print(f"DEBUG: TM found {len(results[0])}, EB found {len(results[1])}, SG found {len(results[2])}")
    all_events = results[0] + results[1] + results[2]
    
    # Deduplication with fuzzy matching
    unique_events = []
    
    # Sort events to prioritize those with real prices first
    # Priority: Has Price > SeatGeek > Ticketmaster > Eventbrite
    def event_priority(e):
        score = 0
        if e.price_low is not None: score += 100
        if e.source == "seatgeek": score += 10
        elif e.source == "ticketmaster": score += 5
        return score
        
    all_events.sort(key=event_priority, reverse=True)
    
    import difflib
    import re

    def normalize_string(s: str) -> str:
        # Remove common suffixes/prefixes and non-alphanumeric chars
        s = s.lower()
        s = re.sub(r'\(.*?\)', '', s) # Remove content in parens like (Touring)
        s = re.sub(r'[^a-z0-9\s]', '', s)
        return s.strip()

    def are_duplicates(e1: schemas.Event, e2: schemas.Event) -> bool:
        # Check date (handle timezone differences by comparing YYYY-MM-DD)
        d1 = e1.date.strftime("%Y-%m-%d")
        d2 = e2.date.strftime("%Y-%m-%d")
        if d1 != d2:
            return False
            
        # Normalize names
        n1 = normalize_string(e1.name)
        n2 = normalize_string(e2.name)
        
        # Normalize venues
        v1 = normalize_string(e1.venue)
        v2 = normalize_string(e2.venue)
        
        # If venues are very similar (or one is unknown), be more lenient with name
        venue_match = (v1 == v2) or (v1 in v2) or (v2 in v1) or (difflib.SequenceMatcher(None, v1, v2).ratio() > 0.8)
        
        if venue_match:
            # If venues match, we can trust substring matches even for short names
            # e.g. "Six" in "Six the Musical"
            if n1 in n2 or n2 in n1:
                return True
            # Or fuzzy match with lower threshold
            if difflib.SequenceMatcher(None, n1, n2).ratio() > 0.6:
                return True
        
        # If venues don't match (or are unknown), stick to strict name matching
        if n1 == n2:
            return True
        if difflib.SequenceMatcher(None, n1, n2).ratio() > 0.85:
            return True
            
        return False

    for event in all_events:
        is_dup = False
        for existing in unique_events:
            if are_duplicates(event, existing):
                is_dup = True
                break
        
        if not is_dup:
            # If no price, generate estimated price
            if event.price_low is None:
                event = generate_mock_price(event)
            unique_events.append(event)
                
    return unique_events

def generate_mock_price(event: schemas.Event) -> schemas.Event:
    """
    Generates a realistic estimated price based on event metadata.
    This is a fallback when APIs don't provide price data.
    """
    # Calculate heuristic price
    heuristic_data = pricing_heuristics.compute_heuristic_price(event)
    mid_price = heuristic_data["heuristic_mid"]
    
    # Use deterministic ranges for estimation
    # We estimate the low price is ~90% of the calculated average, high is ~130%
    low_price = mid_price * 0.9
    high_price = mid_price * 1.3
    
    event.price_low = round(low_price, 2)
    event.price_high = round(high_price, 2)
    
    # Mark source as estimated so the frontend can display a disclaimer
    event.source = f"{event.source} (Est.)"
    
    return event
