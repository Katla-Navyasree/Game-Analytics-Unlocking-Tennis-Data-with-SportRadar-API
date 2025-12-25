import requests

API_KEY = "Ld7wEiJbJZYn69Y2A5DnZmSK7Ph3U7qcrTQU9tKm"
URL = "https://api.sportradar.com/tennis/trial/v3/en/competitions.json"

def fetch_competitions():
    response = requests.get(URL, params={"api_key": API_KEY})
    response.raise_for_status()
    data = response.json()

    categories_dict = {}
    competitions = []

    for comp in data.get("competitions", []):
        category = comp.get("category", {})

        # Collect unique categories
        if category:
            categories_dict[category["id"]] = {
                "category_id": category["id"],
                "category_name": category["name"]
            }

        competitions.append({
            "competition_id": comp["id"],
            "competition_name": comp["name"],
            "parent_id": comp.get("parent_id"),
            "type": comp.get("type"),
            "gender": comp.get("gender"),
            "level": comp.get("level"),
            "category_id": category.get("id"),
        })

    categories = list(categories_dict.values())
    return categories, competitions


if __name__ == "__main__":
    categories, competitions = fetch_competitions()
    print(f"Fetched {len(categories)} categories")
    print(f"Fetched {len(competitions)} competitions")
