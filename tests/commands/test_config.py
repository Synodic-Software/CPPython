import unittest

from conan_for_poetry.commands.config import ConanConfig

class TestConfigCommand(unittest.TestCase):

    def test_Config(self):
        self.assertRaises(NotImplementedError, ConanConfig)


if __name__ == '__main__':
    unittest.main()