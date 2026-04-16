import pandas as pd
import numpy as np
import os
import joblib
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score

def train():
    data_path = 'ml/data/dubai_properties.csv'
    if not os.path.exists(data_path):
        print(f"Dataset not found at {data_path}. Please run generate_data.py first.")
        return
        
    df = pd.read_csv(data_path)
    
    # Features & Targets
    X = df[['area', 'property_type', 'size_sqft', 'bedrooms']]
    
    # We will train 3 separate models for price, rental_yield, roi
    y_price = df['price_aed']
    y_yield = df['rental_yield_percent']
    y_roi = df['roi_5yr_percent']
    
    # Preprocessing
    numeric_features = ['size_sqft', 'bedrooms']
    categorical_features = ['area', 'property_type']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
        
    # We will save the preprocessor and the models in a single dictionary or joblib
    models = {}
    
    targets = {
        'price': y_price,
        'rental_yield': y_yield,
        'roi': y_roi
    }
    
    for name, y in targets.items():
        print(f"Training model for {name}...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', XGBRegressor(random_state=42, n_estimators=100, learning_rate=0.1))
        ])
        
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f"  {name} test MAE: {mae:.2f}, R2: {r2:.2f}")
        
        models[name] = model

    # Save to disk
    os.makedirs('ml/models', exist_ok=True)
    joblib.dump(models, 'ml/models/models.joblib')
    print("Models saved successfully to ml/models/models.joblib")

if __name__ == "__main__":
    train()
