from database import matches_col
from datetime import datetime, timezone

def insert_batch_matches():
    # List of the completed 2026 World Cup matches

    matches_col.delete_many({}) 
    print("Old data wiped successfully.")

    matches = [
        {"home": "Mexico", "away": "South Africa", "home_g": 2, "away_g": 0},
        {"home": "South Korea", "away": "Czechia", "home_g": 2, "away_g": 1},
        {"home": "Canada", "away": "Bosnia & Herzegovina", "home_g": 1, "away_g": 1},
        {"home": "USA", "away": "Paraguay", "home_g": 4, "away_g": 1},
        {"home": "Qatar", "away": "Switzerland", "home_g": 1, "away_g": 1},
        {"home": "Brazil", "away": "Morocco", "home_g": 1, "away_g": 1},
        {"home": "Haiti", "away": "Scotland", "home_g": 0, "away_g": 1},
        {"home": "Australia", "away": "Türkiye", "home_g": 2, "away_g": 0},
        {"home": "Germany", "away": "Curaçao", "home_g": 7, "away_g": 1},
        {"home": "Ivory Coast", "away": "Ecuador", "home_g": 1, "away_g": 0},
        {"home": "Netherlands", "away": "Japan", "home_g": 2, "away_g": 2},
        {"home": "Sweden", "away": "Tunisia", "home_g": 5, "away_g": 1},
        {"home": "Belgium", "away": "Egypt", "home_g": 1, "away_g": 1},
        {"home": "Iran", "away": "New Zealand", "home_g": 2, "away_g": 2},
        {"home": "Spain", "away": "Cape Verde", "home_g": 0, "away_g": 0},
        {"home": "Saudi Arabia", "away": "Uruguay", "home_g": 1, "away_g": 1},
        {"home": "France", "away": "Senegal", "home_g": 3, "away_g": 1},
        {"home": "Norway", "away": "Iraq", "home_g": 4, "away_g": 1},
        {"home": "Argentina", "away": "Algeria", "home_g": 3, "away_g": 0},
        {"home": "Austria", "away": "Jordan", "home_g": 3, "away_g": 1},
        {"home": "Portugal", "away": "DR Congo", "home_g": 1, "away_g": 1},
        {"home": "Uzbekistan", "away": "Colombia", "home_g": 1, "away_g": 3},
        {"home": "England", "away": "Croatia", "home_g": 4, "away_g": 2},
        {"home": "Ghana", "away": "Panama", "home_g": 1, "away_g": 0},
        {"home": "Czechia", "away": "South Africa", "home_g": 1, "away_g": 1},
        {"home": "Switzerland", "away": "Bosnia & Herzegovina", "home_g": 4, "away_g": 1},
        {"home": "Canada", "away": "Qatar", "home_g": 6, "away_g": 0},
        {"home": "Mexico", "away": "South Korea", "home_g": 1, "away_g": 0},
        {"home": "USA", "away": "Australia", "home_g": 2, "away_g": 0},
        {"home": "Scotland", "away": "Morocco", "home_g": 0, "away_g": 1},
        {"home": "Brazil", "away": "Haiti", "home_g": 3, "away_g": 0},
        {"home": "Türkiye", "away": "Paraguay", "home_g": 0, "away_g": 1},
        {"home": "Netherlands", "away": "Sweden", "home_g": 5, "away_g": 1},
        {"home": "Germany", "away": "Ivory Coast", "home_g": 2, "away_g": 1},
        {"home": "Ecuador", "away": "Curaçao", "home_g": 0, "away_g": 0},
        {"home": "Tunisia", "away": "Japan", "home_g": 0, "away_g": 4}
    ]

    print(f"Starting batch injection of {len(matches)} matches...")
    
    # We need to map names to IDs. This logic assumes your DB already has these teams from the qualifiers!
    # If the script errors, it means the team name doesn't match the one in your DB exactly.
    for i, m in enumerate(matches):
        # Look up an existing match to steal the team IDs
        existing = matches_col.find_one({"teams.home.name": m["home"]}) or \
                   matches_col.find_one({"teams.away.name": m["home"]})
        
        # Fallback: if not found, we use a placeholder ID (the model will still learn from the outcome)
        h_id = existing["teams"]["home"]["id"] if existing and existing["teams"]["home"]["name"] == m["home"] else 9000 + i
        a_id = 9001 + i

        match_doc = {
            "fixture": {"id": 80000 + i, "date": datetime.now(timezone.utc).isoformat(), "status": {"short": "FT"}},
            "teams": {"home": {"id": h_id, "name": m["home"]}, "away": {"id": a_id, "name": m["away"]}},
            "goals": {"home": m["home_g"], "away": m["away_g"]}
        }
        
        matches_col.update_one({"fixture.id": match_doc["fixture"]["id"]}, {"$set": match_doc}, upsert=True)
        print(f"Injected: {m['home']} {m['home_g']}-{m['away_g']} {m['away']}")

    print("Batch injection complete!")

if __name__ == "__main__":
    insert_batch_matches()