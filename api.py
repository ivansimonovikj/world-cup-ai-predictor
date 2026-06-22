from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # Added this import!
from pydantic import BaseModel
from database import client
from predict_custom import get_prediction_logic
from fastapi.responses import FileResponse

app = FastAPI()

# 1. Enable CORS so your index.html can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Define the expected data format for the prediction
class MatchPrediction(BaseModel):
    team_a: str
    team_b: str

# 3. Matches endpoint
@app.get("/matches")
def get_matches(date: str):
    db = client['world_cup_db']
    matches_col = db['all_matches']
    return {"matches": list(matches_col.find({"date": date}, {"_id": 0}))}

# 4. Prediction endpoint (Changed to POST)
@app.post("/predict")
def predict(match: MatchPrediction):
    return get_prediction_logic(match.team_a, match.team_b)

# 5. Serve the main HTML page at the root URL
@app.get("/")
def serve_homepage():
    return FileResponse("static/index.html")

# 6. Serve the CSS and JS assets under a dedicated /static path
app.mount("/static", StaticFiles(directory="static"), name="static")