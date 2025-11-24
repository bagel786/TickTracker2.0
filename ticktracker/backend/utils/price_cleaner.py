import pandas as pd
import numpy as np

def clean_price_data(price_history):
    """
    Cleans price history data by removing outliers and handling missing values.
    """
    if not price_history:
        return []

    df = pd.DataFrame([p.dict() for p in price_history])
    
    # Remove outliers using IQR
    Q1 = df['price'].quantile(0.25)
    Q3 = df['price'].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    df_clean = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)]
    
    return df_clean.to_dict('records')
