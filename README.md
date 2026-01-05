# TickTracker

TickTracker is a full-stack event ticket price prediction application designed to help users find the best time to buy tickets. By leveraging machine learning models and heuristic data, TickTracker analyzes price trends to provide "Buy" or "Wait" recommendations, ensuring users get the best deals on events from Ticketmaster, Eventbrite, and SeatGeek.

## 🚀 Goals & Features

The primary goal of TickTracker is to democratize ticket pricing data and empower users against dynamic pricing algorithms.

*   **Aggregated Event Search**: Seamlessly search for events across multiple major ticketing platforms (Ticketmaster, Eventbrite, SeatGeek) in one place.
*   **Hybrid Price Prediction**: Uses a robust **heuristic-first approach** to estimate fair market value based on event type, timing, and venue data. Where historical data is available, an ML layer (Gradient Boosting) refines these estimates.
*   **Buy/Wait Recommendations**: Receive actionable advice on whether to purchase tickets now or wait for a potential price drop.
*   **Price History Visualization**: View historical price trends to understand market fluctuations for specific events.

## 🛠 Tech Stack

### Backend
*   **Framework**: FastAPI (Python) - High-performance, easy-to-use web framework.
*   **Database**: SQLite (Development) / PostgreSQL (Production ready) - managed via SQLAlchemy ORM.
*   **Machine Learning**: scikit-learn - powering the price prediction models.
*   **Task Management**: Automated background tasks for data fetching and model retraining.

### Frontend
*   **Framework**: Next.js 14 - React framework for production-grade web applications.
*   **Styling**: Tailwind CSS - Utility-first CSS framework for rapid UI development.
*   **Language**: TypeScript - For type-safe, robust code.
*   **UI Components**: Custom components built for responsiveness and accessibility.

## 🏃‍♂️ Getting Started

Follow these instructions to run the project locally.

### Prerequisites
*   Node.js (v18+)
*   Python (v3.10+)
*   Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd TickTracker2
    ```

2.  **Backend Setup:**
    Navigate to the backend directory:
    ```bash
    cd ticktracker/backend
    ```

    Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

    Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

    Create a `.env` file based on `.env.example` and add your API keys:
    ```bash
    cp .env.example .env
    # Edit .env with your Ticketmaster, Eventbrite, and SeatGeek keys
    ```

    Start the backend server:
    ```bash
    python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

3.  **Frontend Setup:**
    Open a new terminal and navigate to the frontend directory:
    ```bash
    cd ticktracker/frontend
    ```

    Install dependencies:
    ```bash
    npm install
    ```

    Start the development server:
    ```bash
    npm run dev
    ```

    The application should now be accessible at `http://localhost:3000`.

## 🚢 Deployment

The project includes a `deploy.sh` script to automate deployment on a VPS (Virtual Private Server).

*   **Initial Setup**: `./deploy.sh server`
*   **Service Configuration**: `sudo ./deploy.sh systemd`
*   **Nginx Configuration**: `sudo ./deploy.sh nginx yourdomain.com`
*   **Update App**: `./deploy.sh update`

Refer to the script itself for more detailed usage.

## 🔑 API Configuration

To fully utilize TickTracker, you will need API keys from the following providers:
*   **Ticketmaster**: [Developer Portal](https://developer.ticketmaster.com/)
*   **Eventbrite**: [Platform API](https://www.eventbrite.com/platform/api)
*   **SeatGeek**: [Platform](https://platform.seatgeek.com/)

Ensure these are correctly set in your `backend/.env` file.
