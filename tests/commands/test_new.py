import unittest

from conan_for_poetry.commands.new import ConanNew

class TestNewCommand(unittest.TestCase):

    def test_New(self):
        self.assertRaises(NotImplementedError, ConanNew)


if __name__ == '__main__':
    unittest.main()