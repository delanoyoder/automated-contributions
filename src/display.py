from json import load
from argparse import ArgumentParser


class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = [["□ " for _ in range(columns)] for _ in range(rows)]

    def set_colored(self, row, column, colored=True):
        self.grid[row][column] = "■ " if colored else "□ "

    def display(self):
        for row in self.grid:
            print("".join(row))

    def load_config(self, filename):
        if not filename.endswith(".json"):
            filename += ".json"
        with open(filename, "r") as infile:
            config = load(infile)
        return config


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--config", required=True, help="Name of configuration file")
    args = parser.parse_args()

    grid = Grid(7, 52)
    config = grid.load_config(args.config)

    # Set the colored boxes
    for row, column in config["contributions"]:
        grid.set_colored(row, column, colored=True)

    # Display the grid
    grid.display()
