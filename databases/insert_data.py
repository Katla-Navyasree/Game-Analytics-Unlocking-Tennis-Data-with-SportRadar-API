import mysql.connector
import sys
import os

# Add the parent folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_extraction.competitions import fetch_competitions
from data_extraction.complexes import fetch_complexes
from data_extraction.rankings import fetch_rankings


# Connect to MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Santosh@1428",
    database="tennis_db"
)
cursor = conn.cursor()

# Fetch data from API
print("📡 Fetching competitions...")
categories, competitions = fetch_competitions()
print("Categories:", len(categories))
print("Competitions:", len(competitions))

print("📡 Fetching complexes...")
complexes, venues = fetch_complexes()
print("Complexes:", len(complexes))
print("Venues:", len(venues))

print("📡 Fetching rankings...")
competitors, rankings = fetch_rankings()
print("Competitors:", len(competitors))
print("Rankings:", len(rankings))

# --------------------
# Insert Categories
# --------------------
for c in categories:
    cursor.execute(
        "INSERT IGNORE INTO Categories (category_id, category_name) VALUES (%s, %s)",
        (c["category_id"], c["category_name"])
    )

# --------------------
# Insert Competitions
# --------------------
for c in competitions:
    cursor.execute(
        """
        INSERT IGNORE INTO Competitions
        (competition_id, competition_name, parent_id, type, gender, category_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            c["competition_id"],
            c["competition_name"],
            c["parent_id"],
            c["type"],
            c["gender"],
            c["category_id"]
        )
    )

# --------------------
# Insert Complexes
# --------------------
for c in complexes:
    cursor.execute(
        "INSERT IGNORE INTO Complexes (complex_id, complex_name) VALUES (%s, %s)",
        (c["complex_id"], c["complex_name"])
    )

# --------------------
# Insert Venues
# --------------------
for v in venues:
    cursor.execute(
        """
        INSERT IGNORE INTO Venues
        (venue_id, venue_name, city_name, country_name, country_code, timezone, complex_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            v["venue_id"],
            v["venue_name"],
            v["city_name"],
            v["country_name"],
            v["country_code"],
            v["timezone"],
            v["complex_id"]
        )
    )

# --------------------
# Insert Competitors
# --------------------
for c in competitors:
    cursor.execute(
        """
        INSERT IGNORE INTO Competitors
        (competitor_id, name, country, country_code, abbreviation)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            c["competitor_id"],
            c["name"],
            c.get("country"),
            c.get("country_code"),
            c.get("abbreviation")
        )
    )

# --------------------
# Insert Competitor Rankings
# --------------------
for r in rankings:
    cursor.execute(
        """
        INSERT INTO Competitor_Rankings
        (rank1, movement, points, competitions_played, competitor_id)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            r.get("rank"),
            r.get("movement"),
            r.get("points"),
            r.get("competitions_played"),
            r.get("competitor_id")
        )
    )

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("✅ DATA INSERTION COMPLETE")
