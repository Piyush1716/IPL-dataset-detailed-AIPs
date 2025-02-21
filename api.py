import pandas as pd

df_del = pd.read_csv('cleaned_del.csv')
df_match = pd.read_csv('cleaned_match.csv')

# teams
def teams():
    teams = set(df_match['team1']) | set(df_match['team2'])
    return {'teams' : list(teams)}

# total matches over seasons
def total_matches_over_seasons():
    res = df_match['season'].value_counts()
    return {'seasons' : res.to_dict()}

# matches hosted by each city
def matches_hosted_by_each_city():
    res = df_match['city'].value_counts()
    return {'seasons' : res.to_dict()}

# Average Target Runs by Season
def avg_target_by_season():
    return df_match.groupby('season')['target_runs'].mean().to_dict()

# Function to get player performance stats
# Function to get player performance stats
def player_performance(player_name):
    player_data = df_del[(df_del['batter'] == player_name) | (df_del['bowler'] == player_name)]
    
    if player_data.empty:
        return {"error": "Player not found or no data available"}
    
    # Batting Stats
    batting_data = df_del[df_del['batter'] == player_name]
    total_runs = batting_data['batsman_runs'].sum()
    balls_faced = len(batting_data)
    strike_rate = round((total_runs / balls_faced) * 100, 2) if balls_faced > 0 else 0
    boundaries = batting_data[batting_data['batsman_runs'].isin([4, 6])]['batsman_runs'].count()
    
    # Bowling Stats
    bowling_data = df_del[df_del['bowler'] == player_name]
    total_wickets = bowling_data[bowling_data['is_wicket'] == 1]['is_wicket'].count()
    runs_conceded = bowling_data['total_runs'].sum()
    balls_bowled = len(bowling_data)
    economy_rate = round((runs_conceded / (balls_bowled / 6)), 2) if balls_bowled > 0 else 0
    
    return {
        "player": player_name,
        "batting": {
            "total_runs": int(total_runs),
            "balls_faced": balls_faced,
            "strike_rate": int(strike_rate),
            "boundaries": int(boundaries)
        },
        "bowling": {
            "total_wickets": int(total_wickets),
            "runs_conceded": int(runs_conceded),
            "balls_bowled": balls_bowled,
            "economy_rate": int(economy_rate)
        }
    }

# Function to get player performance against a specific team
def player_vs_team(player_name, team_name):
    player_data = df_del[(df_del['batter'] == player_name) & (df_del['bowling_team'] == team_name)]
    
    if player_data.empty:
        return {"error": "No data available for this player against the specified team"}
    
    # Batting Stats
    total_runs = player_data['batsman_runs'].sum()
    balls_faced = len(player_data)
    strike_rate = round((total_runs / balls_faced) * 100, 2) if balls_faced > 0 else 0
    boundaries = player_data[player_data['batsman_runs'].isin([4, 6])]['batsman_runs'].value_counts().to_dict()
    
    # Bowling Stats
    bowling_data = df_del[(df_del['bowler'] == player_name) & (df_del['batting_team'] == team_name)]
    total_wickets = bowling_data[bowling_data['is_wicket'] == 1]['is_wicket'].count()
    runs = [bowling_data['batsman_runs'].sum(), bowling_data['extra_runs'].sum()]
    runs_conceded = {
        'runs' :  int(runs[0]),
        'extra' : int(runs[1]),
        'total' : int(sum(runs))
    }
    balls_bowled = len(bowling_data)
    economy_rate = round((sum(runs) / (balls_bowled / 6)), 2) if balls_bowled > 0 else 0
    
    return {
        "player": player_name,
        "against_team": team_name,
        "batting": {
            "total_runs": int(total_runs),
            "balls_faced": balls_faced,
            "strike_rate": float(strike_rate),
            "boundaries": boundaries
        },
        "bowling": {
            "total_wickets": int(total_wickets),
            "runs_conceded": runs_conceded,
            "balls_bowled": balls_bowled,
            "economy_rate": float(economy_rate)
        }
    }

