import json
from flask import Flask, render_template, abort, request, redirect, url_for

app = Flask(__name__)

def load_player_data():
    """Loads player data from the JSON file."""
    with open('player_data.json') as f:
        data = json.load(f)
    return data['players']

def save_player_data(players):
    """Saves the full list of players back to the JSON file."""
    with open('player_data.json', 'w') as f:
        json.dump({"players": players}, f, indent=4)

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

@app.route('/add-manual', methods=['GET', 'POST'])
def add_player_manually():
    """Renders a form to add a new player manually and handles submission."""
    if request.method == 'POST':
        name = request.form['name']
        try:
            goals = int(request.form['goals'])
            assists = int(request.form['assists'])
            appearances = int(request.form['appearances'])
        except ValueError:
            return "Invalid input: Goals, assists, and appearances must be numbers.", 400
        
        new_player = {
            "name": name,
            "goals": goals,
            "assists": assists,
            "appearances": appearances,
            "image": "default.png"  # A default image
        }
        
        players = load_player_data()
        players.append(new_player)
        save_player_data(players)
        
        return redirect(url_for('index'))
        
    return render_template('add_player_manual.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)