from cppython.schema import Generator, Metadata

cmakelists_template = (
    f'{sdate} - {time}\n'
    f'Tags: {tags}\n'
    f'Text: {text}'
)

class CMakeGenerator(Generator):
    """
    TODO: Description
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def metadata(self, data: dict) -> Metadata:
        raise NotImplementedError()