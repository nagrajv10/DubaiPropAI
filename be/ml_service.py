import os
import joblib
import pandas as pd

# Load models at startup to keep them in memory
MODELS_PATH = os.getenv("MODELS_PATH", "../ml/models/models.joblib")
models = None

def load_models():
    global models
    if os.path.exists(MODELS_PATH):
        models = joblib.load(MODELS_PATH)
        print(f"Models loaded successfully from {MODELS_PATH}")
    else:
        print(f"Warning: Models not found at {MODELS_PATH}")

def predict(area: str, property_type: str, size_sqft: int, bedrooms: int):
    if models is None:
        raise ValueError("Models are not loaded.")

    # Create dataframe for prediction matching the training feature names
    input_df = pd.DataFrame([{
        'area': area,
        'property_type': property_type,
        'size_sqft': size_sqft,
        'bedrooms': bedrooms
    }])

    price = models['price'].predict(input_df)[0]
    rental_yield = models['rental_yield'].predict(input_df)[0]
    roi = models['roi'].predict(input_df)[0]

    return {
        "predicted_price_aed": float(price),
        "rental_yield_percent": float(rental_yield),
        "roi_5yr_percent": float(roi)
    }
