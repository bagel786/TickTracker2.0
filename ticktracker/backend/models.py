from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from datetime import datetime

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    venue = Column(String)
    city = Column(String)
    date = Column(DateTime)
    timezone = Column(String, nullable=True)
    price_low = Column(Float, nullable=True)
    price_high = Column(Float, nullable=True)
    price_median = Column(Float, nullable=True)
    url = Column(String)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    price_history = relationship("PriceHistory", back_populates="event")
    user_reports = relationship("UserPriceReport", back_populates="event")
    milestones = relationship("EventMilestone", back_populates="event")
    predictions = relationship("PredictionHistory", back_populates="event")
    similar_events = relationship("SimilarEventsCache", back_populates="event")

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, ForeignKey("events.id"))
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    data_source = Column(String, default='api')
    confidence_score = Column(Float, default=1.0)
    seat_section = Column(String, nullable=True)
    is_outlier = Column(Boolean, default=False)

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

class EventMilestone(Base):
    __tablename__ = "event_milestones"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, ForeignKey("events.id"))
    milestone_type = Column(String) 
    milestone_date = Column(DateTime)
    title = Column(String)
    description = Column(String, nullable=True)
    impact_score = Column(Float, default=0.0)
    source = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

    event = relationship("Event", back_populates="milestones")

class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, ForeignKey("events.id"))
    prediction_date = Column(DateTime)
    predicted_price = Column(Float)
    confidence_lower = Column(Float)
    confidence_upper = Column(Float)
    model_version = Column(String)
    features_used = Column(String, nullable=True)
    recommendation = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

    event = relationship("Event", back_populates="predictions")

class SimilarEventsCache(Base):
    __tablename__ = "similar_events_cache"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, ForeignKey("events.id"))
    similar_event_id = Column(String)
    similarity_score = Column(Float)
    matching_factors = Column(String, nullable=True)
    cached_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=True)

    event = relationship("Event", back_populates="similar_events")
