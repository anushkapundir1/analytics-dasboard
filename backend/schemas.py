from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    age: int
    gender: str

class UserLogin(BaseModel):
    username: str
    password: str

class TrackRequest(BaseModel):
    feature_name: str