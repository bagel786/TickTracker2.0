from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database
import chart_schemas as schemas
from services.chart_data_service import ChartDataService

router = APIRouter(
    prefix="/api/events",
    tags=["enhanced-charts"]
)

@router.get("/{event_id}/chart-data", response_model=schemas.EnhancedChartData)
def get_enhanced_chart_data(event_id: str, time_range: str = 'all', db: Session = Depends(database.get_db)):
    service = ChartDataService(db)
    chart_data = service.get_chart_data(event_id, time_range)
    if not chart_data:
        raise HTTPException(status_code=404, detail="Event not found or chart data unavailable")
    return chart_data
