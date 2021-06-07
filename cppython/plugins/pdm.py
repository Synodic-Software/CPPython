
# CPPython
from cppython.core import Project
from cppython.api import CPPythonAPI


class PDMPlugin():
    def __init__(self):
        pass

    def valid(self) -> bool:
        return False

    def gather_pep_612(self, data: dict) -> dict:
        return {}
