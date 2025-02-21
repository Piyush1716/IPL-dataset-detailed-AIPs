from flask import Flask, jsonify, request
import api

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to IPL Analytics API"})

# Get list of all teams
@app.route('/teams', methods=['GET'])
def get_teams():
    return jsonify(api.teams())

# Get total matches played in each season
@app.route('/matches/total_per_season', methods=['GET'])
def get_total_matches_per_season():
    return jsonify(api.total_matches_over_seasons())

# Get total matches hosted by each city
@app.route('/matches/hosted_by_city', methods=['GET'])
def get_matches_hosted_by_city():
    return jsonify(api.matches_hosted_by_each_city())

# Get average target runs per season
@app.route('/matches/average_target_per_season', methods=['GET'])
def get_avg_target_by_season():
    return jsonify(api.avg_target_by_season())

# Get player performance statistics
@app.route('/player/performance', methods=['GET'])
def get_player_performance():
    player_name = request.args.get('player_name')
    if not player_name:
        return jsonify({"error": "Player name is required"}), 400
    return jsonify(api.player_performance(player_name))

# Get player performance against a specific team
@app.route('/player/performance_vs_team', methods=['GET'])
def get_player_vs_team():
    player_name = request.args.get('player_name')
    team_name = request.args.get('team_name')
    if not player_name or not team_name:
        return jsonify({"error": "Player name and team name are required"}), 400
    return jsonify(api.player_vs_team(player_name, team_name))

# Get first innings match details including phase-wise analysis
@app.route('/match/innings/first', methods=['GET'])
def get_match_innings_1():
    match_id = request.args.get('match_id', type=int)
    if match_id is None:
        return jsonify({"error": "Match ID is required"}), 400
    return jsonify(api.match_innings_1(match_id))

# Get second innings match details including top performers
@app.route('/match/innings/second', methods=['GET'])
def get_match_innings_2():
    match_id = request.args.get('match_id', type=int)
    if match_id is None:
        return jsonify({"error": "Match ID is required"}), 400
    return jsonify(api.match_innings_2(match_id))

@app.route('/match/innings/third', methods=['GET'])
def get_match_innings_3():
    match_id = request.args.get('match_id', type=int)
    if match_id is None:
        return jsonify({"error": "Match ID is required"}), 400
    return jsonify(api.match_innings_3(match_id))

@app.route('/match/innings/forth', methods=['GET'])
def get_match_innings_4():
    match_id = request.args.get('match_id', type=int)
    if match_id is None:
        return jsonify({"error": "Match ID is required"}), 400
    return jsonify(api.match_innings_4(match_id))

@app.route('/match/innings/fifth', methods=['GET'])
def get_match_innings_5():
    match_id = request.args.get('match_id', type=int)
    if match_id is None:
        return jsonify({"error": "Match ID is required"}), 400
    return jsonify(api.match_innings_5(match_id))

@app.route('/all partnerships')
def x():
    return jsonify(api.get_all_partnerships())

    

if __name__ == '__main__':
    app.run(debug=True)
