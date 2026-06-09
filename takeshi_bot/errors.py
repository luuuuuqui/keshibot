class TakeshiError(Exception):
    """Base class for user-facing Takeshi errors."""


class InvalidParameterError(TakeshiError):
    """Raised when a command receives invalid parameters."""


class WarningError(TakeshiError):
    """Raised for non-critical command warnings."""


class DangerError(TakeshiError):
    """Raised for serious command failures."""
