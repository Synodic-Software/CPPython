from cppython.schema import PEP621, Generator, Metadata


class CMakeGenerator(Generator):
    """
    A CPPython generator implementing a CMake backend
    """

    def __init__(self, pep_612: PEP621, cppython_data: Metadata, generator_data: dict) -> None:
        super().__init__(pep_612, cppython_data, generator_data)

    # Plugin Contract

    @staticmethod
    def name() -> str:
        """
        The name of the generator
        """
        return "cmake"

    # Generator Contract

    def populate_metadata(self, data: dict):
        """
        data - The CPPoetry data taken from pyproject.toml
        """
        pass

    def populate_plugin(self, data: dict):
        """
        data - The data taken from pyproject.toml that belongs to this generator
        """
        pass

    # API Contract

    def install(self) -> None:
        raise NotImplementedError()

    def update(self) -> None:
        raise NotImplementedError()

    def build(self) -> None:
        raise NotImplementedError()
