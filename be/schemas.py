from pydantic import BaseModel
from typing import Optional

class PropertyBase(BaseModel):
    area: str
    property_type: str
    size_sqft: int
    bedrooms: int

class PropertyCreate(PropertyBase):
    pass

class PropertyOut(PropertyBase):
    id: int
    price_aed: Optional[float] = None
    rent_aed: Optional[float] = None

    class Config:
        from_attributes = True

class PredictionInput(BaseModel):
    area: str
    property_type: str
    size_sqft: int
    bedrooms: int

class PredictionOutput(BaseModel):
    predicted_price_aed: float
    rental_yield_percent: float
    roi_5yr_percent: float
