"""
Custom exceptions used by CPPython
"""


class ConfigError(Exception):
    """
    Raised when there is a configuration error
    """

    def __init__(self, error: str) -> None:
        self._error = error

        super().__init__(error)

    @property
    def error(self) -> str:
        """
        Returns the underlying error

        Returns:
            str -- The underlying error
        """
        return self._error