# inning-wise statistics
# 1. Powerplay, Middle, and Death Overs Analysis in inning
def match_innings_1(match_id):
    match_data = df_del[df_del['match_id'] == match_id]
    
    if match_data.empty:
        return {"error": "Match ID not found"}
    
    innings_stats = {}
    for inning in match_data['inning'].unique():
        inning_data = match_data[match_data['inning'] == inning]
        team = inning_data.iloc[0]['batting_team']
        total_runs = inning_data['total_runs'].sum()
        wickets = inning_data[inning_data['is_wicket'] == 1].shape[0]
        
        # Calculate run rate using min and max over numbers
        min_over = inning_data['over'].min()
        max_over = inning_data['over'].max()
        overs_played = max_over - min_over + 1  # +1 to include both min and max overs
        run_rate = round(total_runs / overs_played, 2) if overs_played > 0 else 0
        
        # Phase-wise analysis
        powerplay_data = inning_data[inning_data['over'].between(0, 5)]  # Overs 0-5 (Powerplay)
        middle_data = inning_data[inning_data['over'].between(6, 14)]    # Overs 6-14 (Middle)
        death_data = inning_data[inning_data['over'].between(15, 19)]    # Overs 15-19 (Death)
        
        # Calculate overs played in each phase
        powerplay_overs = powerplay_data['over'].max() - powerplay_data['over'].min() + 1 if not powerplay_data.empty else 0
        middle_overs = middle_data['over'].max() - middle_data['over'].min() + 1 if not middle_data.empty else 0
        death_overs = death_data['over'].max() - death_data['over'].min() + 1 if not death_data.empty else 0
        
        phase_stats = {
            "powerplay": {
                "runs": powerplay_data['total_runs'].sum(),
                "wickets": powerplay_data[powerplay_data['is_wicket'] == 1].shape[0],
                "run_rate": round(powerplay_data['total_runs'].sum() / powerplay_overs, 2) if powerplay_overs > 0 else 0
            },
            "middle": {
                "runs": middle_data['total_runs'].sum(),
                "wickets": middle_data[middle_data['is_wicket'] == 1].shape[0],
                "run_rate": round(middle_data['total_runs'].sum() / middle_overs, 2) if middle_overs > 0 else 0
            },
            "death": {
                "runs": death_data['total_runs'].sum(),
                "wickets": death_data[death_data['is_wicket'] == 1].shape[0],
                "run_rate": round(death_data['total_runs'].sum() / death_overs, 2) if death_overs > 0 else 0
            }
        }
        
        innings_stats[inning] = {
            "batting_team": team,
            "total_runs": total_runs,
            "wickets": wickets,
            "run_rate": run_rate,
            "phase_stats": phase_stats
        }
    
    return {"match_id": match_id, "innings": innings_stats}

# 2. inning Top Performers
def match_innings_2(match_id):
    match_data = df_del[df_del['match_id'] == match_id]
    
    if match_data.empty:
        return {"error": "Match ID not found"}
    
    innings_stats = {}
    for inning in match_data['inning'].unique():
        inning_data = match_data[match_data['inning'] == inning]
        team = inning_data.iloc[0]['batting_team']
        total_runs = inning_data['total_runs'].sum()
        wickets = inning_data[inning_data['is_wicket'] == 1].shape[0]
        run_rate = round(total_runs / (max(inning_data['over'])) + 1, 2) if max(inning_data['over']) > 0 else 0
        
        # Top batsman
        top_batsman = inning_data.groupby('batter')['batsman_runs'].sum().idxmax()
        top_batsman_runs = inning_data.groupby('batter')['batsman_runs'].sum().max()
        
        # Top bowler
        top_bowler = inning_data.groupby('bowler')['is_wicket'].sum().idxmax()
        top_bowler_wickets = inning_data.groupby('bowler')['is_wicket'].sum().max()
        
        innings_stats[inning] = {
            "batting_team": team,
            "total_runs": total_runs,
            "wickets": wickets,
            "run_rate": run_rate,
            "top_batsman": {
                "name": top_batsman,
                "runs": top_batsman_runs
            },
            "top_bowler": {
                "name": top_bowler,
                "wickets": top_bowler_wickets
            }
        }
    
    return {"match_id": match_id, "innings": innings_stats}

