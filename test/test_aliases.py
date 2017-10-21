import unittest
from alexa.aliases import *

class TestAliases(unittest.TestCase):

    def test_add_invalid_alias(self):
        self.assertEqual(add_alias("AliasName", "FalseTeamName"), 0)

if __name__ == '__main__':
    unittest.main()
