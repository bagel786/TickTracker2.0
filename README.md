# 🎫 TickTracker

TickTracker is a full-stack event ticket price prediction application designed to help users find the best time to buy tickets. By leveraging machine learning models and heuristic data, TickTracker analyzes price trends to provide "Buy" or "Wait" recommendations, ensuring users get the best deals on events from Ticketmaster, Eventbrite, and SeatGeek.

## 🚀 Goals & Features

The primary goal of TickTracker is to democratize ticket pricing data and empower users against dynamic pricing algorithms.

- **Aggregated Event Search**: Seamlessly search for events across multiple major ticketing platforms (Ticketmaster, Eventbrite, SeatGeek) in one place
- **Hybrid Price Prediction**: Uses a robust **heuristic-first approach** to estimate fair market value based on event type, timing, and venue data. Where historical data is available, an ML layer (Gradient Boosting) refines these estimates
- **Buy/Wait Recommendations**: Receive actionable advice on whether to purchase tickets now or wait for a potential price drop
- **Price History Visualization**: View historical price trends to understand market fluctuations for specific events
- **User Price Reports**: Community-driven price reporting with anti-manipulation validation
- **Enhanced Analytics**: Interactive charts with price trends, predictions, and market insights

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI (Python) - High-performance, easy-to-use web framework
- **Database**: SQLite (Development) / PostgreSQL (Production ready) - managed via SQLAlchemy ORM
- **Machine Learning**: scikit-learn (Gradient Boosting) - powering the price prediction models
- **Data Processing**: pandas, numpy - for data manipulation and analysis
- **Web Scraping**: BeautifulSoup4, httpx - for fetching event data from multiple sources
- **Task Management**: Automated background tasks for data fetching and model retraining

### Frontend
- **Framework**: Next.js 14 (App Router) - React framework for production-grade web applications
- **Styling**: Tailwind CSS - Utility-first CSS framework for rapid UI development
- **Language**: TypeScript - For type-safe, robust code
- **Charts**: Recharts - Composable charting library for data visualization
- **UI Components**: Custom components built for responsiveness and accessibility
- **Icons**: Lucide React - Beautiful & consistent icon toolkit

## 🏃‍♂️ Getting Started

Follow these instructions to run the project locally.

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- Git

### Installation

#### Option 1: Docker Compose (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ticktracker
   ```

2. **Set up environment variables:**
   ```bash
   cp ticktracker/backend/.env.example ticktracker/backend/.env
   cp ticktracker/frontend/.env.example ticktracker/frontend/.env.local
   ```
   
   Edit the `.env` files with your API keys.

3. **Start the application:**
   ```bash
   docker-compose up -d
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

#### Option 2: Manual Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ticktracker
   ```

2. **Backend Setup:**
   ```bash
   cd ticktracker/backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your API keys
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Frontend Setup (in a new terminal):**
   ```bash
   cd ticktracker/frontend
   npm install
   cp .env.example .env.local
   # Edit .env.local with your backend URL
   npm run dev
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 🔑 API Configuration

To fully utilize TickTracker, you will need API keys from the following providers:

- **Ticketmaster**: [Developer Portal](https://developer.ticketmaster.com/)
- **Eventbrite**: [Platform API](https://www.eventbrite.com/platform/api)
- **SeatGeek**: [Platform](https://platform.seatgeek.com/)

### Backend Environment Variables (.env)
```env
TICKETMASTER_API_KEY=your_key_here
TICKETMASTER_SECRET=your_secret_here
EVENTBRITE_PRIVATE_TOKEN=your_token_here
SEATGEEK_CLIENT_ID=your_client_id_here
SEATGEEK_CLIENT_SECRET=your_client_secret_here
DATABASE_URL=sqlite:///./ticktracker.db
CORS_ORIGINS=*
```

### Frontend Environment Variables (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📊 Machine Learning Model

TickTracker uses a hybrid approach for price prediction:

1. **Heuristic-First**: Base predictions on event type, venue capacity, days until event, and historical patterns
2. **ML Enhancement**: Gradient Boosting model trained on historical price data refines predictions
3. **Confidence Scoring**: Transparent confidence levels based on data availability and model certainty

### Training the Model
```bash
cd ticktracker/backend
python ml/train_price_model.py
```

Or via API:
```bash
curl -X POST http://localhost:8000/ml/train_price_model
```

## 🚢 Deployment

### Using Docker Compose
```bash
docker-compose up -d
```

### Using the Deploy Script (VPS)
The project includes a `deploy.sh` script to automate deployment on a VPS:

```bash
# Initial server setup
./deploy.sh server

# Configure systemd services
sudo ./deploy.sh systemd

# Configure Nginx
sudo ./deploy.sh nginx yourdomain.com

# Update application
./deploy.sh update
```

### Production Considerations
- Use PostgreSQL instead of SQLite for production
- Set up SSL certificates (Let's Encrypt recommended)
- Configure proper CORS origins
- Set up automated backups
- Monitor logs and performance
- Schedule regular model retraining

## 📁 Project Structure

```
ticktracker/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── database.py          # Database configuration
│   ├── settings.py          # Application settings
│   ├── ml/                  # Machine learning module
│   │   ├── price_model.py   # Price prediction logic
│   │   ├── train_price_model.py
│   │   └── data/            # Training data
│   ├── routers/             # API route handlers
│   ├── services/            # Business logic services
│   └── utils/               # Utility functions (scraping, etc.)
├── frontend/
│   ├── app/
│   │   ├── page.tsx         # Home page
│   │   ├── layout.tsx       # Root layout
│   │   ├── components/      # React components
│   │   ├── events/          # Event pages
│   │   ├── lib/             # Utility functions
│   │   └── services/        # API client
│   └── public/              # Static assets
└── docker-compose.yml       # Docker orchestration
```

## 🔧 API Endpoints

### Events
- `GET /events/search` - Search events across platforms
- `GET /events/{event_id}` - Get event details
- `GET /price-history/{event_id}` - Get price history for an event
- `POST /events/{event_id}/report-price` - Report a price for an event

### Predictions
- `GET /predict/{event_id}` - Get price prediction and recommendation
- `POST /ml/predict_price` - Predict price for event payload

### Machine Learning
- `POST /ml/train` - Train the ML model
- `POST /ml/train_price_model` - Train the price prediction model

### Charts & Analytics
- `GET /charts/price-trends/{event_id}` - Get enhanced price trend data

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Event data provided by Ticketmaster, Eventbrite, and SeatGeek APIs
- Built with FastAPI, Next.js, and scikit-learn
- Inspired by the need for transparent ticket pricing

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This application is for educational and research purposes. Always verify prices on official ticketing platforms before making purchases.
