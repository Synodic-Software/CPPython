import unittest

from conan_for_poetry.commands.update import ConanUpdate

class TestUpdateCommand(unittest.TestCase):

    def test_Update(self):
        self.assertRaises(NotImplementedError, ConanUpdate)


if __name__ == '__main__':
    unittest.main()