# 3. inning Boundary Analysis
def match_innings_3(match_id):
    match_data = df_del[df_del['match_id'] == match_id]
    
    if match_data.empty:
        return {"error": "Match ID not found"}
    
    innings_stats = {}
    for inning in match_data['inning'].unique():
        inning_data = match_data[match_data['inning'] == inning]
        team = inning_data.iloc[0]['batting_team']
        total_runs = inning_data['total_runs'].sum()
        wickets = inning_data[inning_data['is_wicket'] == 1].shape[0]
        run_rate = round(total_runs / (max(inning_data['over']) + 1), 2) if max(inning_data['over']) > 0 else 0
        
        # Boundary analysis
        fours = inning_data[inning_data['batsman_runs'] == 4].shape[0]
        sixes = inning_data[inning_data['batsman_runs'] == 6].shape[0]
        boundary_runs = (fours * 4) + (sixes * 6)
        boundary_percentage = round((boundary_runs / total_runs) * 100, 2) if total_runs > 0 else 0
        
        innings_stats[int(inning)] = {
            "batting_team": team,
            "total_runs": int(total_runs),
            "wickets": wickets,
            "run_rate": float(run_rate),
            "boundaries": {
                "fours": fours,
                "sixes": sixes,
                "boundary_runs": boundary_runs,
                "boundary_percentage": float(boundary_percentage)
            }
        }
    
    return {"match_id": match_id, "innings": innings_stats}

# 4. inning vise Fall of Wickets
def match_innings_4(match_id):
    match_data = df_del[df_del['match_id'] == match_id]
    
    if match_data.empty:
        return {"error": "Match ID not found"}
    
    innings_stats = {}
    for inning in match_data['inning'].unique():
        inning_data = match_data[match_data['inning'] == inning]
        
        # Calculate cumulative runs for each ball
        inning_data['cumulative_runs'] = inning_data['total_runs'].cumsum()
        
        team = inning_data.iloc[0]['batting_team']
        total_runs = inning_data.iloc[-1,-1]
        wickets = inning_data[inning_data['is_wicket'] == 1].shape[0]
        run_rate = round(total_runs / (max(inning_data['over']) + 1), 2) if max(inning_data['over']) > 0 else 0
        
        # Fall of wickets
        fall_of_wickets = inning_data[inning_data['is_wicket'] == 1][['over', 'ball', 'player_dismissed', 'cumulative_runs']]
        fall_of_wickets = fall_of_wickets.rename(columns={'cumulative_runs': 'total_runs'})
        fall_of_wickets = fall_of_wickets.to_dict(orient='records')
        
        innings_stats[int(inning)] = {
            "batting_team": team,
            "total_runs": int(total_runs),
            "wickets": wickets,
            "run_rate": float(run_rate),
            "fall_of_wickets": fall_of_wickets
        }
    
    return {"match_id": match_id, "innings": innings_stats}


# inning vise Partnership Analysis
def match_innings_5(match_id):
    match_data = df_del[df_del['match_id'] == match_id]
    
    if match_data.empty:
        return {"error": "Match ID not found"}
    
    innings_stats = {}
    for inning in match_data['inning'].unique():
        inning_data = match_data[match_data['inning'] == inning]
        team = inning_data.iloc[0]['batting_team']
        total_runs = inning_data['total_runs'].sum()
        wickets = inning_data[inning_data['is_wicket'] == 1].shape[0]
        run_rate = round(total_runs / (max(inning_data['over'])) + 1, 2) if max(inning_data['over']) > 0 else 0
        
        # Partnership analysis
        partnerships = []
        current_partnership = {"batsmen": [], "runs": 0, "balls": 0}
        for _, ball in inning_data.iterrows():
            if ball['is_wicket'] == 1:
                partnerships.append(current_partnership)
                current_partnership = {"batsmen": [], "runs": 0, "balls": 0}
            else:
                current_partnership["batsmen"] = list(set(current_partnership["batsmen"] + [ball['batter'], ball['non_striker']]))
                current_partnership["runs"] += ball['total_runs']
                current_partnership["balls"] += 1
        
        # Add the last partnership
        if current_partnership["runs"] > 0:
            partnerships.append(current_partnership)
        
        # Sort partnerships by runs
        partnerships = sorted(partnerships, key=lambda x: x['runs'], reverse=True)
        
        innings_stats[int(inning)] = {
            "batting_team": team,
            "total_runs": int(total_runs),
            "wickets": wickets,
            "run_rate": float(run_rate),
            "partnerships": partnerships
        }
    
    return {"match_id": match_id, "innings": innings_stats}
    
