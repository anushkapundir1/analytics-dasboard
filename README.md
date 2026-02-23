# 📊 Analytics Dashboard

Full-Stack Analytics Tracking System built with **FastAPI (Backend)** and **React + Vite (Frontend)**.

---

## 🌍 Live Deployment

**Frontend (Vercel)**  
https://analytics-dashboard-eight-topaz.vercel.app/

**Backend API (Render)**  
https://analytics-dashboard-hgqs.onrender.com

**Swagger API Docs**  
https://analytics-dashboard-hgqs.onrender.com/docs

---

## 🛠 Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- SQLite (PostgreSQL recommended for production)
- JWT Authentication
- Uvicorn
- Render

### Frontend
- React (Vite)
- Recharts
- Axios
- React Router
- js-cookie
- Vercel

---

## ✨ Features

### 🔐 Authentication
- User Registration
- Login with JWT
- Protected routes
- Logout functionality

### 📊 Analytics
- Feature click tracking
- Filter usage tracking
- Bar Chart (feature counts)
- Line Chart (time-based trends)
- Interactive chart updates

### 🎛 Filters
- Date filter
- Age group filter (<18, 18-40, >40)
- Gender filter (Male, Female, Other)
- Persistent filters via cookies

### 🌙 UI
- Dark Mode toggle
- Responsive layout
- Interactive charts

---

## 📂 Project Structure

```
root/
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── schemas.py
│   ├── auth.py
│   ├── seed.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    ├── public/
    ├── package.json
    └── vite.config.js
```

---

## 🖥 Backend Setup (Local)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Runs at:

```
http://127.0.0.1:8000
```

Swagger docs:

```
http://127.0.0.1:8000/docs
```

---

## 🌐 Frontend Setup (Local)

```bash
cd frontend
npm install
npm run dev
```

Runs at:

```
http://localhost:5173
```

---

## 🌱 Data Seeding (Required)

To populate the database with dummy analytics data:

```bash
cd backend
python seed.py
```

This script generates 50–100 sample feature interaction records across different users and dates so the dashboard does not appear empty on first load.

---

## 🔑 API Endpoints

| Method | Endpoint     | Description |
|--------|-------------|-------------|
| POST   | /register   | Register user |
| POST   | /login      | Login & receive JWT |
| POST   | /track      | Track interactions (Protected) |
| GET    | /analytics  | Get aggregated analytics data (Protected) |

---

## 🔐 Authentication Flow

1. User registers  
2. User logs in  
3. Backend returns JWT token  
4. Token stored in localStorage  
5. Token sent in header:

```
Authorization: Bearer <token>
```

6. Backend validates token before serving analytics.

---

## 🏗 Architectural Choices

- **FastAPI** was chosen for high performance and automatic API documentation via Swagger.
- **SQLAlchemy ORM** ensures clean separation between models and database logic.
- **JWT authentication** provides stateless and secure session management.
- **React + Vite** enables fast frontend development and optimized builds.
- **Recharts** provides interactive and customizable data visualizations.
- Filters are stored in cookies to preserve user state across refreshes.
- Deployment split into:
  - Backend on Render
  - Frontend on Vercel

---

## ⚡ Scaling Strategy (1M Write Events Per Minute)

If this dashboard needed to handle 1 million write-events per minute, the backend architecture would transition from a simple synchronous write model to an event-driven system. SQLite would be replaced with PostgreSQL or a distributed database. Incoming tracking requests would be pushed into a message queue such as Kafka or Redis Streams, allowing background workers to batch-process and store events efficiently. A caching layer like Redis would be introduced for frequently accessed analytics data. The system would be horizontally scaled behind a load balancer to distribute traffic across multiple instances, and proper indexing and partitioning strategies would be implemented to maintain efficient aggregation queries.

---

## 🚀 Deployment Architecture

```
GitHub Repository
        │
        ├── Backend → Render
        └── Frontend → Vercel
```

---

## ✅ Status

✔ Backend deployed  
✔ Frontend deployed  
✔ Authentication working  
✔ Analytics tracking working  
✔ Data seeding included  
✔ Production-ready setup
