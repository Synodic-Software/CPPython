
class ConanPlugin():

    def PoetryNew(self):
        from .commands.new import ConanNew
        ConanNew()

    def PoetryInit(self):
        from .commands.init import ConanInit
        ConanInit()


    def PoetryInstall(self):
        from .commands.install import ConanInstall
        ConanInstall()


    def PoetryUpdate(self):
        from .commands.update import ConanUpdate
        ConanUpdate()


    def PoetryAdd(self):
        from .commands.add import ConanAdd
        ConanAdd()


    def PoetryRemove(self):
        from .commands.remove import ConanRemove
        ConanRemove()


    def PoetryShow(self):
        from .commands.show import ConanShow
        ConanShow()


    def PoetryBuild(self):
        from .commands.build import ConanBuild
        ConanBuild()


    def PoetryPublish(self):
        from .commands.publish import ConanPublish
        ConanPublish()


    def PoetryConfig(self):
        from .commands.config import ConanConfig
        ConanConfig()


    def PoetryCheck(self):
        from .commands.check import ConanCheck
        ConanCheck()


    def PoetrySearch(self):
        from .commands.search import ConanSearch
        ConanSearch()


    def PoetryLock(self):
        from .commands.lock import ConanLock
        ConanLock()


    def PoetryVersion(self):
        from .commands.version import ConanVersion
        ConanVersion()


    def PoetryExport(self):
        from .commands.export import ConanExport
        ConanExport()


    def PoetryEnv(self):
        from .commands.env import ConanEnv
        ConanEnv()