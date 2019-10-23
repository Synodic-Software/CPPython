import unittest

from conan_for_poetry.commands.show import ConanShow

class TestShowCommand(unittest.TestCase):

    def test_Show(self):
        self.assertRaises(NotImplementedError, ConanShow)


if __name__ == '__main__':
    unittest.main()