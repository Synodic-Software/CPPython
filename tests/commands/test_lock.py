import unittest

from conan_for_poetry.commands.lock import ConanLock

class TestLockCommand(unittest.TestCase):

    def test_Lock(self):
        self.assertRaises(NotImplementedError, ConanLock)


if __name__ == '__main__':
    unittest.main()