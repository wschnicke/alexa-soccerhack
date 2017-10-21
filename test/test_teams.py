import unittest
from alexa.teams import *

class TestTeams(unittest.TestCase):

    def test_get_team_id_exists(self):
        self.assertEqual(get_team_id("Newcastle United"), 19)

    def test_get_team_id_exists_mixed_casing(self):
        self.assertEqual(get_team_id("neWCastle UNitEd"), 19)

    def test_get_team_id_doesnt_exist(self):
        self.assertEqual(get_team_id("Nonexistant Team") ,None)

    def test_get_team_exists(self):
        self.assertEqual(get_team("Newcastle United"), [19, "Newcastle United"])

    def test_get_team_exists_mixed_casing(self):
        self.assertEqual(get_team("neWCastle UNitEd"), [19, "Newcastle United"])

    def test_get_team_doesnt_exist(self):
        self.assertEqual(get_team("Nonexistant Team") ,None)

    def test_get_team_name_exists(self):
        self.assertEqual(get_team_name(8), "Stoke City")

    def test_get_team_name_doesnt_exist(self):
        self.assertEqual(get_team_name(11111) ,None)

if __name__ == '__main__':
    unittest.main()
