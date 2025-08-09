import json
from flask import Flask, render_template, abort

app = Flask(__name__)

def load_player_data():
    """Loads player data from the JSON file."""
    with open('player_data.json') as f:
        data = json.load(f)
    return data['players']

@app.route('/')
def index():
    """Renders the main page with a list of players."""
    players = load_player_data()
    return render_template('players.html', players=players)

@app.route('/player/<player_name>')
def player_stats(player_name):
    """Renders the stats for a specific player."""
    players = load_player_data()
    player = next((p for p in players if p['name'].replace(' ', '-') == player_name), None)
    if player is None:
        abort(404)
    return render_template('player_stats.html', player=player)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)