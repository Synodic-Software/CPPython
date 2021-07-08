class ConfigError(Exception):
    def __init__(self, error: Exception) -> None:
        self._error = error

        super().__init__(str(error))

    @property
    def error(self) -> Exception:
        return self._error