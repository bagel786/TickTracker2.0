from datetime import datetime, timezone
import random
from typing import Dict, List, Tuple, Optional

# --- Configuration ---

HEURISTIC_CURVES: Dict[str, List[Tuple[int, int, float]]] = {
    "major_concert": [
        # (min_days_out, max_days_out, price_multiplier)
        (90, 365, 0.9),   # very early = early-bird-ish
        (30, 89, 1.0),    # normal
        (7, 29, 1.1),     # creeping up
        (0, 6, 1.25),     # last-minute surge
    ],
    "sports": [
        (120, 365, 1.05),  # early fans pay more
        (30, 119, 0.95),   # mid-range sometimes cheaper
        (7, 29, 1.05),
        (0, 6, 1.20),
    ],
    "festival": [
        (180, 365, 0.8),   # super early bird
        (60, 179, 1.0),
        (14, 59, 1.15),
        (0, 13, 1.35),
    ],
    "theatre": [
        (60, 365, 1.0),
        (14, 59, 1.05),
        (0, 13, 1.15),
    ],
    "default": [
        (30, 365, 1.0),
        (7, 29, 1.05),
        (0, 6, 1.10),
    ],
}

WEEKEND_MULTIPLIER = 1.1  # Fri/Sat/Sun
WEEKDAY_MULTIPLIER = 1.0

# --- Helper Functions ---

def classify_event_type(event) -> str:
    """
    Return one of: 'festival', 'major_concert', 'sports', 'theatre', 'symphony', 'local_show', 'default'
    Use event.name, event.category (if available), and tags.
    """
    name_lower = event.name.lower()
    
    if "festival" in name_lower:
        return "festival"
    if any(k in name_lower for k in ["nba", "nfl", "mlb", "nhl", "football", "basketball", "soccer", "baseball"]):
        return "sports"
    if any(k in name_lower for k in ["hamilton", "wicked", "lion king", "broadway", "musical", "theatre"]):
        return "theatre"
    if any(k in name_lower for k in ["symphony", "orchestra", "philharmonic"]):
        return "symphony"
    if any(k in name_lower for k in ["tour", "concert", "live"]):
        return "major_concert"
        
    return "default"

def compute_days_to_event(event_datetime_utc: datetime) -> int:
    # Ensure event_datetime_utc is timezone-aware if possible, or assume UTC
    if event_datetime_utc.tzinfo is None:
        event_datetime_utc = event_datetime_utc.replace(tzinfo=timezone.utc)
        
    now = datetime.now(timezone.utc)
    delta = event_datetime_utc - now
    return max(delta.days, 0)

def get_time_multiplier(event_type: str, days_to_event: int) -> float:
    curves = HEURISTIC_CURVES.get(event_type, HEURISTIC_CURVES["default"])
    for min_days, max_days, mult in curves:
        if min_days <= days_to_event <= max_days:
            return mult
    return 1.0

def get_venue_multiplier(capacity: Optional[int]) -> float:
    if capacity is None: return 1.0
    if capacity < 1000: return 0.9
    if capacity < 5000: return 1.0
    if capacity < 20000: return 1.1
    return 1.2

def get_day_of_week_multiplier(event_datetime: datetime) -> float:
    # 0=Mon, 4=Fri, 5=Sat, 6=Sun
    weekday = event_datetime.weekday()
    if weekday >= 4:
        return WEEKEND_MULTIPLIER
    return WEEKDAY_MULTIPLIER

def get_demand_multiplier(event) -> float:
    # Placeholder for demand signals from API
    # If we had 'status' or 'inventory_level', we'd use it here.
    # For now, return 1.0 or small random boost if name implies high demand
    name_lower = event.name.lower()
    if any(k in name_lower for k in ["taylor swift", "beyonce", "super bowl", "finals"]):
        return 1.3
    return 1.0

def infer_base_price_from_name(name_lower: str) -> float:
    base_price = 45.0 # Default
    
    if any(k in name_lower for k in ['concert', 'tour', 'live']):
        base_price = 85.0
    elif any(k in name_lower for k in ['nba', 'lakers', 'bulls', 'knicks', 'warriors']):
        base_price = 120.0
    elif any(k in name_lower for k in ['nfl', 'football']):
        base_price = 150.0
    elif any(k in name_lower for k in ['hamilton', 'wicked', 'lion king', 'broadway']):
        base_price = 140.0
    elif any(k in name_lower for k in ['festival']):
        base_price = 200.0
    elif any(k in name_lower for k in ['orchestra', 'symphony']):
        base_price = 60.0
        
    return base_price

def get_city_multiplier(city: Optional[str]) -> float:
    if not city:
        return 1.0
    city_lower = city.lower()
    if city_lower in ['new york', 'los angeles', 'chicago', 'san francisco', 'las vegas']:
        return 1.4
    return 1.0

def compute_heuristic_price(event) -> dict:
    """
    Input: Event object with metadata and event datetime.
    Output: {
        "heuristic_low": float,
        "heuristic_high": float,
        "heuristic_mid": float,
        "components": { ... detailed multipliers for debugging }
    }
    """
    name_lower = event.name.lower()
    base_price = infer_base_price_from_name(name_lower)
    
    city_mult = get_city_multiplier(event.city)
    days_to_event = compute_days_to_event(event.date)
    event_type = classify_event_type(event)
    time_mult = get_time_multiplier(event_type, days_to_event)
    
    # We don't have venue capacity in the current Event schema easily, 
    # but if we did, we'd use it. For now, assume None or default.
    venue_capacity = getattr(event, "venue_capacity", None)
    venue_mult = get_venue_multiplier(venue_capacity)
    
    dow_mult = get_day_of_week_multiplier(event.date)
    demand_mult = get_demand_multiplier(event)

    deterministic_price = (
        base_price
        * city_mult
        * time_mult
        * venue_mult
        * dow_mult
        * demand_mult
    )
    
    # Controlled randomness for "naturalness" if this is a mock price
    # But the heuristic itself should be the deterministic center.
    # The prompt says: "Heuristics are deterministic... randomness is only for visual naturalness"
    # But compute_heuristic_price should probably return the deterministic values, 
    # and let the caller add randomness if needed, OR we return the range here.
    # The prompt says: "Heuristics produce: heuristic_low, heuristic_high, heuristic_mid"
    
    heuristic_mid = round(deterministic_price, 2)
    heuristic_low = round(heuristic_mid * 0.8, 2) # Simple rule
    heuristic_high = round(heuristic_mid * 1.3, 2) # Simple rule
    
    return {
        "heuristic_low": heuristic_low,
        "heuristic_high": heuristic_high,
        "heuristic_mid": heuristic_mid,
        "components": {
            "base_price": base_price,
            "city_mult": city_mult,
            "time_mult": time_mult,
            "venue_mult": venue_mult,
            "dow_mult": dow_mult,
            "demand_mult": demand_mult,
            "days_to_event": days_to_event,
            "event_type": event_type
        }
    }
