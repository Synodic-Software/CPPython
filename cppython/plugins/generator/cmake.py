"""
The default generator implementation for CPPython
"""
from typing import Type

from cppython.schema import Generator, GeneratorData, PyProject


class CMakeData(GeneratorData):
    """
    The data schema required for the CMake tooling
    """


class CMakeGenerator(Generator):
    """
    A CPPython generator implementing a CMake backend
    """

    def __init__(self, pyproject: PyProject, cmake_data: CMakeData) -> None:
        super().__init__(pyproject, cmake_data)

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
