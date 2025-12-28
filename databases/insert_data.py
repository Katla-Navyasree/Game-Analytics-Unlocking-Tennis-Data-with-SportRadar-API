from supabase_client import supabase

from data_extraction.competitions import fetch_competitions
from data_extraction.complexes import fetch_complexes
from data_extraction.rankings import fetch_rankings

# --------------------
# Fetch data
# --------------------
print("📡 Fetching competitions...")
categories, competitions = fetch_competitions()

print("📡 Fetching complexes...")
complexes, venues = fetch_complexes()

print("📡 Fetching rankings...")
competitors, rankings = fetch_rankings()

# --------------------
# Insert Categories
# --------------------
supabase.table("categories").upsert(
    [
        {
            "category_id": c["category_id"],
            "category_name": c["category_name"]
        }
        for c in categories
    ]
).execute()

# --------------------
# Insert Competitions
# --------------------
supabase.table("competitions").upsert(
    [
        {
            "competition_id": c["competition_id"],
            "competition_name": c["competition_name"],
            "parent_id": c["parent_id"],
            "type": c["type"],
            "gender": c["gender"],
            "category_id": c["category_id"]
        }
        for c in competitions
    ]
).execute()

# --------------------
# Insert Complexes
# --------------------
supabase.table("complexes").upsert(
    [
        {
            "complex_id": c["complex_id"],
            "complex_name": c["complex_name"]
        }
        for c in complexes
    ]
).execute()

# --------------------
# Insert Venues
# --------------------
supabase.table("venues").upsert(
    [
        {
            "venue_id": v["venue_id"],
            "venue_name": v["venue_name"],
            "city_name": v["city_name"],
            "country_name": v["country_name"],
            "country_code": v["country_code"],
            "timezone": v["timezone"],
            "complex_id": v["complex_id"]
        }
        for v in venues
    ]
).execute()

# --------------------
# Insert Competitors
# --------------------
supabase.table("competitors").upsert(
    [
        {
            "competitor_id": c["competitor_id"],
            "name": c["name"],
            "country": c.get("country"),
            "country_code": c.get("country_code"),
            "abbreviation": c.get("abbreviation")
        }
        for c in competitors
    ]
).execute()

# --------------------
# Insert Rankings
# --------------------
supabase.table("competitor_rankings").insert(
    [
        {
            "rank": r.get("rank"),
            "movement": r.get("movement"),
            "points": r.get("points"),
            "competitions_played": r.get("competitions_played"),
            "competitor_id": r.get("competitor_id")
        }
        for r in rankings
    ]
).execute()

print("✅ DATA INSERTION COMPLETE (Supabase)")
