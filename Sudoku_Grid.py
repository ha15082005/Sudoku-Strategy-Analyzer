import numpy as np

# A class to represent a Sudoku grid
class Sudoku_Grid:

    # Initialize the grid from a puzzle string
    def __init__(self, puzzle_string):
        self.grid = self.string_to_grid(puzzle_string)

    # Convert a Sudoku string to a 9x9 numpy grid
    @staticmethod
    def string_to_grid(sudoku_string):
        return np.array([int(char) for char in sudoku_string]).reshape(9, 9)

    # Check if a number can be placed in a specific cell without violating Sudoku rules
    def is_valid(self, row, col, num):
        # Loop through all cells in the row and column to check for conflicts
        for i in range(9):
            # Check if the number already exists in the row or column
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False
            # Check if the number already exists in the 3x3 subgrid
            if self.grid[row - row % 3 + i // 3][col - col % 3 + i % 3] == num:
                return False
        return True # If no conflicts, the number can be placed