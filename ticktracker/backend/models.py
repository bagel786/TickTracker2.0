from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    venue = Column(String)
    city = Column(String)
    date = Column(DateTime)
    price_low = Column(Float, nullable=True)
    price_high = Column(Float, nullable=True)
    url = Column(String)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    price_history = relationship("PriceHistory", back_populates="event")
    user_reports = relationship("UserPriceReport", back_populates="event")

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, ForeignKey("events.id"))
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event", back_populates="price_history")

class UserPriceReport(Base):
    __tablename__ = "user_price_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, ForeignKey("events.id"))
    price = Column(Float)
    source_url = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    event = relationship("Event", back_populates="user_reports")
