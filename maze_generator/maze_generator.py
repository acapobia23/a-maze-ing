import random
from .cell import Cell

N, E, S, W = 0, 1, 2, 3

DIRS = {
    N: (0, -1),
    E: (1, 0),
    S: (0, 1),
    W: (-1, 0),
}


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool,
        seed: int | None,
    ):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect

        self.random = random.Random(seed)

        self.grid: list[list[Cell]] = []
        self.solution: list[tuple[int, int]] | None = None

    # ----------------------------
    # GRID
    # ----------------------------

    def _create_grid(self) -> None:
        self.grid = [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]

    # ----------------------------
    # NEIGHBORS
    # ----------------------------

    def _get_neighbors(self, cell: Cell) -> list[tuple[Cell, int]]:
        x, y = cell.x, cell.y
        neighbors: list[tuple[Cell, int]] = []

        for direction, (dx, dy) in DIRS.items():
            nx, ny = x + dx, y + dy

            if 0 <= nx < self.width and 0 <= ny < self.height:
                next_cell = self.grid[ny][nx]

                if not next_cell.visited and not getattr(next_cell,
                                                         "is_42", False):
                    neighbors.append((next_cell, direction))

        return neighbors

    # ----------------------------
    # WALL REMOVAL
    # ----------------------------

    def _remove_wall(self, current: Cell,
                     next_cell: Cell, direction: int) -> None:
        current.walls[direction] = 0

        opposite = {
            N: S,
            S: N,
            E: W,
            W: E,
        }

        next_cell.walls[opposite[direction]] = 0

    # ----------------------------
    # DFS GENERATION
    # ----------------------------

    def _dfs(self, cell: Cell) -> None:
        cell.visited = True

        neighbors = self._get_neighbors(cell)
        self.random.shuffle(neighbors)

        for next_cell, direction in neighbors:
            if not next_cell.visited:
                self._remove_wall(cell, next_cell, direction)
                self._dfs(next_cell)

    # ----------------------------
    # OPTIONAL CYCLES
    # ----------------------------

    def _add_cycles(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]

                if getattr(cell, "is_42", False):
                    continue

                for direction, (dx, dy) in DIRS.items():
                    nx, ny = x + dx, y + dy

                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        neighbor = self.grid[ny][nx]

                        if getattr(neighbor, "is_42", False):
                            continue

                        if self.random.random() < 0.05:
                            self._remove_wall(cell, neighbor, direction)

    # ----------------------------
    # 42 PATTERN
    # ----------------------------

    def _can_place_42(self) -> bool:
        return self.width >= 7 and self.height >= 5

    def _place_42_pattern(self) -> None:
        pattern = (
            (1, 0, 1, 0, 1, 1, 1),
            (1, 0, 1, 0, 0, 0, 1),
            (1, 1, 1, 0, 1, 1, 1),
            (0, 0, 1, 0, 1, 0, 0),
            (0, 0, 1, 0, 1, 1, 1),
        )

        offset_x = (self.width - len(pattern[0])) // 2
        offset_y = (self.height - len(pattern)) // 2

        for dy, row in enumerate(pattern):
            for dx, is_closed in enumerate(row):
                if not is_closed:
                    continue

                cell = self.grid[offset_y + dy][offset_x + dx]
                cell.walls = [1, 1, 1, 1]
                cell.visited = True
                cell.is_42 = True

    def generate(self) -> None:
        self._create_grid()

        if self._can_place_42():
            self._place_42_pattern()
        else:
            print("Error: maze too small for 42 pattern")

        start_x, start_y = self.entry
        start_cell = self.grid[start_y][start_x]

        self._dfs(start_cell)

        if not self.perfect:
            self._add_cycles()

    def solve(self) -> list[tuple[int, int]]:
        from collections import deque

        start_x, start_y = self.entry
        end_x, end_y = self.exit

        start = self.grid[start_y][start_x]
        goal = self.grid[end_y][end_x]

        queue = deque([start])
        parents: dict[Cell, Cell | None] = {start: None}
        visited: set[Cell] = {start}

        while queue:
            cell = queue.popleft()

            if cell.x == goal.x and cell.y == goal.y:
                break

            x, y = cell.x, cell.y

            for direction, (dx, dy) in DIRS.items():
                nx, ny = x + dx, y + dy

                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbor = self.grid[ny][nx]

                    # controllo muro: posso passare solo se NON c'è muro
                    if cell.walls[direction] == 0 and neighbor not in visited:
                        visited.add(neighbor)
                        parents[neighbor] = cell
                        queue.append(neighbor)

        # ricostruzione path
        path = []
        cur: Cell | None = goal

        while cur is not None:
            path.append((cur.x, cur.y))
            cur = parents.get(cur)

        path.reverse()

        self.solution = path
        return path

    # ----------------------------
    # DEBUG PRINT
    # ----------------------------
    def print_maze(self, wall_color: str, show_path: bool = False) -> None:
        RESET = "\033[0m"
        BLUE = "\033[94m"

        for y in range(len(self.grid)):
            top = ""
            mid = ""

            for x in range(len(self.grid[y])):
                cell = self.grid[y][x]

                # --- 42 pattern ALWAYS BLUE ---
                is_42 = getattr(cell, "is_42", False)
                cell_color_start = BLUE if is_42 else ""
                cell_color_end = RESET if is_42 else ""

                # --- path check ---
                in_path = (
                    show_path
                    and self.solution is not None
                    and (x, y) in self.solution
                )

                if in_path:
                    center = " . "
                else:
                    center = "###" if is_42 else "   "

                # --- walls (ONLY HERE we use wall_color) ---
                north = cell.walls[0] == 1
                west = cell.walls[3] == 1

                top += wall_color + "+" + ("---" if north else "   ") + RESET
                mid += wall_color + ("|" if west else " ") + RESET

                mid += cell_color_start + center + cell_color_end

            top += wall_color + "+" + RESET
            mid += wall_color + "|" + RESET

            print(top)
            print(mid)

        print(wall_color + "+---" * len(self.grid[0]) + "+" + RESET)

    def _cell_to_hex(self, cell: Cell) -> str:
        value = (
            (cell.walls[0] << 0) |
            (cell.walls[1] << 1) |
            (cell.walls[2] << 2) |
            (cell.walls[3] << 3)
        )
        return format(value, "X")

    def _path_to_dirs(self, path: list[tuple[int, int]]) -> str:
        res = ""

        for i in range(1, len(path)):
            x1, y1 = path[i - 1]
            x2, y2 = path[i]

            dx = x2 - x1
            dy = y2 - y1

            if dx == 1:
                res += "E"
            elif dx == -1:
                res += "W"
            elif dy == 1:
                res += "S"
            elif dy == -1:
                res += "N"

        return res

    def export(self, filename: str) -> None:
        lines = []

        # 1. maze rows
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                cell = self.grid[y][x]
                row += self._cell_to_hex(cell)
            lines.append(row)

        # empty line
        lines.append("")

        # 2. entry / exit
        ex, ey = self.entry
        sx, sy = self.exit

        lines.append(f"{ex},{ey}")
        lines.append(f"{sx},{sy}")

        # 3. path
        if self.solution is None:
            self.solve()

        path = self.solution if self.solution is not None else self.solve()

        path_dirs = self._path_to_dirs(path)
        lines.append(path_dirs)

        # write file
        with open(filename, "w") as f:
            f.write("\n".join(lines) + "\n")
