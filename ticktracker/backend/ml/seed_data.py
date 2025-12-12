import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

def generate_seed_data():
    """
    Generates synthetic data to train the price model.
    This simulates historical data so the model has something to learn from
    in the absence of a large real database.
    """
    
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia"]
    event_types = ["concert", "sports", "theater", "festival"]
    demand_signals = ["low", "medium", "high", "very_high"]
    
    n_samples = 1000
    data = []
    
    for _ in range(n_samples):
        # Features
        city = random.choice(cities)
        etype = random.choice(event_types)
        demand = random.choice(demand_signals)
        days_out = random.randint(1, 180)
        weekday = random.randint(0, 6)
        capacity = random.randint(1000, 80000)
        
        # Base Heuristic (what our simplistic logic would guess)
        base = 50
        if etype == "festival": base = 200
        elif etype == "sports": base = 100
        elif etype == "theater": base = 120
        
        if city in ["New York", "Los Angeles"]:
            base *= 1.4
            
        heuristic_mid = base
        
        # Simulate Market Reality (Target Variable)
        # Price increases as days_out decreases
        time_factor = 1.0 + (1.0 / (days_out + 1)) * 0.5 # Up to 50% increase last minute
        
        # Demand factor
        demand_mult = 1.0
        if demand == "high": demand_mult = 1.3
        elif demand == "very_high": demand_mult = 2.0
        
        true_market_mid = heuristic_mid * time_factor * demand_mult * random.uniform(0.9, 1.1)
        
        # TM Ranges (noisy observation of truth)
        tm_min = true_market_mid * 0.8 * random.uniform(0.95, 1.05)
        tm_max = true_market_mid * 1.2 * random.uniform(0.95, 1.05)
        
        # Occasionally missing TM data
        if random.random() < 0.3:
            tm_min = np.nan
            tm_max = np.nan
            
        data.append({
            "days_to_event_at_observation": days_out,
            "venue_capacity": capacity,
            "heuristic_mid": heuristic_mid,
            "ticketmaster_min_price": tm_min,
            "ticketmaster_max_price": tm_max,
            "eventbrite_min_tier_price": np.nan, # Mostly missing
            "event_type": etype,
            "city": city,
            "country": "US",
            "weekday": weekday,
            "demand_signal": demand,
            "observed_market_price_mid": true_market_mid
        })
        
    df = pd.DataFrame(data)
    
    # Save
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    output_path = os.path.join(data_dir, "price_training_data.parquet")
    df.to_parquet(output_path)
    print(f"Generated {n_samples} samples to {output_path}")

if __name__ == "__main__":
    generate_seed_data()