def get_all_partnerships():
    all_partnerships = []
    
    # Iterate through all matches
    for match_id in df_del['match_id'].unique():
        match_data = df_del[df_del['match_id'] == match_id]
        
        # Iterate through all innings in the match
        for inning in match_data['inning'].unique():
            inning_data = match_data[match_data['inning'] == inning]
            team = inning_data.iloc[0]['batting_team']
            
            # Initialize partnership tracking
            partnerships = []
            current_partnership = {"batsmen": set(), "runs": 0, "balls": 0}
            
            # Iterate through each ball in the inning
            for _, ball in inning_data.iterrows():
                if ball['is_wicket'] == 1:
                    # Finalize the current partnership
                    current_partnership["batsmen"] = list(current_partnership["batsmen"])  # Convert set to list
                    partnerships.append(current_partnership)
                    # Start a new partnership
                    current_partnership = {"batsmen": set(), "runs": 0, "balls": 0}
                else:
                    # Update the current partnership
                    current_partnership["batsmen"].add(ball['batter'])
                    current_partnership["batsmen"].add(ball['non_striker'])
                    current_partnership["runs"] += ball['total_runs']
                    current_partnership["balls"] += 1
            
            # Add the last partnership if it exists
            if current_partnership["runs"] > 0:
                current_partnership["batsmen"] = list(current_partnership["batsmen"])  # Convert set to list
                partnerships.append(current_partnership)
            
            # Append partnerships to the all_partnerships list
            for partnership in partnerships:
                all_partnerships.append({
                    "match_id": int(match_id),
                    "inning": int(inning),
                    "batting_team": team,
                    "batsmen": partnership["batsmen"],
                    "runs": partnership["runs"],
                    "balls": partnership["balls"]
                })
    
    return all_partnerships

def batsman_vs_bowler(batsman, bowler):
    # Filter deliveries where the batsman faced the bowler
    filtered_data = df_del[
        (df_del['batter'] == batsman) & 
        (df_del['bowler'] == bowler)
    ]
    
    if filtered_data.empty:
        return {"error": "No data found for this combination"}
    
    # Calculate stats
    total_runs = filtered_data['batsman_runs'].sum()
    total_balls = len(filtered_data)
    dismissals = filtered_data['is_wicket'].sum()
    strike_rate = (total_runs / total_balls) * 100 if total_balls > 0 else 0
    average = total_runs / dismissals if dismissals > 0 else total_runs
    
    # Dismissal types
    dismissal_types = filtered_data[filtered_data['is_wicket'] == 1]['dismissal_kind'].value_counts().to_dict()
    
    return {
        "batsman": batsman,
        "bowler": bowler,
        "total_runs": int(total_runs),
        "total_balls": total_balls,
        "dismissals": int(dismissals),
        "strike_rate": float(round(strike_rate, 2)),
        "average": float(round(average, 2)),
        "dismissal_types": dismissal_types}

def player_dismissal_analysis(player_name):
    # Filter deliveries where the player was dismissed
    dismissals = df_del[
        (df_del['player_dismissed'] == player_name) & 
        (df_del['is_wicket'] == 1)
    ]
    
    if dismissals.empty:
        return {"error": "No dismissals found for this player"}
    
    # Count dismissal types
    dismissal_types = dismissals['dismissal_kind'].value_counts().to_dict()
    
    return {
        "player": player_name,
        "total_dismissals": len(dismissals),
        "dismissal_types": dismissal_types
    }

