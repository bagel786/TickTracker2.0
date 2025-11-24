import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
from joblib import dump
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "price_training_data.parquet")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "price_model.joblib")

def train_model():
    print("Starting model training...")
    
    if not os.path.exists(DATA_PATH):
        print(f"No training data found at {DATA_PATH}. Skipping training.")
        return
        
    df = pd.read_parquet(DATA_PATH)
    
    if df.empty:
        print("Training data is empty. Skipping training.")
        return

    # Features
    numeric_features = [
        "days_to_event_at_observation",
        "venue_capacity",
        "heuristic_mid",
        "ticketmaster_min_price",
        "ticketmaster_max_price",
        "eventbrite_min_tier_price"
    ]
    
    categorical_features = [
        "event_type",
        "city",
        "country",
        "weekday", # Treat as categorical or numeric? User said categorical.
        "demand_signal"
    ]
    
    # Target
    # We want to predict the residual or the actual price.
    # The prompt says: "ML model learns the residual: residual = true_price - heuristic_mid_price"
    # OR "Train the model on features -> target (log prices if you used log transform)."
    # Let's follow "Part 4: Train the Price Model ... Train the model on features -> target"
    # And "Part 5 ... ml_mid_price = np.expm1(pred)" implies we predict the price directly (log-transformed).
    
    target = "observed_market_price_mid"
    
    # Filter rows where target is missing
    df = df.dropna(subset=[target])
    
    if len(df) < 10:
        print("Not enough data to train (need at least 10 samples).")
        return

    X = df[numeric_features + categorical_features]
    y = np.log1p(df[target]) # Log transform target
    
    # Preprocessing
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
        
    # Model
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', GradientBoostingRegressor(n_estimators=100, random_state=42))
    ])
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    # Inverse transform for metrics
    y_test_orig = np.expm1(y_test)
    y_pred_orig = np.expm1(y_pred)
    
    rmse = np.sqrt(mean_squared_error(y_test_orig, y_pred_orig))
    mae = mean_absolute_error(y_test_orig, y_pred_orig)
    mape = mean_absolute_percentage_error(y_test_orig, y_pred_orig)
    
    print(f"Model Evaluation:")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAE: {mae:.2f}")
    print(f"MAPE: {mape:.2%}")
    
    # Save
    dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()
