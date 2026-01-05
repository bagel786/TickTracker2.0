import requests
import sys

BASE_URL = "http://localhost:8000"

def test_chart_data():
    print("Testing /api/events/{id}/chart-data...")
    
    # 1. Search for an event to get an ID
    try:
        search_res = requests.get(f"{BASE_URL}/events/search")
        search_res.raise_for_status()
        events = search_res.json()
        if not events:
            print("SKIPPING: No events found to test.")
            return
        
        event_id = events[0]['id']
        print(f"Found event ID: {event_id}")
    except Exception as e:
        print(f"FAILED to search events: {e}")
        sys.exit(1)

    # 2. Query Chart Data
    try:
        chart_url = f"{BASE_URL}/api/events/{event_id}/chart-data"
        print(f"Querying {chart_url}")
        res = requests.get(chart_url)
        res.raise_for_status()
        data = res.json()
        
        # 3. Verify Structure
        required_keys = ["historical_prices", "predictions", "milestones", "similar_events", "buy_windows", "statistics"]
        for key in required_keys:
            if key not in data:
                print(f"FAILED: Missing key '{key}' in response.")
                sys.exit(1)
        
        print("SUCCESS: Chart data structure verified.")
        print(f"Predictions count: {len(data['predictions'])}")
        print(f"Buy windows count: {len(data['buy_windows'])}")

    except Exception as e:
        print(f"FAILED to get chart data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_chart_data()
