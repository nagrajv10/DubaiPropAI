import pandas as pd
import numpy as np
import os

# Set random seed
np.random.seed(42)

def generate_synthetic_data(num_records=2000):
    areas = ['Marina', 'Downtown', 'JVC', 'Business Bay', 'Palm Jumeirah']
    property_types = ['Apartment', 'Villa', 'Townhouse']
    
    data = []
    for _ in range(num_records):
        area = np.random.choice(areas, p=[0.25, 0.2, 0.35, 0.15, 0.05])
        prop_type = np.random.choice(property_types, p=[0.7, 0.2, 0.1])
        
        # Base logic for size and bedrooms
        if prop_type == 'Apartment':
            bedrooms = np.random.choice([1, 2, 3, 4], p=[0.4, 0.4, 0.15, 0.05])
            base_size = 500 + (bedrooms - 1) * 350
        elif prop_type == 'Townhouse':
            bedrooms = np.random.choice([3, 4, 5], p=[0.5, 0.4, 0.1])
            base_size = 1800 + (bedrooms - 3) * 500
        else: # Villa
            bedrooms = np.random.choice([3, 4, 5, 6], p=[0.2, 0.4, 0.3, 0.1])
            base_size = 2500 + (bedrooms - 3) * 800
            
        size_sqft = np.random.normal(base_size, base_size * 0.1)
        
        # Base price per sqft depending on area
        area_multiplier = {
            'JVC': 1.0,
            'Business Bay': 1.4,
            'Marina': 1.6,
            'Downtown': 1.8,
            'Palm Jumeirah': 2.5
        }
        
        # Base price calculation
        base_price_sqft = 1000 * area_multiplier[area]
        price_aed = size_sqft * base_price_sqft * np.random.normal(1, 0.1)
        
        # Rental yield usually highest in JVC, lowest in Palm
        yield_multiplier = {
            'JVC': 0.08,
            'Business Bay': 0.065,
            'Marina': 0.06,
            'Downtown': 0.055,
            'Palm Jumeirah': 0.045
        }
        rental_yield_percent = yield_multiplier[area] * 100 * np.random.normal(1, 0.05)
        
        # Annual rent
        rent_aed = price_aed * (rental_yield_percent / 100)
        
        # 5-year ROI estimation (Rent * 5 + some capital appreciation component)
        appreciation_yearly = np.random.normal(0.02, 0.01) # 2% yearly appreciation avg
        roi_5yr_percent = (rental_yield_percent * 5) + (appreciation_yearly * 5 * 100)
        
        data.append({
            'area': area,
            'property_type': prop_type,
            'size_sqft': int(size_sqft),
            'bedrooms': bedrooms,
            'price_aed': int(price_aed),
            'rent_aed': int(rent_aed),
            'rental_yield_percent': round(rental_yield_percent, 2),
            'roi_5yr_percent': round(roi_5yr_percent, 2)
        })
        
    df = pd.DataFrame(data)
    
    os.makedirs(os.path.dirname('ml/data/dubai_properties.csv'), exist_ok=True)
    df.to_csv('ml/data/dubai_properties.csv', index=False)
    print("Synthetic data generated at ml/data/dubai_properties.csv")

if __name__ == "__main__":
    generate_synthetic_data()
