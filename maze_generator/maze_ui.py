from typing import ClassVar
from .maze_generator import MazeGenerator

WALL_COLORS: ClassVar[dict[str, str]] = {
    "default": "\033[0m",
    "blue": "\033[94m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
}

class MazeUI:

    def __init__(self, maze: MazeGenerator) -> None:
        self.maze: MazeGenerator = maze

        self.show_path: bool = False
        self.wall_color: str = WALL_COLORS["default"]

    def _restart(self) -> None:
        self.show_path: bool = False
        self.wall_color: str = WALL_COLORS["default"]