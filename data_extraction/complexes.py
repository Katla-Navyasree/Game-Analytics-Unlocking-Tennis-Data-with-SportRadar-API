import requests

API_KEY = "Ld7wEiJbJZYn69Y2A5DnZmSK7Ph3U7qcrTQU9tKm"
URL = "https://api.sportradar.com/tennis/trial/v3/en/complexes.json"

def fetch_complexes():
    response = requests.get(URL, params={"api_key": API_KEY})

    if response.status_code != 200:
        print("Access denied:", response.text)
        return [], []

    data = response.json()

    if "complexes" not in data:
        print("Unexpected format:", data)
        return [], []

    complexes = []
    venues = []

    for comp in data["complexes"]:
        complexes.append({
            "complex_id": comp["id"],
            "complex_name": comp["name"]
        })

        for v in comp.get("venues", []):
            venues.append({
                "venue_id": v["id"],
                "venue_name": v["name"],
                "city_name": v.get("city_name"),
                "country_name": v.get("country_name"),
                "country_code": v.get("country_code"),
                "timezone": v.get("timezone"),
                "complex_id": comp["id"]
            })

    return complexes, venues

if __name__ == "__main__":
    complexes,venues = fetch_complexes()
    print(f"Fetched {len(complexes)} complexes")
    print(f"Fetched {len(venues)} venues")