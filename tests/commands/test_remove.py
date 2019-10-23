import unittest

from conan_for_poetry.commands.remove import ConanRemove

class TestRemoveCommand(unittest.TestCase):

    def test_Remove(self):
        self.assertRaises(NotImplementedError, ConanRemove)


if __name__ == '__main__':
    unittest.main()