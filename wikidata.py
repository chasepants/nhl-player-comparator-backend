from SPARQLWrapper import SPARQLWrapper, JSON

def query_sparql_endpoint(player1, player2):
    # Initialize SPARQLWrapper
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    # Define the SPARQL query
    query = f"""
        SELECT DISTINCT

        ?player1Label ?player1Description ?league1Label ?league1StartTime ?league1EndTime ?team1Label 
        ?team1StartTime ?team1EndTime ?League ?draftTeam1Label ?draftPosition1 ?draftYear1 ?draftLeague1Label
        
        ?player2Label ?player2Description ?league2Label ?league2StartTime ?league2EndTime ?team2Label 
        ?team2StartTime ?team2EndTime ?draftTeam2Label ?draftPosition2 ?draftYear2 ?draftLeague2Label
        
        WHERE {{  
            # Player 1 Information
            ?player1 ?label "{player1}"@en.  
            ?player1 wdt:P31 wd:Q5 .

            # League Participation for Player 1
            ?player1 p:P118 ?leagueStatement1.
            ?leagueStatement1 ps:P118 ?league1.
            OPTIONAL {{ ?leagueStatement1 pq:P580 ?league1StartTime. }}
            OPTIONAL {{ ?leagueStatement1 pq:P582 ?league1EndTime. }}
            
            # Team Participation for Player 1
            ?player1 p:P54 ?teamStatement1.
            ?teamStatement1 ps:P54 ?team1.
            OPTIONAL {{ ?teamStatement1 pq:P580 ?team1StartTime. }}
            OPTIONAL {{ ?teamStatement1 pq:P582 ?team1EndTime. }}

            # Draft Information for Player 1
            OPTIONAL {{
                ?player1 p:P647 ?draftStatement1.  # Retrieve the draftedBy statement.
                ?draftStatement1 ps:P647 ?draftTeam1.  # Draft team.
        
                # Qualifiers: Draft Year and Position
                OPTIONAL {{ ?draftStatement1 pq:P585 ?draftYear1. }}      # Draft year.
                OPTIONAL {{ ?draftStatement1 pq:P1836 ?draftPosition1. }} # Draft position.
                OPTIONAL {{ ?draftTeam1 wdt:P118 ?draftLeague1. }}  # League associated with the team.
            }}

            # Wikipedia article for Player 1
            ?article schema:about ?player1 .
            ?article schema:inLanguage "en" .
            ?article schema:isPartOf <https://en.wikipedia.org/>.
            
            # Player 2 Information
            ?player2 ?label "{player2}"@en.  
            ?player2 wdt:P31 wd:Q5 .

            # League Participation for Player 2
            ?player2 p:P118 ?leagueStatement2.
            ?leagueStatement2 ps:P118 ?league2.
            OPTIONAL {{ ?leagueStatement2 pq:P580 ?league2StartTime. }}
            OPTIONAL {{ ?leagueStatement2 pq:P582 ?league2EndTime. }}

            # Team Participation for Player 2
            ?player2 p:P54 ?teamStatement2.
            ?teamStatement2 ps:P54 ?team2.
            OPTIONAL {{ ?teamStatement2 pq:P580 ?team2StartTime. }}
            OPTIONAL {{ ?teamStatement2 pq:P582 ?team2EndTime. }}

            # Draft Information for Player 2
            OPTIONAL {{
                ?player2 p:P647 ?draftStatement2.  # Retrieve the draftedBy statement.
                ?draftStatement2 ps:P647 ?draftTeam2.  # Draft team.
        
                # Qualifiers: Draft Year and Position
                OPTIONAL {{ ?draftStatement2 pq:P585 ?draftYear2. }}      # Draft year.
                OPTIONAL {{ ?draftStatement2 pq:P1836 ?draftPosition2. }} # Draft position.
                OPTIONAL {{ ?draftTeam2 wdt:P118 ?draftLeague2. }}  # League associated with the team.
            }}

            # Wikipedia article for Player 2
            ?article2 schema:about ?player2 .
            ?article2 schema:inLanguage "en" .
            ?article2 schema:isPartOf <https://en.wikipedia.org/>. 

            # Include labels for readable results
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
    """

    # Execute the query
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    # Parse the results
    return results['results']['bindings']

def get_player_id(player1, player2):
    # Initialize SPARQLWrapper
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    # Define the SPARQL query
    query = f"""
        SELECT DISTINCT ?player1Label ?player2Label ?nhlPlayerId1 ?nhlPlayerId2
        WHERE {{  
            # Player 1 Information
            ?player1 ?label "{player1}"@en.  
            ?player1 wdt:P31 wd:Q5 .
            ?player1 wdt:P3522 ?nhlPlayerId1.  # NHL.com Player ID for Player 1

            # Wikipedia article for Player 1
            ?article schema:about ?player1 .
            ?article schema:inLanguage "en" .
            ?article schema:isPartOf <https://en.wikipedia.org/>.
            
            # Player 2 Information
            ?player2 ?label "{player2}"@en.  
            ?player2 wdt:P31 wd:Q5 .
            ?player2 wdt:P3522 ?nhlPlayerId2.  # NHL.com Player ID for Player 1

            # Wikipedia article for Player 2
            ?article2 schema:about ?player2 .
            ?article2 schema:inLanguage "en" .
            ?article2 schema:isPartOf <https://en.wikipedia.org/>. 

            # Include labels for readable results
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
    """

    # Execute the query
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    # Parse the results
    return results['results']['bindings']