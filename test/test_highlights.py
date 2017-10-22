import unittest
from alexa.highlights import *
from alexa.teams import *

class TestAliases(unittest.TestCase):

    def test_update_tracked_matches_from_none_tracked(self):
        self.assertEqual(update_tracked_matches([]), [])

    # TEMP
    def test_update_tracked_matches_from_some_tracked(self):
        global tracked_matches, finished_matches
        del tracked_matches[:] # empty list
        del finished_matches[:]
        matches = update_tracked_matches([480, 19, 8], [480, 19, 8])
        self.assertNotEqual(matches, [])
        # So this assertion isn't always good, because sometimes people are on break and none will be fetched. So need to figure out better way to do this.

    # TEMP
    def test_get_tracking_matches_and_match_updates(self):
        global tracked_teams, tracked_matches, finished_matches
        del tracked_matches[:]
        del tracked_updates[:]
        del finished_matches[:]
        matches = update_tracked_matches([480, 19, 8], [480, 19, 8])
        events = get_tracked_updates(matches)
        self.assertNotEqual(events, [])

    # TEMP
    def test_tracks_and_get_updates(self):
        global tracked_teams, tracked_matches, tracked_updates, finished_matches
        del tracked_teams[:]
        del tracked_matches[:]
        del tracked_updates[:]
        del finished_matches[:]
        track_team(18)
        track_team(19)
        track_team(7)
        updates = report_updates()
        self.assertNotEqual(len(updates), 0)
        updates2 = report_updates()
        self.assertEqual(len(updates2), 0)

    def test_get_updates_empty(self):
        global tracked_teams, tracked_matches, tracked_updates, finished_matches
        del tracked_teams[:]
        del tracked_matches[:]
        del tracked_updates[:]
        del finished_matches[:]
        updates = report_updates()
        self.assertEqual(len(updates), 0)

if __name__ == '__main__':
    unittest.main()
