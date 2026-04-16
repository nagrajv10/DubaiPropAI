from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models, schemas, crud, ml_service
from database import engine, get_db

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DubaiPropAI Backend API")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    ml_service.load_models()

@app.get("/health")
def read_health():
    return {"status": "healthy"}

@app.post("/predict", response_model=schemas.PredictionOutput)
def predict_property(input_data: schemas.PredictionInput):
    try:
        prediction = ml_service.predict(
            area=input_data.area,
            property_type=input_data.property_type,
            size_sqft=input_data.size_sqft,
            bedrooms=input_data.bedrooms
        )
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/properties", response_model=schemas.PropertyOut)
def create_property(property: schemas.PropertyCreate, db: Session = Depends(get_db)):
    return crud.create_property(db=db, property=property)

@app.get("/properties", response_model=List[schemas.PropertyOut])
def read_properties(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_properties(db, skip=skip, limit=limit)

@app.get("/properties/{property_id}", response_model=schemas.PropertyOut)
def read_property(property_id: int, db: Session = Depends(get_db)):
    db_property = crud.get_property(db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property
