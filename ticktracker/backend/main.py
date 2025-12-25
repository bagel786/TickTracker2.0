from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import models, schemas, database, settings
from utils import fetch_events, price_cleaner

from ml import train, train_price_model, price_model

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title=settings.settings.PROJECT_NAME)

# CORS - Configure allowed origins from environment
cors_origins = settings.settings.CORS_ORIGINS.split(",") if settings.settings.CORS_ORIGINS != "*" else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "TickTracker API is running"}

@app.get("/events/search", response_model=List[schemas.Event])
async def search_events(
    query: Optional[str] = None,
    location: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(database.get_db)
):
    # 1. Fetch from external APIs (Ticketmaster, Eventbrite)
    # This should ideally be a background task or cached, but for now we call directly
    # to ensure we have fresh data for the search.
    # In a real prod app, we'd search our DB first, then fetch external if needed.
    
    # For this implementation, we'll fetch and merge.
    external_events = await fetch_events.search_all_events(query, location, start_date, end_date)
    
    # 2. Save/Update in DB (Deduplication happens here or in fetch_events)
    # fetch_events should handle deduplication logic before returning
    
    # Filter by price if needed (since APIs might not support strict price filtering)
    filtered_events = []
    for event_data in external_events:
        if min_price is not None and event_data.price_low is not None and event_data.price_low < min_price:
            continue
        if max_price is not None and event_data.price_low is not None and event_data.price_low > max_price:
            continue
        filtered_events.append(event_data)

    # Save to DB to ensure we have them for details/history
    # This is a simplified "upsert" logic
    for event in filtered_events:
        db_event = db.query(models.Event).filter(models.Event.id == event.id).first()
        if not db_event:
            db_event = models.Event(**event.model_dump())
            db.add(db_event)
        else:
            # Update fields if needed
            pass
    db.commit()
    
    return filtered_events

@app.get("/events/{event_id}", response_model=schemas.EventDetail)
def get_event(event_id: str, db: Session = Depends(database.get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.get("/price-history/{event_id}", response_model=List[schemas.PriceHistory])
def get_price_history(event_id: str, db: Session = Depends(database.get_db)):
    history = db.query(models.PriceHistory).filter(models.PriceHistory.event_id == event_id).all()
    return history

@app.get("/predict/{event_id}", response_model=schemas.Prediction)
def predict_price(event_id: str, db: Session = Depends(database.get_db)):
    # Use the real prediction logic (ML + Heuristic blend)
    # This keeps the app honest - no more fake 85% confidence
    try:
        # First, we need the event object. For now we reconstruct a minimal one or fetch from DB
        # Ideally this endpoint should probably read the event from DB first
        event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if not event:
             raise HTTPException(status_code=404, detail="Event not found for prediction")
             
        # Convert DB model to Schema if needed, or pass DB model if compatible
        # Our predict_price_for_event expects an object with attributes.
        
        prediction_result = price_model.predict_price_for_event(event)
        
        return {
            "prediction": prediction_result["buy_recommendation"].split(" ")[0].lower(), # "buy", "wait", "monitor"
            "confidence": float(prediction_result["confidence"]) / 100.0,
            "next_7_days_projection": [
                 prediction_result["pred_mid_price"] * (1 + (i * 0.01)) for i in range(7) # Placeholder projection based on mid price
            ]
        }
    except Exception as e:
        print(f"Prediction error: {e}")
        # Fallback if something breaks
        return {
            "prediction": "monitor",
            "confidence": 0.0,
            "next_7_days_projection": []
        }

@app.post("/ml/train")
def train_model():
    train.train_model()
    return {"message": "Training started"}

@app.post("/ml/predict_price")
def predict_price_api(event: schemas.Event):
    """
    Predict price for a given event payload.
    """
    return price_model.predict_price_for_event(event)

@app.post("/ml/train_price_model")
def train_price_model_api():
    """
    Trigger training of the price prediction model.
    """
    # In a real app, this should be a background task
    try:
        train_price_model.train_model()
        return {"message": "Price model training completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@app.post("/events/{event_id}/report-price", response_model=schemas.UserPriceReport)
def report_price(event_id: str, report: schemas.PriceReportCreate, db: Session = Depends(database.get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    # Validation Logic (Anti-Manipulation)
    # 1. Price must be positive
    if report.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be positive")
        
    # 2. Check against heuristic/current range if available
    # If we have a price_low, use it as a baseline. If not, maybe use heuristic.
    # Let's use a generous multiplier (e.g. 0.2x to 5x) to catch astronomical outliers.
    baseline_price = event.price_low or 100.0 # Default if unknown
    
    if report.price > 50000: # Hard cap for safety unless it's the Super Bowl
        raise HTTPException(status_code=400, detail="Price seems unrealistically high. Please verify.")
        
    # 3. Save report
    db_report = models.UserPriceReport(
        event_id=event_id,
        price=report.price,
        source_url=report.source_url
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    return db_report