def player_performance_by_phase(player_name, phase):
    # Define phase overs
    
    # Overs 0-5 (Powerplay)
    # Overs 6-14 (Middle)
    # Overs 15-19 (Death)
    
    if phase == "powerplay":
        overs = range(0, 5)
    elif phase == "middle":
        overs = range(6, 14)
    elif phase == "death":
        overs = range(15, 19)
    else:
        return {"error": "Invalid phase. Use 'powerplay', 'middle', or 'death'"}
    
    # Filter deliveries for the player in the specified phase
    phase_data = df_del[
        (df_del['batter'] == player_name) & 
        (df_del['over'].isin(overs))
    ]
    
    if phase_data.empty:
        return {"error": "No data found for this player in the specified phase"}
    
    # Calculate stats
    total_runs = phase_data['batsman_runs'].sum()
    total_balls = len(phase_data)
    boundaries = len(phase_data[phase_data['batsman_runs'].isin([4, 6])])
    strike_rate = (total_runs / total_balls) * 100 if total_balls > 0 else 0
    
    return {
        "player": player_name,
        "phase": phase,
        "total_runs": int(total_runs),
        "total_balls": total_balls,
        "boundaries": boundaries,
        "strike_rate": float(round(strike_rate, 2))
    }

def team_phase_stats(team, phase, role="batting"):
    # Define phase overs
    if phase == "powerplay":
        overs = range(0, 5)
    elif phase == "middle":
        overs = range(6, 14)
    elif phase == "death":
        overs = range(15, 19)
    else:
        return {"error": "Invalid phase. Use 'powerplay', 'middle', or 'death'"}
    
    # Filter data based on role (batting or bowling)
    if role == "batting":
        filtered_data = df_del[
            (df_del['batting_team'] == team) & 
            (df_del['over'].isin(overs))
        ]
        total_runs = filtered_data['total_runs'].sum()
        total_balls = len(filtered_data)
        boundaries = len(filtered_data[filtered_data['batsman_runs'].isin([4, 6])])
        strike_rate = (total_runs / total_balls) * 100 if total_balls > 0 else 0
        wickets_lost = filtered_data['is_wicket'].sum()
        
        return {
            "team": team,
            "phase": phase,
            "role": role,
            "total_runs": int(total_runs),
            "total_balls": total_balls,
            "boundaries": boundaries,
            "strike_rate": float(round(strike_rate, 2)),
            "wickets_lost": int(wickets_lost)
        }
    
    elif role == "bowling":
        filtered_data = df_del[
            (df_del['bowling_team'] == team) & 
            (df_del['over'].isin(overs))
        ]
        total_runs_conceded = filtered_data['total_runs'].sum()
        total_balls = len(filtered_data)
        wickets_taken = filtered_data['is_wicket'].sum()
        economy_rate = (total_runs_conceded / total_balls) * 6 if total_balls > 0 else 0
        
        return {
            "team": team,
            "phase": phase,
            "role": role,
            "total_runs_conceded": int(total_runs_conceded),
            "total_balls": total_balls,
            "wickets_taken": int(wickets_taken),
            "economy_rate": float(round(economy_rate, 2))
        }
    
    else:
        return {"error": "Invalid role. Use 'batting' or 'bowling'"}

def team_home_vs_away(team, home_venue):
    # Filter home matches
    home_matches = df_match[
        ((df_match['team1'] == team) | (df_match['team2'] == team)) & 
        (df_match['venue'] == home_venue)
    ]
    home_wins = len(home_matches[home_matches['winner'] == team])
    
    # Filter away matches
    away_matches = df_match[
        ((df_match['team1'] == team) | (df_match['team2'] == team)) & 
        (df_match['venue'] != home_venue)
    ]
    away_wins = len(away_matches[away_matches['winner'] == team])
    
    return {
        "team": team,
        "home_venue": home_venue,
        "home_matches": len(home_matches),
        "home_wins": home_wins,
        "away_matches": len(away_matches),
        "away_wins": away_wins
    }
    
