import unittest

from conan_for_poetry.commands.add import ConanAdd

class TestAddCommand(unittest.TestCase):

    def test_Add(self):
        self.assertRaises(NotImplementedError, ConanAdd)


if __name__ == '__main__':
    unittest.main()