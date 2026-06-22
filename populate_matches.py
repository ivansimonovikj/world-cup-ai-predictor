from pymongo import MongoClient
from database import client # Ensure this imports your existing MongoClient

# 1. Setup the connection
db = client['world_cup_db']
matches_col = db['all_matches']

matches_col.delete_many({})
print("Previous data wiped clean!")

# 2. The Group Stage Data
group_stage_data = [
  {"date": "2026-06-21", "team_a": "Spain", "team_b": "Saudi Arabia", "kickoff_et": "12:00 PM", "stadium": "Atlanta Stadium"},
  {"date": "2026-06-21", "team_a": "Belgium", "team_b": "Iran", "kickoff_et": "3:00 PM", "stadium": "Los Angeles Stadium"},
  {"date": "2026-06-21", "team_a": "Uruguay", "team_b": "Cape Verde", "kickoff_et": "6:00 PM", "stadium": "Miami Stadium"},
  {"date": "2026-06-21", "team_a": "New Zealand", "team_b": "Egypt", "kickoff_et": "9:00 PM", "stadium": "BC Place Vancouver"},
  {"date": "2026-06-22", "team_a": "Argentina", "team_b": "Austria", "kickoff_et": "1:00 PM", "stadium": "Dallas Stadium"},
  {"date": "2026-06-22", "team_a": "France", "team_b": "Iraq", "kickoff_et": "5:00 PM", "stadium": "Philadelphia Stadium"},
  {"date": "2026-06-22", "team_a": "Norway", "team_b": "Senegal", "kickoff_et": "8:00 PM", "stadium": "New York/New Jersey Stadium"},
  {"date": "2026-06-22", "team_a": "Jordan", "team_b": "Algeria", "kickoff_et": "11:00 PM", "stadium": "San Francisco Bay Area Stadium"},
  {"date": "2026-06-23", "team_a": "Portugal", "team_b": "Uzbekistan", "kickoff_et": "1:00 PM", "stadium": "Houston Stadium"},
  {"date": "2026-06-23", "team_a": "England", "team_b": "Ghana", "kickoff_et": "4:00 PM", "stadium": "Boston Stadium"},
  {"date": "2026-06-23", "team_a": "Panama", "team_b": "Croatia", "kickoff_et": "7:00 PM", "stadium": "Toronto Stadium"},
  {"date": "2026-06-23", "team_a": "Colombia", "team_b": "DR Congo", "kickoff_et": "10:00 PM", "stadium": "Guadalajara Stadium"},
  {"date": "2026-06-24", "team_a": "Switzerland", "team_b": "Canada", "kickoff_et": "3:00 PM", "stadium": "BC Place Vancouver"},
  {"date": "2026-06-24", "team_a": "Bosnia & Herzegovina", "team_b": "Qatar", "kickoff_et": "3:00 PM", "stadium": "Seattle Stadium"},
  {"date": "2026-06-24", "team_a": "Scotland", "team_b": "Brazil", "kickoff_et": "6:00 PM", "stadium": "Miami Stadium"},
  {"date": "2026-06-24", "team_a": "Morocco", "team_b": "Haiti", "kickoff_et": "6:00 PM", "stadium": "Atlanta Stadium"},
  {"date": "2026-06-24", "team_a": "Mexico", "team_b": "Czechia", "kickoff_et": "9:00 PM", "stadium": "Mexico City Stadium"},
  {"date": "2026-06-24", "team_a": "South Korea", "team_b": "South Africa", "kickoff_et": "9:00 PM", "stadium": "Monterrey Stadium"},
  {"date": "2026-06-25", "team_a": "Curaçao", "team_b": "Ivory Coast", "kickoff_et": "4:00 PM", "stadium": "Philadelphia Stadium"},
  {"date": "2026-06-25", "team_a": "Ecuador", "team_b": "Germany", "kickoff_et": "4:00 PM", "stadium": "New York/New Jersey Stadium"},
  {"date": "2026-06-25", "team_a": "Tunisia", "team_b": "Netherlands", "kickoff_et": "7:00 PM", "stadium": "Kansas City Stadium"},
  {"date": "2026-06-25", "team_a": "Japan", "team_b": "Sweden", "kickoff_et": "7:00 PM", "stadium": "Dallas Stadium"},
  {"date": "2026-06-25", "team_a": "USA", "team_b": "Türkiye", "kickoff_et": "10:00 PM", "stadium": "Los Angeles Stadium"},
  {"date": "2026-06-25", "team_a": "Paraguay", "team_b": "Australia", "kickoff_et": "10:00 PM", "stadium": "San Francisco Bay Area Stadium"},
  {"date": "2026-06-26", "team_a": "Norway", "team_b": "France", "kickoff_et": "3:00 PM", "stadium": "Boston Stadium"},
  {"date": "2026-06-26", "team_a": "Senegal", "team_b": "Iraq", "kickoff_et": "3:00 PM", "stadium": "Toronto Stadium"},
  {"date": "2026-06-26", "team_a": "Uruguay", "team_b": "Spain", "kickoff_et": "8:00 PM", "stadium": "Guadalajara Stadium"},
  {"date": "2026-06-26", "team_a": "Cape Verde", "team_b": "Saudi Arabia", "kickoff_et": "8:00 PM", "stadium": "Houston Stadium"},
  {"date": "2026-06-26", "team_a": "New Zealand", "team_b": "Belgium", "kickoff_et": "11:00 PM", "stadium": "BC Place Vancouver"},
  {"date": "2026-06-26", "team_a": "Egypt", "team_b": "Iran", "kickoff_et": "11:00 PM", "stadium": "Seattle Stadium"},
  {"date": "2026-06-27", "team_a": "Panama", "team_b": "England", "kickoff_et": "5:00 PM", "stadium": "New York/New Jersey Stadium"},
  {"date": "2026-06-27", "team_a": "Croatia", "team_b": "Ghana", "kickoff_et": "5:00 PM", "stadium": "Philadelphia Stadium"},
  {"date": "2026-06-27", "team_a": "Colombia", "team_b": "Portugal", "kickoff_et": "7:30 PM", "stadium": "Miami Stadium"},
  {"date": "2026-06-27", "team_a": "DR Congo", "team_b": "Uzbekistan", "kickoff_et": "7:30 PM", "stadium": "Atlanta Stadium"},
  {"date": "2026-06-27", "team_a": "Algeria", "team_b": "Austria", "kickoff_et": "10:00 PM", "stadium": "Kansas City Stadium"},
  {"date": "2026-06-27", "team_a": "Jordan", "team_b": "Argentina", "kickoff_et": "10:00 PM", "stadium": "Dallas Stadium"}
]

# 3. Add to the collection
matches_col.insert_many(group_stage_data)
print(f"Successfully added {len(group_stage_data)} matches to the 'all_matches' collection!")