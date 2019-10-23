import unittest

from conan_for_poetry.commands.check import ConanCheck

class TestCheckCommand(unittest.TestCase):

    def test_Check(self):
        self.assertRaises(NotImplementedError, ConanCheck)


if __name__ == '__main__':
    unittest.main()