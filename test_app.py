import unittest
from app import app, load_player_data

class PlayerStatsAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.players = load_player_data()

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

if __name__ == '__main__':
    unittest.main()