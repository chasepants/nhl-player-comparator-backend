import requests

# def fetch_player_season_totals(player_id):
#     """
#     Fetch season totals for a player from the NHL API.
#     """
#     url = f"https://api-web.nhle.com/v1/player/{player_id}/landing"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         return data.get('seasonTotals', [])
#     else:
#         print(f"Failed to fetch data for player {player_id}: {response.status_code}")
#         return []

def fetch_player_data(player_id):
    """
    Fetch detailed player data including profile info and season stats.
    """
    url = f"https://api-web.nhle.com/v1/player/{player_id}/landing"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        first_name = data.get("firstName", []).get("default", "Unknown")
        last_name  = data.get("lastName", []).get("default", "Unknown")

        # Extract necessary fields
        profile = {
            "profilePicture": data.get("headshot", ""),
            "name": f"{first_name} {last_name}",
            "age": data.get("birthDate", "Unknown"),
            "weight": data.get("weightInPounds", "Unknown"),
            "isActive": data.get("isActive", False),
        }
        season_stats = data.get("seasonTotals", [])
        return {"profile": profile, "seasonStats": season_stats}

    print(f"Failed to fetch data for player {player_id}: {response.status_code}")
    return None


def generate_prolog_facts_for_teams(player_name, season_totals):
    """
    Generate Prolog facts for the teams a player has played for, including the seasons.
    """
    facts = []
    for season in season_totals:
        team_name = season['teamName']['default'].replace("'", "\\'")
        start_season = str(season['season'])[:4]
        end_season = str(season['season'])[4:]
        print(f"played_for('{player_name}', '{team_name}', {start_season}, {end_season}).")
        facts.append(f"played_for('{player_name}', '{team_name}', {start_season}, {end_season})")
    return facts

