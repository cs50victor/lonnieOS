import unittest
from shellConfig import getArg


class TestUtils(unittest.TestCase):

    def test_validArgs(self):
        """
            Test that it returns the correct argument values
        """
        line = "command --id=6"
        arg = "--id"
        self.assertEqual(getArg(line, arg,int), 6)

        line = "command --num=6.6"
        arg = "--num"
        self.assertEqual(getArg(line, arg, float), 6.6)
        line = "command --num=6"
        self.assertEqual(getArg(line, arg, float), 6.0)

        line = "command --num=hey"
        arg = "--num"
        self.assertEqual(getArg(line, arg, str), "hey")
        line = "command --num=HeY"
        self.assertEqual(getArg(line, arg, str), "hey")

        line = "command --num=0"
        arg = "--num"
        self.assertEqual(getArg(line, arg, int), 0)

    def test_invalidArgs(self):
        """
            Test that it return None if argument wasn't found
        """
        line = "command --id=6"
        arg = "num"
        self.assertEqual(getArg(line, arg, int), None)
        line = "command --id=6.0"
        self.assertEqual(getArg(line, arg, int), None)
        line = "command --id=6"
        arg = "="
        self.assertEqual(getArg(line, arg, int), None)
        line = "command --id=hey"
        arg = "-id"
        self.assertEqual(getArg(line, arg, str), None)
        arg = "id"
        self.assertEqual(getArg(line, arg, float), None)
    


if __name__ == "__main__":
    unittest.main()