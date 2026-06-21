import pandas as pd
from database import matches_col

def prepare_training_data():
    print("Extracting matches from MongoDB...")
    
    cursor = matches_col.find({"fixture.status.short": "FT"})
    matches = list(cursor)
    
    if len(matches) == 0:
        return None

    data = []
    for m in matches:
        home_goals = m['goals']['home']
        away_goals = m['goals']['away']
        
        # Target Variable: 0 = Away Win, 1 = Draw, 2 = Home Win
        if home_goals > away_goals: result = 2
        elif home_goals == away_goals: result = 1
        else: result = 0

        data.append({
            'fixture_id': m['fixture']['id'],
            'date': m['fixture']['date'],
            'home_team_id': m['teams']['home']['id'],
            'away_team_id': m['teams']['away']['id'],
            'home_team': m['teams']['home']['name'],
            'away_team': m['teams']['away']['name'],
            'home_goals': home_goals,
            'away_goals': away_goals,
            'result': result
        })

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], format='ISO8601')
    df = df.sort_values('date').reset_index(drop=True)
    
    print(f"Loaded {len(df)} matches. Engineering advanced features...")

    # --- FEATURE 1: Recent Form (Last 5 Matches) ---
    def get_recent_form(team_id, current_date, window=5):
        past = df[((df['home_team_id'] == team_id) | (df['away_team_id'] == team_id)) & (df['date'] < current_date)].tail(window)
        if len(past) == 0: return 0.0, 0.0
        scored = sum(row['home_goals'] if row['home_team_id'] == team_id else row['away_goals'] for _, row in past.iterrows())
        conceded = sum(row['away_goals'] if row['home_team_id'] == team_id else row['home_goals'] for _, row in past.iterrows())
        return scored / len(past), conceded / len(past)

    # --- FEATURE 2: Head-to-Head Win Rate ---
    def get_h2h_rate(home_id, away_id, current_date):
        past_h2h = df[
            (((df['home_team_id'] == home_id) & (df['away_team_id'] == away_id)) |
             ((df['home_team_id'] == away_id) & (df['away_team_id'] == home_id))) &
            (df['date'] < current_date)
        ]
        if len(past_h2h) == 0: return 0.5 # Neutral if they've never played
        
        home_team_wins = sum(1 for _, row in past_h2h.iterrows() if 
                             (row['home_team_id'] == home_id and row['result'] == 2) or 
                             (row['away_team_id'] == home_id and row['result'] == 0))
        return home_team_wins / len(past_h2h)

    # --- FEATURE 3: All-Time Win Rate (Strength Proxy) ---
    def get_all_time_win_rate(team_id, current_date):
        past = df[((df['home_team_id'] == team_id) | (df['away_team_id'] == team_id)) & (df['date'] < current_date)]
        if len(past) == 0: return 0.0
        wins = sum(1 for _, row in past.iterrows() if 
                   (row['home_team_id'] == team_id and row['result'] == 2) or 
                   (row['away_team_id'] == team_id and row['result'] == 0))
        return wins / len(past)

    # Apply all functions
    features = []
    for index, row in df.iterrows():
        h_score, h_conc = get_recent_form(row['home_team_id'], row['date'])
        a_score, a_conc = get_recent_form(row['away_team_id'], row['date'])
        h2h_win_rate = get_h2h_rate(row['home_team_id'], row['away_team_id'], row['date'])
        h_strength = get_all_time_win_rate(row['home_team_id'], row['date'])
        a_strength = get_all_time_win_rate(row['away_team_id'], row['date'])
        
        features.append({
            'home_form_scored': h_score, 'home_form_conceded': h_conc,
            'away_form_scored': a_score, 'away_form_conceded': a_conc,
            'h2h_home_win_rate': h2h_win_rate,
            'home_overall_strength': h_strength,
            'away_overall_strength': a_strength
        })

    # Join the new features to the original dataframe
    features_df = pd.DataFrame(features)
    df = pd.concat([df, features_df], axis=1)

    print("\nFinal Shape for scikit-learn:", df.shape)
    return df

if __name__ == "__main__":
    prepare_training_data()