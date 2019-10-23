import unittest

from conan_for_poetry.commands.build import ConanBuild

class TestBuildCommand(unittest.TestCase):

    def test_Build(self):
        self.assertRaises(NotImplementedError, ConanBuild)



if __name__ == '__main__':
    unittest.main()