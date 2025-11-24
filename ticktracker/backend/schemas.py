from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class EventBase(BaseModel):
    id: str
    name: str
    venue: str
    city: str
    date: datetime
    price_low: Optional[float] = None
    price_high: Optional[float] = None
    url: str
    source: str

class EventCreate(EventBase):
    pass

class Event(EventBase):
    created_at: datetime

    class Config:
        from_attributes = True

class PriceHistoryBase(BaseModel):
    price: float
    timestamp: datetime

class PriceHistory(PriceHistoryBase):
    id: int
    event_id: str

    class Config:
        from_attributes = True

class EventDetail(Event):
    price_history: List[PriceHistory] = []

class Prediction(BaseModel):
    prediction: str
    confidence: float

class PriceReportCreate(BaseModel):
    price: float
    source_url: Optional[str] = None

class UserPriceReport(BaseModel):
    id: int
    event_id: str
    price: float
    source_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
