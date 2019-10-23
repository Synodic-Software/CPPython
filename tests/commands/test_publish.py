import unittest

from conan_for_poetry.commands.publish import ConanPublish

class TestPublishCommand(unittest.TestCase):

    def test_Publish(self):
        self.assertRaises(NotImplementedError, ConanPublish)


if __name__ == '__main__':
    unittest.main()