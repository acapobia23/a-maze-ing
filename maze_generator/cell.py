class Cell:
    def __init__(self, x: int, y: int):
        # position
        self.x = x
        self.y = y

        self.walls: list[int] = [1, 1, 1, 1]

        # DFS state
        self.visited = False
        self.is_42 = False