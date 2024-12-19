from flask import Flask, request, render_template, jsonify
from pyswip import Prolog # type: ignore
from nhl_api import fetch_player_data, generate_prolog_facts_for_teams
from prolog_service import add_facts_to_prolog, query_prolog_for_overlaps
from wikidata import query_sparql_endpoint, get_player_id


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/overlap", methods=['POST'])
def overlap():
    # Get player names from the request
    player1 = request.json.get('player1')
    player2 = request.json.get('player2')

    data = query_sparql_endpoint(player1, player2)
    player1Data = {}
    player2Data = {}

    for entry in data:
        # Extract player, league, team, and draft information
        player1 = entry['player1Label']['value'].replace("'", "\\'")
        league1 = entry['league1Label']['value'].replace("'", "\\'")
        team1 =  entry.get('team1Label', {}).get('value', '').replace("'", "\\'")
        draftTeam1 = entry.get('draftTeam1Label', {}).get('value', '').replace("'", "\\'")
        draftLeague1 = entry.get('draftLeague1Label', {}).get('value', '').replace("'", "\\'")
        draftYear1 = entry.get('draftYear1', {}).get('value', '').replace("'", "\\'")
        draftPosition1 = entry.get('draftPosition1', {}).get('value', '').replace("'", "\\'")

        player2 = entry['player2Label']['value'].replace("'", "\\'")
        league2 = entry['league2Label']['value'].replace("'", "\\'")
        team2 = entry['team2Label']['value'].replace("'", "\\'")
        draftTeam2 = entry.get('draftTeam2Label', {}).get('value', '').replace("'", "\\'")
        draftLeague2 = entry.get('draftLeague2Label', {}).get('value', '').replace("'", "\\'")
        draftYear2 = entry.get('draftYear2', {}).get('value', '').replace("'", "\\'")
        draftPosition2 = entry.get('draftPosition2', {}).get('value', '').replace("'", "\\'")

        player1Data = {
            "name": player1,
            "league": league1,
            "draftTeam": draftTeam1,
            "draftYear": draftYear1,
            "team": team1,
            "draftLeague": draftLeague1,
            "draftPosition": draftPosition1
        }
        # print(player1Data)
        player2Data = {
            "name": player2,
            "league": league2,
            "draftTeam": draftTeam2,
            "draftYear": draftYear2,
            "team": team2,
            "draftLeague": draftLeague2,
            "draftPosition": draftPosition2
        }
        # print(player2Data)


    # Initialize Prolog
    prolog = Prolog()
    prolog.consult("overlap_rules.pl")

    # Add facts dynamically
    add_facts_to_prolog(prolog, data)

    # Query Prolog for overlaps
    results = query_prolog_for_overlaps(prolog, player1, player2)

    # Return results
    return jsonify({
        "prolog_results": results,
        "player1": player1Data,
        "player2": player2Data
    })

# @app.route("/rivals", methods=['POST'])
# def rivals():
#     # Get player names from the request
#     player1 = request.json.get('player1')
#     player2 = request.json.get('player2')

#     data = get_player_id(player1, player2)
#     player1Id = data[0].get('nhlPlayerId1', {}).get('value', '').replace("'", "\\'")
#     player2Id = data[0].get('nhlPlayerId2', {}).get('value', '').replace("'", "\\'")
#     player1_name = data[0].get('player1Label', {}).get('value', '').replace("'", "\\'")
#     player2_name = data[0].get('player2Label', {}).get('value', '').replace("'", "\\'")

#     # Fetch season totals for both players
#     player1_season_totals = fetch_player_season_totals(player1Id)
#     player2_season_totals = fetch_player_season_totals(player2Id)

#     player1_team_facts = generate_prolog_facts_for_teams(player1_name, player1_season_totals)
#     player2_team_facts = generate_prolog_facts_for_teams(player2_name, player2_season_totals)

#     prolog = Prolog()
#     prolog.consult("rival_rules.pl")

#     # Add these facts to Prolog dynamically
#     for fact in player1_team_facts + player2_team_facts:
#         print(fact)
#         prolog.assertz(f"{fact}")

#     # Query Prolog for overlaps (existing logic)
#     query = f"in_rivalry('{player1_name}', '{player2_name}')"
#     result = list(prolog.query(query))
#     response = bool(result)

#     # Return overlaps as JSON
#     return jsonify({
#         "in_rivalry": response
#     })

@app.route("/rivals", methods=['POST'])
def rivals():
    # Get player names from the request
    player1 = request.json.get('player1')
    player2 = request.json.get('player2')

    data = get_player_id(player1, player2)
    player1Id = data[0].get('nhlPlayerId1', {}).get('value', '').replace("'", "\\'")
    player2Id = data[0].get('nhlPlayerId2', {}).get('value', '').replace("'", "\\'")
    player1_name = data[0].get('player1Label', {}).get('value', '').replace("'", "\\'")
    player2_name = data[0].get('player2Label', {}).get('value', '').replace("'", "\\'")

    # Fetch player data
    player1_data = fetch_player_data(player1Id)
    player2_data = fetch_player_data(player2Id)

    # Check rivalry using Prolog
    prolog = Prolog()
    prolog.consult("rival_rules.pl")

    # Add Prolog facts for each player
    if player1_data:
        player1_team_facts = generate_prolog_facts_for_teams(player1_name, player1_data["seasonStats"])
        for fact in player1_team_facts:
            prolog.assertz(fact)

    if player2_data:
        player2_team_facts = generate_prolog_facts_for_teams(player2_name, player2_data["seasonStats"])
        for fact in player2_team_facts:
            prolog.assertz(fact)

    # Query Prolog
    query = f"in_rivalry('{player1_name}', '{player2_name}')"
    result = list(prolog.query(query))
    rivalry_status = bool(result)

    # Return detailed data for the view
    return jsonify({
        "in_rivalry": rivalry_status,
        "player1": player1_data,
        "player2": player2_data,
    })


if __name__ == '__main__':
    app.run(debug=True)

