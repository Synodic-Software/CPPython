
# CPPython
from cppython.core import PEP621, Plugin
from cerberus.validator import Validator

class CPPythonPlugin():
    def __init__(self):
        pass

class PDMPlugin(Plugin):
    def __init__(self):
        pass

    def valid(self, data: dict) -> bool:
        return False

    def gather_pep_612(self, validator: Validator, data: dict) -> dict:
        return PEP621()