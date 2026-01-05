from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from datetime import datetime, timedelta
import random

def seed_data():
    db = SessionLocal()
    
    # 1. Create a logical Future Event (relative to 2026)
    event_id = "seed_event_2026"
    
    # Check if exists and delete to start fresh
    existing = db.query(models.Event).filter(models.Event.id == event_id).first()
    if existing:
        db.delete(existing)
        db.commit()

    # Create Event: "Global Tech Conference 2026"
    # Date: March 15, 2026 (approx 2 months from "now" Jan 2026)
    event = models.Event(
        id=event_id,
        name="Global Tech Conference 2026",
        venue="Moscone Center",
        city="San Francisco",
        date=datetime(2026, 3, 15, 9, 0),
        timezone="America/Los_Angeles",
        price_low=250.0,
        price_high=500.0,
        price_median=375.0,
        url="https://example.com/tickets",
        source="Ticketmaster",
        created_at=datetime.utcnow()
    )
    db.add(event)
    db.commit()

    print(f"Created event: {event.name} ({event.id})")

    # 2. Generate Historical Data (Past 60 days)
    # Start date: Nov 4, 2025
    # End date: Jan 4, 2026 (Today)
    
    start_date = datetime(2025, 11, 4)
    days = 60
    base_price = 280.0
    
    print("Generating price history...")
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        
        # Add some random volatility
        change = random.uniform(-5, 8) 
        base_price += change
        base_price = max(200, base_price) # Floor
        
        history = models.PriceHistory(
            event_id=event_id,
            price=round(base_price, 2),
            timestamp=current_date,
            data_source='api',
            confidence_score=0.95,
            is_outlier=False
        )
        db.add(history)
    
    # 3. Add Milestones
    m1 = models.EventMilestone(
        event_id=event_id,
        milestone_type="Announcement",
        milestone_date=datetime(2025, 11, 10),
        title="Keynote Speaker Announced",
        description="Elon Musk announced as speaker",
        impact_score=0.8
    )
    
    m2 = models.EventMilestone(
        event_id=event_id,
        milestone_type="Release",
        milestone_date=datetime(2025, 12, 1),
        title="Early Bird Ends",
        description="Ticket prices increased",
        impact_score=0.6
    )
    
    db.add(m1)
    db.add(m2)
    
    db.commit()
    print("Database seeded successfully!")
    db.close()

if __name__ == "__main__":
    seed_data()
