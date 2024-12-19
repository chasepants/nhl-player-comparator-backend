% Rules
is_overlap_league(Player1, Player2) :-
    played_in_league(Player1, League),
    played_in_league(Player2, League).

is_overlap_team(Player1, Player2) :-
    played_in_team(Player1, Team),
    played_in_team(Player2, Team).

is_overlap_draft_team(Player1, Player2) :-
    drafted_by(Player1, Team),
    drafted_by(Player2, Team).

is_overlap_draft_league(Player1, Player2) :-
    drafted_in_league(Player1, League),
    drafted_in_league(Player2, League).

was_in_same_draft(Player1, Player2) :-
    was_in_draft(Player1, League, Date),
    was_in_draft(Player2, League, Date).

% Facts to be added at runtime