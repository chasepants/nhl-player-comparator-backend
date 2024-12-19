rival('Anaheim Ducks', 'Los Angeles Kings').
rival('Anaheim Ducks', 'San Jose Sharks').
rival('Boston Bruins', 'Montreal Canadiens').
rival('Boston Bruins', 'Toronto Maple Leafs').
rival('Chicago Blackhawks', 'Detroit Red Wings').
rival('Calgary Flames', 'Edmonton Oilers').
rival('Edmonton Oilers', 'Calgary Flames').
rival('New York Rangers', 'New York Islanders').
rival('New York Rangers', 'New Jersey Devils').
rival('Pittsburgh Penguins', 'Washington Capitals').
rival('Vegas Golden Knights', 'Colorado Avalanche').

in_rivalry(Player1, Player2) :-
    played_for(Player1, Team1, Start1, End1),
    played_for(Player2, Team2, Start2, End2),
    rival(Team1, Team2),
    overlapping_period(Start1, End1, Start2, End2),
    !.

in_rivalry(Player1, Player2) :-
    played_for(Player1, Team1, Start1, End1),
    played_for(Player2, Team2, Start2, End2),
    rival(Team2, Team1),
    overlapping_period(Start1, End1, Start2, End2),
    !.

overlapping_period(Start1, End1, Start2, End2) :-
    Start1 =< End2,
    Start2 =< End1.
