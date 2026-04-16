from sqlalchemy import Column, Integer, String, Float
from database import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    area = Column(String, index=True)
    property_type = Column(String, index=True)
    size_sqft = Column(Integer)
    bedrooms = Column(Integer)
    price_aed = Column(Float, nullable=True)
    rent_aed = Column(Float, nullable=True)
