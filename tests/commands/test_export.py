import unittest

from conan_for_poetry.commands.export import ConanExport

class TestExportCommand(unittest.TestCase):

    def test_Export(self):
        self.assertRaises(NotImplementedError, ConanExport)


if __name__ == '__main__':
    unittest.main()