"""Project schema specifications
"""

from abc import abstractmethod


class API:
    """Project API specification"""

    @abstractmethod
    def install(self) -> None:
        """_summary_

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self) -> None:
        """_summary_

        Raises:
            NotImplementedError: _description_
        """

        raise NotImplementedError()
