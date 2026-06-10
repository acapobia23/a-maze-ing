from config.exceptions import ConfigError, ConfigParseError, ConfigValueError
import sys
from typing import TypedDict, cast


ConfigValue = int | str | bool | tuple[int, int]


class Config(TypedDict):
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int


KEYS = (
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
    "SEED",
)


def parse_int(v: str) -> int:
    return int(v)


def parse_str(v: str) -> str:
    return v.strip()


def parse_bool(v: str) -> bool:
    v = v.lower()
    if v == "true":
        return True
    if v == "false":
        return False
    raise ConfigValueError(f"Invalid syntax boolean value: '{v}'")


def parse_tuple(v: str) -> tuple[int, int]:
    x, y = v.split(",")
    return int(x), int(y)


PARSERS = {
    "WIDTH": parse_int,
    "HEIGHT": parse_int,
    "ENTRY": parse_tuple,
    "EXIT": parse_tuple,
    "OUTPUT_FILE": parse_str,
    "PERFECT": parse_bool,
    "SEED": parse_int,
}


def check_dimension(cnf: Config) -> None:
    if cnf["WIDTH"] < 1 or cnf["WIDTH"] > 45:
        raise ConfigValueError("Invalid width: width > 9 & < 45")
    if cnf["HEIGHT"] < 1 or cnf["HEIGHT"] > 45:
        raise ConfigValueError("Invalid height: height > 7 & < 45")


def check_entry_exit(cnf: Config) -> None:
    x1, y1 = cnf["ENTRY"]
    x2, y2 = cnf["EXIT"]
    w = cnf["WIDTH"]
    h = cnf["HEIGHT"]

    if not (0 <= x1 < w and 0 <= y1 < h):
        raise ConfigValueError("Invalid Entry cords")
    if not (0 <= x2 < w and 0 <= y2 < h):
        raise ConfigValueError("Invalid Exit cords")
    if cnf["ENTRY"] == cnf["EXIT"]:
        raise ConfigValueError("Invalid Entry Exit: same cords")


def check_output_file(cnf: Config) -> None:
    file = cnf["OUTPUT_FILE"]
    if file.count("/") != 0:
        raise ConfigValueError(f"Output file is a directory: {file}")


def check_seed(cnf: Config) -> None:
    if cnf["SEED"] < 0:
        raise ConfigValueError("Invalid Seed")


VALIDATOR = (
    check_dimension,
    check_entry_exit,
    check_output_file,
    check_seed,
)


def raw_config() -> list[tuple[str, str]]:
    raw: list[tuple[str, str]] = []

    if len(sys.argv) != 2:
        raise ConfigError("Error Arg Count: python3 a_maze_ing.py config.txt")

    try:
        with open(sys.argv[1], "r") as f:
            file = f.readlines()
    except FileNotFoundError as e:
        raise ConfigParseError("Config file not found") from e

    for line in file:
        line = line.replace("\n", "")
        if not line or line.startswith("#"):
            continue
        if " " in line or "\t" in line:
            raise ConfigParseError(f"Invalid syntax space found: {line}")
        if line.count("=") != 1:
            raise ConfigParseError(f"Invalid line: {line}"
                                   "   Right Syntax 'KEY=VALUE'")
        key, value = line.split("=", 1)
        if key == "" or value == "":
            raise ConfigParseError(f"Invalid syntax config: {line}"
                                   "   Right Syntax 'KEY=VALUE'")
        raw.append((key, value))

    checked = set()
    for key, value in raw:
        if key in checked:
            raise ConfigParseError(f"Duplicate key: {key}")
        checked.add(key)
        if key not in KEYS:
            raise ConfigParseError(f"Unknow Key: {key}")
    return raw


def config_parser() -> Config:
    config: dict[str, ConfigValue] = {}
    raw = raw_config()

    for key, value in raw:
        try:
            parsed_value = PARSERS[key](value)
            config[key] = cast(ConfigValue, parsed_value)
        except (ValueError, TypeError) as e:
            raise ConfigValueError(f"Invalid value for {key}: {value}") from e

    missing = [key for key in KEYS if key not in config]
    if missing:
        raise ConfigParseError(f"Missing key: {', '.join(missing)}")

    typed_config = cast(Config, config)
    for funct in VALIDATOR:
        funct(typed_config)
    return typed_config
