import unittest
import scripts/cleanup_utilities

regex = __import__("../scripts/cleanup_utilities.py")

class TestReplace(unittest.TestCase):

    def test_replace(self):
            pass

if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
