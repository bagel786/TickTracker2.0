from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import models
import chart_schemas as schemas
from typing import List, Optional
import math

# Placeholder for ML model imports
# from ml.price_model import predict_price_for_event

class ChartDataService:
    def __init__(self, db: Session):
        self.db = db

    def get_chart_data(self, event_id: str, time_range: str = 'all') -> schemas.EnhancedChartData:
        event = self._get_event(event_id)
        if not event:
            return None # Or raise exception

        # 1. Fetch Historical Data
        historical_prices = self._get_historical_prices(event_id, time_range)
        
        # 2. Fetch/Generate Predictions
        predictions = self._get_predictions(event)

        # 3. Fetch Milestones
        milestones = self._get_milestones(event_id)

        # 4. Fetch Similar Events (Placeholder)
        similar_events = self._get_similar_events(event_id)

        # 5. Calculate Buy Windows
        buy_windows = self._calculate_buy_windows(event, predictions)

        # 6. Generate Stats
        statistics = self._generate_statistics(event, historical_prices, predictions)

        return schemas.EnhancedChartData(
            historical_prices=historical_prices,
            predictions=predictions,
            milestones=milestones,
            similar_events=similar_events,
            buy_windows=buy_windows,
            statistics=statistics
        )

    def _get_event(self, event_id: str):
        return self.db.query(models.Event).filter(models.Event.id == event_id).first()

    def _get_historical_prices(self, event_id: str, time_range: str) -> List[schemas.PriceDataPoint]:
        query = self.db.query(models.PriceHistory)\
            .filter(models.PriceHistory.event_id == event_id)\
            .order_by(models.PriceHistory.timestamp.asc())
        
        # Apply time range filter if needed (omitted for brevity in Phase 1 basic)
        
        prices = query.all()
        return [
            schemas.PriceDataPoint(
                date=p.timestamp,
                price=p.price,
                confidence=p.confidence_score,
                data_source=p.data_source,
                is_outlier=p.is_outlier
            ) for p in prices
        ]

    def _get_predictions(self, event) -> List[schemas.PredictionDataPoint]:
        # For Phase 1, return empty or mock predictions to ensure endpoint works
        # Real ML integration can be uncommented/refined in later phases or now if stable
        
        # Mock logic to prove data flow
        predictions = []
        
        # Start predictions from "today" (simulated as Jan 4, 2026 based on seed data)
        # In a real app, this would be datetime.now()
        current_date = datetime(2026, 1, 4) 
        
        # Base price from last known history or event median
        base_price = event.price_median or 100.0
        
        for i in range(1, 15): # Predict next 14 days
            future_date = current_date + timedelta(days=i)
            # Simple mock projection: assume slight increase/fluctuation
            # We use sin wave to make it look "real"
            import math
            fluctuation = math.sin(i * 0.5) * 5 
            predicted_price = base_price + (i * 0.5) + fluctuation
            
            predictions.append(schemas.PredictionDataPoint(
                date=future_date,
                predicted_price=predicted_price,
                confidence_lower=predicted_price * 0.9,
                confidence_upper=predicted_price * 1.1
            ))
            
        return predictions

    def _get_milestones(self, event_id: str) -> List[schemas.Milestone]:
        # Fetch from DB table event_milestones
        milestones = self.db.query(models.EventMilestone)\
            .filter(models.EventMilestone.event_id == event_id)\
            .all()
            
        return [
            schemas.Milestone(
                date=m.milestone_date,
                title=m.title,
                type=m.milestone_type,
                description=m.description
            ) for m in milestones
        ]

    def _get_similar_events(self, event_id: str) -> List[schemas.SimilarEvent]:
        # Placeholder
        return []

    def _calculate_buy_windows(self, event, predictions: List[schemas.PredictionDataPoint]) -> List[schemas.BuyWindow]:
        # Simple logic: if price is dipping in prediction, suggest buy
        windows = []
        # Mock: suggest buying in the next 3 days
        if predictions:
            windows.append(schemas.BuyWindow(
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=3),
                expected_price=predictions[0].predicted_price,
                reason="Predicted low price period"
            ))
        return windows

    def _generate_statistics(self, event, history, predictions) -> schemas.ChartStatistics:
        current_price = event.price_low
        
        trend = "stable"
        if history and len(history) > 1:
            if history[-1].price > history[0].price:
                trend = "increasing"
            else:
                trend = "decreasing"
                
        return schemas.ChartStatistics(
            current_price=current_price,
            price_trend=trend,
            recommendation="wait" if trend == "decreasing" else "buy",
            volatility=0.15 # Mock
        )
