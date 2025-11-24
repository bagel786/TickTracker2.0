# TickTracker Remastered

A full-stack event ticket price prediction application with ML-powered heuristics.

## Features

- **Event Search**: Search events from Ticketmaster, Eventbrite, and SeatGeek APIs
- **Price Prediction**: ML + heuristic-based price estimation system
- **User Price Reporting**: Users can report actual prices with anti-manipulation safeguards
- **Price History Tracking**: Track price changes over time
- **Buy/Wait Recommendations**: Smart recommendations on when to purchase tickets

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- scikit-learn
- Python 3.x

### Frontend
- Next.js 14
- React
- TypeScript
- Tailwind CSS

## Setup

### Backend
```bash
cd ticktracker/backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd ticktracker/frontend
npm install
npm run dev
```

## ML Price Prediction

The system uses a two-layer approach:
1. **Heuristic Layer**: Rule-based pricing using event type, location, time-to-event, and demand signals
2. **ML Layer**: Gradient boosting model that learns corrections on top of heuristics

## API Keys Required

- Ticketmaster API Key
- Eventbrite Private Token
- SeatGeek Client ID

See `SEATGEEK_SETUP.md` for detailed setup instructions.
