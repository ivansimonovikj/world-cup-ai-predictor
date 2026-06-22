import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from database import matches_col
from engineer_features import prepare_training_data
import warnings
import csv
from datetime import datetime

warnings.filterwarnings('ignore')

# --- 1. LOAD DATA & TRAIN MODELS (Executed once on import) ---
print("Loading historical data and training the AI Brains...")
df = prepare_training_data()

features = [
    'home_form_scored', 'home_form_conceded',
    'away_form_scored', 'away_form_conceded',
    'h2h_home_win_rate',
    'home_overall_strength', 'away_overall_strength'
]

X = df[features]
clf_model = RandomForestClassifier(n_estimators=100, random_state=42).fit(X, df['result'])
reg_home_model = RandomForestRegressor(n_estimators=100, random_state=42).fit(X, df['home_goals'])
reg_away_model = RandomForestRegressor(n_estimators=100, random_state=42).fit(X, df['away_goals'])
print("All models trained successfully!\n")

# --- 2. HELPER FUNCTIONS ---
def get_team_id(team_name):
    match = matches_col.find_one({"teams.home.name": {"$regex": f"^{team_name}$", "$options": "i"}})
    if match: return match['teams']['home']['id'], match['teams']['home']['name']
    match = matches_col.find_one({"teams.away.name": {"$regex": f"^{team_name}$", "$options": "i"}})
    if match: return match['teams']['away']['id'], match['teams']['away']['name']
    return None, None

def get_current_form(team_id):
    past = df[(df['home_team_id'] == team_id) | (df['away_team_id'] == team_id)].tail(5)
    if len(past) == 0: return 0.0, 0.0
    scored = sum(row['home_goals'] if row['home_team_id'] == team_id else row['away_goals'] for _, row in past.iterrows())
    conceded = sum(row['away_goals'] if row['home_team_id'] == team_id else row['home_goals'] for _, row in past.iterrows())
    return scored / len(past), conceded / len(past)

def get_h2h(team_a, team_b):
    past_h2h = df[(((df['home_team_id'] == team_a) & (df['away_team_id'] == team_b)) |
                    ((df['home_team_id'] == team_b) & (df['away_team_id'] == team_a)))]
    if len(past_h2h) == 0: return 0.5
    a_wins = sum(1 for _, row in past_h2h.iterrows() if 
                 (row['home_team_id'] == team_a and row['result'] == 2) or 
                 (row['away_team_id'] == team_a and row['result'] == 0))
    return a_wins / len(past_h2h)

def get_strength(team_id):
    past = df[(df['home_team_id'] == team_id) | (df['away_team_id'] == team_id)]
    if len(past) == 0: return 0.0
    wins = sum(1 for _, row in past.iterrows() if 
               (row['home_team_id'] == team_id and row['result'] == 2) or 
               (row['away_team_id'] == team_id and row['result'] == 0))
    return wins / len(past)

def log_prediction(team_a, team_b, prediction, prob_a, prob_b, prob_draw):
    with open('ai_predictions_log.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(['Date', 'Team A', 'Team B', 'Prediction', 'Prob A', 'Prob B', 'Prob Draw'])
        writer.writerow([datetime.now().strftime("%Y-%m-%d"), team_a, team_b, prediction, prob_a, prob_b, prob_draw])

# --- 3. THE PREDICTION LOGIC ---
def get_prediction_logic(team_a_name, team_b_name):
    team_a_id, team_a_name = get_team_id(team_a_name)
    team_b_id, team_b_name = get_team_id(team_b_name)

    if not team_a_id or not team_b_id:
        return {"error": "Team not found"}

    a_scored, a_conceded = get_current_form(team_a_id)
    b_scored, b_conceded = get_current_form(team_b_id)
    a_strength = get_strength(team_a_id)
    b_strength = get_strength(team_b_id)

    # Scenarios
    h2h_1 = get_h2h(team_a_id, team_b_id)
    s1 = pd.DataFrame([{'home_form_scored': a_scored, 'home_form_conceded': a_conceded, 'away_form_scored': b_scored, 'away_form_conceded': b_conceded, 'h2h_home_win_rate': h2h_1, 'home_overall_strength': a_strength, 'away_overall_strength': b_strength}])
    
    h2h_2 = get_h2h(team_b_id, team_a_id)
    s2 = pd.DataFrame([{'home_form_scored': b_scored, 'home_form_conceded': b_conceded, 'away_form_scored': a_scored, 'away_form_conceded': a_conceded, 'h2h_home_win_rate': h2h_2, 'home_overall_strength': b_strength, 'away_overall_strength': a_strength}])
    
    prob_1, prob_2 = clf_model.predict_proba(s1)[0], clf_model.predict_proba(s2)[0]
    goals_a_s1, goals_b_s1 = reg_home_model.predict(s1)[0], reg_away_model.predict(s1)[0]
    goals_b_s2, goals_a_s2 = reg_home_model.predict(s2)[0], reg_away_model.predict(s2)[0]

    fA = (prob_1[2] + prob_2[0]) / 2
    fD = (prob_1[1] + prob_2[1]) / 2
    fB = (prob_1[0] + prob_2[2]) / 2
    xG_A, xG_B = (goals_a_s1 + goals_a_s2) / 2, (goals_b_s1 + goals_b_s2) / 2
    total_g = xG_A + xG_B

    margin = 0.05
    diff = abs(fA - fB)

    if fD > fA and fD > fB:
        pred = "Draw"
    elif fA > fB and diff <= margin:
        pred = f"{team_a_name} Wins or Draw"
    elif fB > fA and diff <= margin:
        pred = f"{team_b_name} Wins or Draw"
    elif fA > fB:
        pred = f"{team_a_name} Wins"
    elif fB > fA:
        pred = f"{team_b_name} Wins"
    else:
        pred = "Draw"

    log_prediction(team_a_name, team_b_name, pred, round(fA*100, 1), round(fB*100, 1), round(fD*100, 1))

    return {
        "matchup": f"{team_a_name} vs {team_b_name}", 
        "prob_a": round(fA*100, 1), 
        "prob_b": round(fB*100, 1),
        "prob_draw": round(fD*100, 1), 
        "btts": "YES" if (xG_A > 1.25 and xG_B > 1.25) else "NO",
        "over_2_5": "YES" if total_g > 2.8 else "NO", 
        "prediction": pred
    }