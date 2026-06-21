import requests
import time
from config import Config
from database import matches_col

def fetch_qualification_and_friendlies():
    # Define our targeted leagues
    leagues = {
        "10": "International Friendlies",
        "29": "WC Qualification Africa",
        "30": "WC Qualification Asia",
        "31": "WC Qualification CONCACAF",
        "32": "WC Qualification Europe",
        "33": "WC Qualification Oceania",
        "34": "WC Qualification South America"
    }
    
    # We loop through recent years to capture the entire qualification cycle
    seasons = ["2023", "2024", "2025", "2026"]
    
    headers = {
        "x-apisports-key": Config.API_KEY
    }

    total_saved = 0

    for league_id, league_name in leagues.items():
        print(f"\n--- Starting: {league_name} (ID: {league_id}) ---")
        
        for season in seasons:
            url = f"{Config.API_URL}/fixtures"
            querystring = {"league": league_id, "season": season}
            
            print(f"Fetching season {season}...")
            response = requests.get(url, headers=headers, params=querystring)
            
            if response.status_code == 200:
                data = response.json()
                fixtures = data.get("response", [])
                
                if fixtures:
                    saved_count = 0
                    for match in fixtures:
                        matches_col.update_one(
                            {"fixture.id": match["fixture"]["id"]},
                            {"$set": match},
                            upsert=True
                        )
                        saved_count += 1
                    print(f"-> Success: Found and stored {saved_count} matches.")
                    total_saved += saved_count
                else:
                    print(f"-> No fixtures found for season {season}.")
            else:
                print(f"-> Error {response.status_code} fetching league {league_id} for season {season}.")
                print(response.text)
                
            # 1-second pause to strictly respect free tier rate limits
            time.sleep(1)

    print(f"\n All data ingestion complete! Total matches stored in DB: {total_saved}")

if __name__ == "__main__":
    fetch_qualification_and_friendlies()