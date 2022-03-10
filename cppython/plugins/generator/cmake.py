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
        self.data = cmake_data

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

    def generator_downloaded(self) -> bool:

        # CMake tooling is a part of the python package tooling
        return True

    def download_generator(self) -> None:
        """
        Installs the external tooling required by the generator if necessary
        """

    def update_generator(self) -> None:
        """
        Update the tooling required by the generator
        """

    def install(self) -> None:
        raise NotImplementedError()

    def update(self) -> None:
        raise NotImplementedError()

    def build(self) -> None:
        raise NotImplementedError()
