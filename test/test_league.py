import unittest
from alexa.league import *

class TestLeagues(unittest.TestCase):
    def test_team_get_league_id_empty(self):
        self.assertEqual(get_league_id(" "), None)

    def test_get_league_id_exists(self):
        self.assertEqual(get_league_id("English Premier League"), 2)

    def test_get_league_id_exists2(self):
        self.assertEqual(get_league_id("EPL"), 2)

    def test_get_league_id_exists3(self):
        self.assertEqual(get_league_id("Major League Soccer"), 59)

    def test_get_league_id_exists4(self):
        self.assertEqual(get_league_id("MLS"), 59)

    def test_get_league_id_exists_mixed_casing(self):
        self.assertEqual(get_league_id("eNglish PremiER LeAGUE"), 2)

    def test_get_team_id_doesnt_exist(self):
        self.assertEqual(get_league_id("Nonexistant Team") ,None)
