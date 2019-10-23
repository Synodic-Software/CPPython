import unittest

from conan_for_poetry.commands.search import ConanSearch

class TestSearchCommand(unittest.TestCase):

    def test_Search(self):
        self.assertRaises(NotImplementedError, ConanSearch)


if __name__ == '__main__':
    unittest.main()