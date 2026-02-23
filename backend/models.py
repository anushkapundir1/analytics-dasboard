
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    age = Column(Integer)
    gender = Column(String)

class FeatureClick(Base):
    __tablename__ = "feature_clicks"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    feature_name = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)