# Distribution of Match Results
def match_won_analysis():
    result_counts = df_match['result'].value_counts().to_dict()
    
    # Total matches
    total_matches = sum(result_counts.values())
    
    # Extract values safely
    win_by_runs = result_counts.get('runs', 0)
    win_by_wickets = result_counts.get('wickets', 0)
    tie_matches = result_counts.get('tie', 0)
    no_result_matches = result_counts.get('no result', 0)

    # Calculate percentages
    percent_by_runs = round((win_by_runs / total_matches) * 100, 2) if total_matches else 0
    percent_by_wickets = round((win_by_wickets / total_matches) * 100, 2) if total_matches else 0
    percent_tie = round((tie_matches / total_matches) * 100, 2) if total_matches else 0
    percent_no_result = round((no_result_matches / total_matches) * 100, 2) if total_matches else 0

    return {
        "total_matches": total_matches,
        "win_by_wickets": {
            "count": win_by_wickets,
            "percentage": percent_by_wickets
        },
        "win_by_runs": {
            "count": win_by_runs,
            "percentage": percent_by_runs
        },
        "tie": {
            "count": tie_matches,
            "percentage": percent_tie
        },
        "no_result": {
            "count": no_result_matches,
            "percentage": percent_no_result
        }
    }
    
# Result Margin Distribution
def result_margin_distribution():
    # Extract margins
    margin_wins_by_runs = df_match[df_match['result'] == 'runs']['result_margin'].dropna().astype(int)
    margin_wins_by_wickets = df_match[df_match['result'] == 'wickets']['result_margin'].dropna().astype(int)

    # Define bins for runs (0-10, 10-20, ..., 90-100, 100+)
    run_bins = list(range(0, 141, 10))  # 0-10, 10-20, ..., 130-140
    run_bins.append(float('inf'))  # 140+

    # Group runs into bins
    run_labels = [f"{run_bins[i]}-{run_bins[i+1] - 1}" if run_bins[i+1] != float('inf') else "140+" for i in range(len(run_bins)-1)]
    run_distribution = pd.cut(margin_wins_by_runs, bins=run_bins, labels=run_labels, right=False).value_counts().sort_index()

    # Count wickets directly using value_counts()
    wicket_distribution = margin_wins_by_wickets.value_counts().sort_index()

    return {
        "win_by_runs": run_distribution.to_dict(),
        "win_by_wickets": wicket_distribution.to_dict()
    }
# Matches Won by Toss Decision
def matches_won_by_toss_decision():
    """
    Analyzes the relationship between toss decisions and match outcomes.

    Returns:
        pd.DataFrame: A DataFrame containing:
            - toss_decision (str): The decision made after winning the toss ("bat" or "field").
            - wins (int): Number of matches won by teams that won the toss and chose this decision.
            - total_matches (int): Total matches where teams made this toss decision.
            - percentage (float): Win percentage for each toss decision.

    The function filters matches where the toss-winning team also won the match, 
    then calculates the win count and percentage for each toss decision.
    """
    
    # Filter matches where the toss winner is also the match winner
    toss_winner_wins = df_match[df_match['toss_winner'] == df_match['winner']]

    # Groups matches by toss_decision (bat or field).
    # Counts how many times a team won the match after winning the toss.
    toss_decision_wins = toss_winner_wins.groupby('toss_decision').size().reset_index(name='wins')
    
    # Calculate total matches for each toss decision
    total_matches_by_toss_decision = df_match['toss_decision'].value_counts().reset_index()
    total_matches_by_toss_decision.columns = ['toss_decision', 'total_matches']
    
    # Merge wins and total matches
    toss_decision_stats = pd.merge(toss_decision_wins, total_matches_by_toss_decision, on='toss_decision')
    
    # Calculate win percentage
    toss_decision_stats['percentage'] = (toss_decision_stats['wins'] / toss_decision_stats['total_matches']) * 100
    toss_decision_stats['percentage'] = toss_decision_stats['percentage'].round(2)
    
    return toss_decision_stats.to_dict(orient='records')