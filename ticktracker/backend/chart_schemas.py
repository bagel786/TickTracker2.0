from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class PriceDataPoint(BaseModel):
    date: datetime
    price: float
    confidence: Optional[float] = None
    data_source: Optional[str] = None
    is_outlier: bool = False

class PredictionDataPoint(BaseModel):
    date: datetime
    predicted_price: float
    confidence_lower: float
    confidence_upper: float

class Milestone(BaseModel):
    date: datetime
    title: str
    type: str
    description: Optional[str] = None

class SimilarEvent(BaseModel):
    event_name: str
    similarity_score: float
    price_data: List[PriceDataPoint]

class BuyWindow(BaseModel):
    start_date: datetime
    end_date: datetime
    expected_price: float
    reason: str

class ChartStatistics(BaseModel):
    current_price: Optional[float]
    price_trend: str
    recommendation: str
    volatility: float

class EnhancedChartData(BaseModel):
    historical_prices: List[PriceDataPoint]
    predictions: List[PredictionDataPoint]
    milestones: List[Milestone]
    similar_events: List[SimilarEvent]
    buy_windows: List[BuyWindow]
    statistics: ChartStatistics

class MilestoneResponse(BaseModel):
    milestones: List[Milestone]

class SimilarEventsResponse(BaseModel):
    similar_events: List[SimilarEvent]

class PredictionsResponse(BaseModel):
    predictions: List[PredictionDataPoint]
    buy_windows: List[BuyWindow]
