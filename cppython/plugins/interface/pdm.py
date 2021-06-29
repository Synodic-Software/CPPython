
# CPPython
from os import stat
from cppython.schema import PEP621, Plugin

class CPPythonPlugin():
    def __init__(self):
        pass

class PDMPlugin(Plugin):
    def __init__(self):
        pass

    @staticmethod
    def valid(data: dict) -> bool:
        return False

    def gather_pep_612(self, data: dict) -> PEP621:
        return PEP621()