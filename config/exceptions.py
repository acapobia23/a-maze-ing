class MazeError(Exception):
    """
    Base exception for the project.
    """
    pass


class ConfigError(MazeError):
    """
    Generic configuration error.
    """
    pass


class ConfigParseError(ConfigError):
    """
    Raised when the config file has syntax/format issues.
    Example: missing '=', malformed line, etc.
    """
    pass


class ConfigValueError(ConfigError):
    """
    Raised when a config value is invalid.
    Example: WIDTH=-1, invalid bool, bad tuple format.
    """
    pass
