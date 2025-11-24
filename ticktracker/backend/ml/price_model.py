import joblib
import os
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from ..utils import pricing_heuristics
from typing import Dict, Any, Optional

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "price_model.joblib")

_price_model = None

def get_price_model():
    global _price_model
    if _price_model is None:
        if os.path.exists(MODEL_PATH):
            try:
                _price_model = joblib.load(MODEL_PATH)
            except Exception as e:
                print(f"Error loading model: {e}")
                return None
        else:
            return None
    return _price_model

def blend_prices(heuristic_mid: float, ml_mid: float, confidence: float) -> Dict[str, float]:
    """
    Returns final_low, final_high, final_mid, confidence.
    """
    alpha = confidence  # 0-1, 1 = trust model fully
    
    # Simple blending: weighted average
    final_mid = alpha * ml_mid + (1 - alpha) * heuristic_mid

    final_low = final_mid * 0.8
    final_high = final_mid * 1.3

    return {
        "final_low": round(final_low, 2),
        "final_high": round(final_high, 2),
        "final_mid": round(final_mid, 2),
        "confidence": round(confidence * 100, 1),
    }

def get_buy_recommendation(days_to_event: int, confidence: float, current_price: Optional[float], expected_mid: float) -> str:
    """
    Simple buy/wait logic.
    """
    if days_to_event <= 5:
        return "Buy now"
    
    if current_price is None:
        return "Monitor"
        
    if confidence >= 0.75:
        if current_price < expected_mid * 0.9:
            return "Buy now"
        if current_price > expected_mid * 1.1:
            return "Wait"
            
    return "Monitor"

def predict_price_for_event(event) -> Dict[str, Any]:
    """
    Predict price for an event using ML + Heuristics.
    Input: Event object (pydantic model or similar)
    """
    # 1. Compute Heuristics
    heuristic_data = pricing_heuristics.compute_heuristic_price(event)
    heuristic_mid = heuristic_data["heuristic_mid"]
    
    # 2. Try ML Prediction
    model = get_price_model()
    ml_mid = None
    confidence = 0.0
    source = "heuristic_only"
    
    if model:
        try:
            # Build feature vector
            # Must match training features order/names
            
            # Extract features
            days_to_event = pricing_heuristics.compute_days_to_event(event.date)
            venue_capacity = getattr(event, "venue_capacity", None) # Might be missing on Event object
            
            # We need to construct a DataFrame for the pipeline
            features = {
                "days_to_event_at_observation": [days_to_event],
                "venue_capacity": [venue_capacity if venue_capacity else np.nan],
                "heuristic_mid": [heuristic_mid],
                "ticketmaster_min_price": [event.price_low if event.source == "ticketmaster" else np.nan],
                "ticketmaster_max_price": [event.price_high if event.source == "ticketmaster" else np.nan],
                "eventbrite_min_tier_price": [event.price_low if event.source == "eventbrite" else np.nan],
                "event_type": [pricing_heuristics.classify_event_type(event)],
                "city": [event.city],
                "country": ["US"], # Default or extract
                "weekday": [event.date.weekday()],
                "demand_signal": ["unknown"] # Placeholder
            }
            
            df_features = pd.DataFrame(features)
            
            # Predict
            pred_log = model.predict(df_features)[0]
            ml_mid = np.expm1(pred_log)
            
            # Estimate confidence (mock logic for now)
            # Real logic would use prediction intervals or distance from training data
            confidence = 0.7 # Default moderate confidence if model works
            source = "ml+heuristic"
            
        except Exception as e:
            print(f"ML prediction failed: {e}")
            ml_mid = None
            
    # 3. Blend
    if ml_mid is not None:
        result = blend_prices(heuristic_mid, ml_mid, confidence)
    else:
        result = {
            "final_low": heuristic_data["heuristic_low"],
            "final_high": heuristic_data["heuristic_high"],
            "final_mid": heuristic_mid,
            "confidence": 0.0
        }
        
    # 4. Recommendation
    days_to_event = pricing_heuristics.compute_days_to_event(event.date)
    current_price = event.price_low # Use low price as proxy for "current available"
    recommendation = get_buy_recommendation(days_to_event, result["confidence"]/100.0, current_price, result["final_mid"])
    
    return {
        "event_id": event.id,
        "pred_low_price": result["final_low"],
        "pred_high_price": result["final_high"],
        "pred_mid_price": result["final_mid"],
        "confidence": result["confidence"],
        "source": source,
        "buy_recommendation": recommendation,
        "heuristic_details": heuristic_data
    }
