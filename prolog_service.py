
def add_facts_to_prolog(prolog, data):
    # Initialize sets to avoid duplication
    played_in_league_facts = set()
    played_in_team_facts = set()
    drafted_by_facts = set()
    drafted_in_league_facts = set()
    was_in_draft_facts = set()

    for entry in data:
        # Extract player, league, team, and draft information
        player1 = entry['player1Label']['value'].replace("'", "\\'")
        league1 = entry['league1Label']['value'].replace("'", "\\'")
        team1 = entry.get('team1Label', {}).get('value', '').replace("'", "\\'")
        draftTeam1 = entry.get('draftTeam1Label', {}).get('value', '').replace("'", "\\'")
        draftLeague1 = entry.get('draftLeague1Label', {}).get('value', '').replace("'", "\\'")
        draftYear1 = entry.get('draftYear1', {}).get('value', '').replace("'", "\\'")

        player2 = entry['player2Label']['value'].replace("'", "\\'")
        league2 = entry['league2Label']['value'].replace("'", "\\'")
        team2 = entry.get('team2Label', {}).get('value', '').replace("'", "\\'")
        draftTeam2 = entry.get('draftTeam2Label', {}).get('value', '').replace("'", "\\'")
        draftLeague2 = entry.get('draftLeague2Label', {}).get('value', '').replace("'", "\\'")
        draftYear2 = entry.get('draftYear2', {}).get('value', '').replace("'", "\\'")

        # Add played_in_league facts
        played_in_league_facts.add(f"played_in_league('{player1}', '{league1}')")
        played_in_league_facts.add(f"played_in_league('{player2}', '{league2}')")

        # Add played_in_team facts (if team data is available)
        if team1:
            played_in_team_facts.add(f"played_in_team('{player1}', '{team1}')")
        if team2:
            played_in_team_facts.add(f"played_in_team('{player2}', '{team2}')")

        # Add drafted_by facts (if draft data is available)
        if draftTeam1:
            drafted_by_facts.add(f"drafted_by('{player1}', '{draftTeam1}')")
        if draftTeam2:
            drafted_by_facts.add(f"drafted_by('{player2}', '{draftTeam2}')")
       
        # Add drafted_in_league facts (if draft data is available)
        if draftLeague1:
            drafted_in_league_facts.add(f"drafted_in_league('{player1}', '{draftLeague1}')")
        if draftLeague2:
            drafted_in_league_facts.add(f"drafted_in_league('{player2}', '{draftLeague2}')")

        # Add was_in_draft facts (if draft data is available)
        if draftYear1:
            was_in_draft_facts.add(f"was_in_draft('{player1}', '{draftLeague1}', '{draftYear1}')")
        if draftYear2:
            was_in_draft_facts.add(f"was_in_draft('{player2}', '{draftLeague2}', '{draftYear2}')")

    # Assert facts into Prolog
    for fact in played_in_league_facts:
        # print(f"Adding fact: {fact}")
        prolog.assertz(fact)  # No trailing period
    for fact in played_in_team_facts:
        # print(f"Adding fact: {fact}")
        prolog.assertz(fact)  # No trailing period
    for fact in drafted_by_facts:
        # print(f"Adding fact: {fact}")
        prolog.assertz(fact)  # No trailing period
    for fact in drafted_in_league_facts:
        # print(f"Adding fact: {fact}")
        prolog.assertz(fact)  # No trailing period
    for fact in was_in_draft_facts:
        # print(f"Adding fact: {fact}")
        prolog.assertz(fact)  # No trailing period

def query_prolog_for_overlaps(prolog, player1, player2):
    # Query Prolog for overlap rules
    overlap_league = list(prolog.query(f"is_overlap_league('{player1}', '{player2}')"))
    overlap_team = list(prolog.query(f"is_overlap_team('{player1}', '{player2}')"))
    overlap_draft_team = list(prolog.query(f"is_overlap_draft_team('{player1}', '{player2}')"))
    overlap_draft_league = list(prolog.query(f"is_overlap_draft_league('{player1}', '{player2}')"))
    was_in_same_draft = list(prolog.query(f"was_in_same_draft('{player1}', '{player2}')"))

    return {
        "same_league": bool(overlap_league),
        "same_team": bool(overlap_team),
        "same_draft_team": bool(overlap_draft_team),
        "drafted_same_league": bool(overlap_draft_league),
        "same_draft": bool(was_in_same_draft)
    }

