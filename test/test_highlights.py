import unittest
from alexa.highlights import *
from alexa.teams import *

class TestAliases(unittest.TestCase):

    def test_update_tracked_matches_from_none_tracked(self):
        self.assertEqual(update_tracked_matches([]), [])

    def test_update_tracked_matches_from_some_tracked(self):
        global tracked_matches
        del tracked_matches[:] # empty list
        matches = update_tracked_matches([480, 19, 8], [480, 19, 8])
        self.assertNotEqual(matches, [])
        # So this assertion isn't always good, because sometimes people are on break. So need to figure out better way to do this.

    def test_get_tracking_matches_and_match_updates(self):
        global tracked_teams, tracked_matches
        del tracked_matches[:]
        matches = update_tracked_matches([480, 19, 8], [480, 19, 8])
        events = get_tracked_updates(matches)
        self.assertNotEqual(events, [])

    def test_track_and_get_updates(self):
        global tracked_teams
        del tracked_teams[:]
        del tracked_matches[:]
        track_team(480)
        track_team(19)
        updates = report_updates()
        self.assertNotEqual(len(updates), 0)

if __name__ == '__main__':
    unittest.main()
