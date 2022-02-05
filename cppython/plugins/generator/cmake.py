"""
TODO:
"""
from pathlib import Path
from typing import Type

from cppython.schema import PEP621, Generator, GeneratorData, Metadata


class CMakeData(GeneratorData):
    """
    TODO:
    """

    pass


class CMakeGenerator(Generator):
    """
    A CPPython generator implementing a CMake backend
    """

    def __init__(self, pep_612: PEP621, cppython_data: Metadata, generator_data: CMakeData) -> None:
        super().__init__(pep_612, cppython_data, generator_data)

    # Plugin Contract

    @staticmethod
    def name() -> str:
        """
        The name of the generator
        """
        return "cmake"

    # Generator Contract

    def install_generator(self) -> bool:
        """
        Installs the external tooling required by the generator if necessary
        Returns whether anything was installed or not
        """
        return False

    @staticmethod
    def data_type() -> Type[GeneratorData]:
        """
        Returns the pydantic type to cast the generator configuration data to
        """
        return CMakeData

    # API Contract

    def install(self) -> None:
        raise NotImplementedError()

    def update(self) -> None:
        raise NotImplementedError()

    def build(self) -> None:
        raise NotImplementedError()
