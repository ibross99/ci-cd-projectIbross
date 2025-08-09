import unittest
import os
import json
from app import app, load_player_data, save_player_data

class PlayerStatsAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Backup original data
        with open('player_data.json') as f:
            self.original_data = json.load(f)
        self.players = self.original_data['players']

    def tearDown(self):
        # Restore original data
        with open('player_data.json', 'w') as f:
            json.dump(self.original_data, f, indent=4)

    def test_index_page(self):
        """Test that the index page loads correctly and lists players."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Liverpool Player Stats</h1>', response.data)
        for player in self.players:
            self.assertIn(player['name'].encode(), response.data)

    def test_player_stats_page(self):
        """Test that a player's stats page loads correctly."""
        player = self.players[0]
        player_name_slug = player['name'].replace(' ', '-')
        response = self.app.get(f'/player/{player_name_slug}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(player['name'].encode(), response.data)
        self.assertIn(f"Goals: {player['goals']}".encode(), response.data)
        self.assertIn(f"Assists: {player['assists']}".encode(), response.data)

    def test_player_not_found(self):
        """Test that a 404 error is returned for a player that does not exist."""
        response = self.app.get('/player/Non-Existent-Player')
        self.assertEqual(response.status_code, 404)

    def test_add_player_page_loads(self):
        """Test that the 'add-manual' page loads correctly."""
        response = self.app.get('/add-manual')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Add a New Player</h1>', response.data)

    def test_add_player_successfully(self):
        """Test that a new player can be added successfully."""
        new_player_data = {
            'name': 'Test Player',
            'goals': '10',
            'assists': '5',
            'appearances': '20'
        }
        response = self.app.post('/add-manual', data=new_player_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Check that the new player is now in the data
        updated_players = load_player_data()
        player_names = [p['name'] for p in updated_players]
        self.assertIn('Test Player', player_names)

        # Check that the new player's stats are correct
        added_player = next((p for p in updated_players if p['name'] == 'Test Player'), None)
        self.assertIsNotNone(added_player)
        self.assertEqual(added_player['goals'], 10)
        self.assertEqual(added_player['assists'], 5)
        self.assertEqual(added_player['appearances'], 20)

    def test_add_player_invalid_input(self):
        """Test that adding a player with invalid (non-integer) stats fails."""
        invalid_player_data = {
            'name': 'Invalid Player',
            'goals': 'ten',
            'assists': 'five',
            'appearances': 'twenty'
        }
        response = self.app.post('/add-manual', data=invalid_player_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid input', response.data)

if __name__ == '__main__':
    unittest.main()

    