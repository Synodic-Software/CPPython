import unittest

from conan_for_poetry.commands.env import ConanEnv

class TestEnvCommand(unittest.TestCase):

    def test_Env(self):
        self.assertRaises(NotImplementedError, ConanEnv)


if __name__ == '__main__':
    unittest.main()