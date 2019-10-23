import unittest

from conan_for_poetry.plugin import ConanPlugin

class TestRequirements(unittest.TestCase):

    def test_poetry(self):
        pass

    def test_repository(self):
        pass


class TestPlugin(unittest.TestCase):

    def test_PoetryNew(self):
        plugin = ConanPlugin()
        self.assertRaises(NotImplementedError, plugin.PoetryNew)


    def test_PoetryInit(self):
        plugin = ConanPlugin()
        self.assertRaises(NotImplementedError, plugin.PoetryInit)


    def test_PoetryInstall(self):
        plugin = ConanPlugin()
        self.assertRaises(NotImplementedError, plugin.PoetryInstall)


    def test_PoetryUpdate(self):
        plugin = ConanPlugin()
        self.assertRaises(NotImplementedError, plugin.PoetryUpdate)


    def test_PoetryAdd(self):
        plugin = ConanPlugin()
        self.assertRaises(NotImplementedError,  plugin.PoetryAdd)


    def test_PoetryRemove(self):
        plugin = ConanPlugin()
        self.assertRaises(NotImplementedError, plugin.PoetryRemove)


    def test_PoetryShow(self):
        plugin = ConanPlugin()
        self.assertRaises(NotImplementedError, plugin.PoetryShow)


    def test_PoetryBuild(self):
        plugin = ConanPlugin()
        self.assertRaises(NotImplementedError, plugin.PoetryBuild)


    def test_PoetryPublish(self):
        plugin = ConanPlugin()
        self.assertRaises(NotImplementedError, plugin.PoetryPublish)


    def test_PoetryConfig(self):
        plugin = ConanPlugin()
        self.assertRaises(NotImplementedError, plugin.PoetryConfig)


    def test_PoetryCheck(self):
        plugin = ConanPlugin()
        self.assertRaises(NotImplementedError, plugin.PoetryCheck)


    def test_PoetrySearch(self):
        plugin = ConanPlugin()
        self.assertRaises(NotImplementedError, plugin.PoetrySearch)


    def test_PoetryLock(self):
        plugin = ConanPlugin()
        self.assertRaises(NotImplementedError, plugin.PoetryLock)


    def test_PoetryVersion(self):
        plugin = ConanPlugin()
        self.assertRaises(NotImplementedError, plugin.PoetryVersion)


    def test_PoetryExport(self):
        plugin = ConanPlugin()
        self.assertRaises(NotImplementedError, plugin.PoetryExport)


    def test_PoetryEnv(self):
        plugin = ConanPlugin()
        self.assertRaises(NotImplementedError, plugin.PoetryEnv)


if __name__ == '__main__':
    unittest.main()