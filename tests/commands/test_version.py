import unittest

from conan_for_poetry.commands.version import ConanVersion

class TestVersionCommand(unittest.TestCase):

    def test_Version(self):
        self.assertRaises(NotImplementedError, ConanVersion)


if __name__ == '__main__':
    unittest.main()