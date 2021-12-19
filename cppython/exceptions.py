"""
Custom exceptions used by CPPython
"""


class ConfigError(Exception):
    """
    Raised when there is a configuration error
    """

    def __init__(self, error: Exception) -> None:
        self._error = error

        super().__init__(str(error))

    @property
    def error(self) -> Exception:
        """
        Accessor to the config error Exception base type

        Returns:
            Exception -- The base error type
        """
        return self._error
