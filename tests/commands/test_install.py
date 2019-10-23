import unittest

from conan_for_poetry.commands.install import ConanInstall

class TestInstallCommand(unittest.TestCase):

    def test_Install(self):
        self.assertRaises(NotImplementedError, ConanInstall)


if __name__ == '__main__':
    unittest.main()