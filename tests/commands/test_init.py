import unittest

from conan_for_poetry.commands.init import ConanInit

class TestInitCommand(unittest.TestCase):

    def test_Init(self):
        self.assertRaises(NotImplementedError, ConanInit)


if __name__ == '__main__':
    unittest.main()