import random
from datetime import datetime, timedelta
from database import SessionLocal, engine, Base
import models
from auth import hash_password

# Create tables if not exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ----- CONFIG -----
NUM_USERS = 20
NUM_CLICKS = 300

features = [
    "login",
    "bar_chart_click",
    "gender_filter",
    "age_group_filter",
    "date_filter",
]

genders = ["Male", "Female", "Other"]

# ----- CREATE USERS -----
users = []

for i in range(NUM_USERS):
    user = models.User(
        username=f"user{i}",
        password=hash_password("1234"),
        age=random.randint(15, 60),
        gender=random.choice(genders),
    )
    db.add(user)
    users.append(user)

db.commit()

print("Users created.")

# Refresh users with IDs
users = db.query(models.User).all()

# ----- CREATE FEATURE CLICKS -----
for _ in range(NUM_CLICKS):
    user = random.choice(users)

    random_days = random.randint(0, 30)
    random_time = datetime.utcnow() - timedelta(days=random_days)

    click = models.FeatureClick(
        user_id=user.id,
        feature_name=random.choice(features),
        timestamp=random_time,
    )

    db.add(click)

db.commit()

print("Feature clicks created.")
print("Seeding complete!")

db.close()