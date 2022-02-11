"""
TODO:
"""
from typing import Type

from cppython.schema import Generator, GeneratorData, PyProject


class CMakeData(GeneratorData):
    """
    TODO:
    """


class CMakeGenerator(Generator):
    """
    A CPPython generator implementing a CMake backend
    """

    def __init__(self, pyproject: PyProject) -> None:
        super().__init__(pyproject)

    @staticmethod
    def name() -> str:
        """
        The name of the generator
        """
        return "cmake"

    @staticmethod
    def data_type() -> Type[GeneratorData]:
        """
        Returns the pydantic type to cast the generator configuration data to
        """
        return CMakeData

    def install_generator(self) -> bool:
        """
        Installs the external tooling required by the generator if necessary
        Returns whether anything was installed or not
        """
        return False

    def install(self) -> None:
        raise NotImplementedError()

    def update(self) -> None:
        raise NotImplementedError()

    def build(self) -> None:
        raise NotImplementedError()
