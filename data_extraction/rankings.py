import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("SPORTSRADAR_API_KEY")

if not API_KEY:
    raise ValueError("SPORTSRADAR_API_KEY is not set in the environment")

URL = "https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json"

HEADERS = {
    "accept": "application/json",
    "x-api-key": API_KEY
}


def fetch_rankings():
    """
    Fetch tennis rankings from Sportradar API.
    Works with trial keys (may only return limited data).
    Returns:
        competitors: list of competitor dicts
        rankings: list of ranking dicts
    """
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)

        if response.status_code == 403:
            print("Error 403: Forbidden. Check your API key or endpoint.")
            return [], []

        if response.status_code == 404:
            print("Error 404: Not Found. Endpoint may not exist for your key.")
            return [], []

        response.raise_for_status()
        data = response.json()

    except requests.RequestException as e:
        print("Request failed:", e)
        return [], []

    competitors = []
    rankings = []

    # Loop through all returned rankings
    for ranking in data.get("rankings", []):
        ranking_id = ranking.get("id", "")
        ranking_name = ranking.get("name", "")

        for r in ranking.get("competitor_rankings", []):
            comp = r.get("competitor", {})

            competitors.append({
                "competitor_id": comp.get("id"),
                "name": comp.get("name"),
                "country": comp.get("country"),
                "country_code": comp.get("country_code"),
                "abbreviation": comp.get("abbreviation")
            })

            rankings.append({
                "ranking_id": ranking_id,
                "ranking_name": ranking_name,
                "rank": r.get("rank"),
                "movement": r.get("movement"),
                "points": r.get("points"),
                "competitions_played": r.get("competitions_played"),
                "competitor_id": comp.get("id")
            })

    return competitors, rankings


if __name__ == "__main__":
    competitors, rankings = fetch_rankings()
    print(f"Fetched {len(competitors)} competitors")
    print(f"Fetched {len(rankings)} rankings")

    print("\nSample competitors:")
    for c in competitors[:5]:
        print(c)

    print("\nSample rankings:")
    for r in rankings[:5]:
        print(r)
