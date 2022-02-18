import unittest
from utils import getArg


class TestUtils(unittest.TestCase):

    def test_validArgs(self):
        """
            Test that it returns the correct argument values
        """
        line = "command --id=6"
        arg = "--id"
        self.assertEqual(getArg(line, arg), "6")
        line = "command --num=66"
        arg = "--num"
        self.assertEqual(getArg(line, arg), "66")

    def test_invalidArgs(self):
        """
            Test that it return None if argument wasn't found
        """
        line = "command --id=6"
        arg = "num"
        self.assertEqual(getArg(line, arg), None)
        arg = "="
        self.assertEqual(getArg(line, arg), None)
        arg = "-id"
        self.assertEqual(getArg(line, arg), None)
        arg = "id"
        self.assertEqual(getArg(line, arg), None)
    

if __name__ == "__main__":
    unittest.main()