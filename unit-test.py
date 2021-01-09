import unittest
import game
class TestFuncs(unittest.TestCase):

    def test_add_enemy(self):
        pos = [100, -5]
        self.assertEqual(game.AddEnemy(0, pos, 5), 6)

if __name__ == '__main__':
    unittest.main()