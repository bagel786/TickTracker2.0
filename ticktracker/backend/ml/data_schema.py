from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TrainingDataRow(BaseModel):
    event_id: str
    event_name: str
    event_type: str
    city: str
    venue_name: str
    venue_capacity: Optional[int]
    country: str
    event_datetime: datetime
    days_to_event_at_observation: int
    weekday: int
    is_weekend: bool
    base_price_heuristic: float
    heuristic_low: float
    heuristic_high: float
    heuristic_mid: float
    ticketmaster_min_price: Optional[float]
    ticketmaster_max_price: Optional[float]
    eventbrite_min_tier_price: Optional[float]
    eventbrite_max_tier_price: Optional[float]
    demand_signal: Optional[str]
    observed_market_price_low: Optional[float]
    observed_market_price_high: Optional[float]
    observed_market_price_mid: Optional[float]
    source: str
