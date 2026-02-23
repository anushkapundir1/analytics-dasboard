from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
import schemas
from auth import hash_password, verify_password, create_token
from jose import jwt, JWTError
from datetime import datetime

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    existing = db.query(models.User).filter(models.User.username == user.username).first()

    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = models.User(
        username=user.username,
        password=hash_password(user.password),
        age=user.age,
        gender=user.gender
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = create_token({"user_id": db_user.id})

    return {"access_token": token}

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
SECRET_KEY = "secret"
ALGORITHM = "HS256"

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),db: Session = Depends(get_db)):

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@app.post("/track")
def track(
    request: schemas.TrackRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    click = models.FeatureClick(
        user_id=current_user.id,
        feature_name=request.feature_name
    )

    db.add(click)
    db.commit()

    return {"message": "Interaction recorded"}

from sqlalchemy import func

@app.get("/analytics")
def analytics(
    start_date: str = None,
    end_date: str = None,
    age_group: str = None,
    gender: str = None,
    selected_feature: str = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.FeatureClick).join(
        models.User,
        models.FeatureClick.user_id == models.User.id
)
    if start_date:
        try:
            start = datetime.fromisoformat(start_date)
            query = query.filter(models.FeatureClick.timestamp >= start)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format")

    if end_date:
        try:
            end = datetime.fromisoformat(end_date)
            query = query.filter(models.FeatureClick.timestamp <= end)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_date format")
    if gender:
        query = query.filter(models.User.gender == gender)

    if age_group == "<18":
        query = query.filter(models.User.age < 18)

    elif age_group == "18-40":
        query = query.filter(models.User.age.between(18, 40))

    elif age_group == ">40":
        query = query.filter(models.User.age > 40)

    bar_data = query.with_entities(
        models.FeatureClick.feature_name,
        func.count(models.FeatureClick.id).label("count")
    ).group_by(
        models.FeatureClick.feature_name
    ).all()

    bar_result = [
        {"feature_name": row.feature_name, "count": row.count}
        for row in bar_data
]
    if selected_feature:
        line_data = query.filter(
            models.FeatureClick.feature_name == selected_feature
        ).with_entities(
            func.date(models.FeatureClick.timestamp).label("date"),
            func.count(models.FeatureClick.id).label("count")
    ).group_by(
        func.date(models.FeatureClick.timestamp)
    ).order_by(
        func.date(models.FeatureClick.timestamp)
    ).all()

        line_result = [
            {"date": str(row.date), "count": row.count}
            for row in line_data
        ]
    else:
        line_result = []
    return {
    "bar_chart": bar_result,
    "line_chart": line_result
}
@app.get("/")
def home():
    return {"message": "API Working"}