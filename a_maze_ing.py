from config import config_parser, ConfigError
from maze_generator import MazeUI, MazeGenerator, WALL_COLORS
import sys
import os
import random


if __name__ == "__main__":
    try:
        config = config_parser()
    except ConfigError as e:
        print("Config Error:", e)
        sys.exit(1)
    generator = MazeGenerator(
        config["WIDTH"],
        config["HEIGHT"],
        config["ENTRY"],
        config["EXIT"],
        config["SEED"],
        config["PERFECT"],
    )

    ui = MazeUI(generator)
    ui.maze.generate()
    ui.maze.print_maze(ui.wall_color, ui.show_path)
    while True:
        print("\n=====  A-MAZE-ING  =====")
        print(" 1) Regenerate a New Maze")
        print(" 2) Hide / Show Solution")
        print(" 3) Change maze wall colours")
        print(" 4) exit")

        choice = int(input("> ").strip())
        
        os.system("clear")

        if choice == 1:
            ui.maze.generate()
            ui._restart()
            ui.maze.print_maze(ui.wall_color, ui.show_path)
        elif choice == 2:
            ui.show_path = not ui.show_path
            ui.maze.solve()
            ui.maze.print_maze(ui.wall_color, ui.show_path)
        elif choice == 3:
            available = [
                c for c in WALL_COLORS.values()
                if c != ui.wall_color
            ]
            ui.wall_color = random.choice(available)
            ui.maze.print_maze(ui.wall_color, ui.show_path)
        elif choice == 4:
            break
        else:
            print("\n  ERROR CHOICE \n")
    generator.export(config["OUTPUT_FILE"])


