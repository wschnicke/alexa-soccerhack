import unittest
from alexa.highlights import *
from alexa.teams import track_team

class TestAliases(unittest.TestCase):

    def test_get_tracking_matches_from_none_tracked(self):
        self.assertEqual(update_tracked_matches(), [])

    def test_get_tracking_matches_from_some_tracked(self):
        track_team(480)
        track_team(19)
        track_team(8)
        matches = update_tracked_matches()
        self.assertNotEqual(matches, [])
        # So this assertion isn't always good, because sometimes people are on break. So need to figure out better way to do this.

if __name__ == '__main__':
    unittest.main()
