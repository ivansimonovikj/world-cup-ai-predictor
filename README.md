# 🏆 World Cup AI Predictor

**Live Demo:** [world-cup-ai-predictor.onrender.com](https://world-cup-ai-predictor.onrender.com/)

> A full-stack, AI-driven sports analytics platform that predicts match outcomes, win probabilities, and goal metrics using an ensemble machine learning architecture.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=flat&logo=mongodb&logoColor=white)](https://www.mongodb.com/)

---

## 💡 The "Elevator Pitch"

Most basic sports predictors rely on simple statistical averages. This application utilizes a **probabilistic machine learning ensemble** to neutralize home-field bias, calculate Expected Goals (xG), and generate actionable betting-style insights (Both Teams To Score, Over 2.5 Goals). It features a fully decoupled architecture, with a Python ML backend serving a mobile-first, responsive vanilla JavaScript frontend.

## 🏗️ Architecture & Tech Stack

The application is built with a clear separation of concerns, ensuring scalability and maintainability:

- **Intelligence Layer (Machine Learning):** `scikit-learn` (RandomForestClassifier & RandomForestRegressor), `pandas`, `numpy`.
- **API & Routing Layer:** `FastAPI`, `Uvicorn` / `Gunicorn` (for production WSGI management).
- **Data Layer:** `MongoDB` (Cloud-hosted via Atlas), `pymongo`, `certifi`.
- **Presentation Layer:** Mobile-first HTML5, CSS3 (CSS Grid/Flexbox), and asynchronous Vanilla JavaScript (ES6+).

## 🚀 Core Features

- **Dual-Perspective Inference:** Calculates predictions from two separate dataframes (Team A as Home vs. Team B as Home) and averages the probabilities to eliminate dataset bias.
- **Real-Time Data Serving:** Asynchronous database querying to fetch daily match schedules and historic head-to-head (H2H) forms.
- **Dynamic Analytics Dashboard:** Users can trigger ML inferences on demand, dynamically rendering win probabilities and goal statistics without page reloads.
- **Responsive UI/UX:** Grid-based layout that seamlessly reflows from multi-column desktop views to single-column mobile interfaces.

## 🧠 Engineering Challenges & Solutions

1. **Handling Algorithmic Bias in Sports Data:** \* _Challenge:_ Training data inherently favors the "Home" team, skewing predictions for neutral-venue tournaments like the World Cup.
   - _Solution:_ Engineered the inference pipeline to run every matchup twice (swapping home/away designations) and averaged the `predict_proba()` outputs to create a strictly neutral baseline.
2. **Production-Ready API Connectivity:** \* _Challenge:_ Transitioning from a local `127.0.0.1` environment to a cloud deployment without breaking frontend data fetching or facing CORS blockages.
   - _Solution:_ Implemented dynamic environment detection in the frontend (`window.location.hostname`) to automatically route API calls, and configured strict FastAPI CORS middleware for production security.
3. **Optimizing DOM Performance:** \* _Challenge:_ Rendering complex prediction dashboards dynamically can lead to layout shifts and sluggish UI.
   - _Solution:_ Utilized efficient DOM delegation, asynchronous `fetch` requests with proper state management (loading indicators, error handling), and localized CSS ID targeting to ensure instantaneous UI updates.

## ⚙️ Local Setup & Installation

Follow these steps to run the application locally:

### 1. Clone Repository

```bash
git clone https://github.com/ivansimonovikj/world-cup-ai-predictor.git
cd world-cup-ai-predictor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Setup

Create a .env file in the project root:

```env
MONGO_URI=your_mongodb_connection_string
```

### 4. Run Backend

```bash
uvicorn api:app --reload
```

### 5. Run Frontend

Open index.html in your browser or use a live server.
