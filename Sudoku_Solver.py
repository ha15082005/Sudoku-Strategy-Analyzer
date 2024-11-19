import numpy as np
from Sudoku_Grid import Sudoku_Grid

# Implements Sudoku solving logic and tracks the strategies used during the process
class Sudoku_Solver:

    def __init__(self, Sudoku_Grid):
        self.grid = Sudoku_Grid.grid
        self.naked_singles = []  # To track Naked Single moves
        self.hidden_singles = []  # To track Hidden Single moves
        self.naked_pairs = [] # To track Naked Pair moves
        self.pointing_pairs = [] # To track Pointing Pair moves
        self.box_line_reductions = [] # To track Box-Line Reductions
        self.x_wings = [] # To track X-Wing moves
        self.swordfish = [] # To track Swordfish moves

    # Check if a number can be placed in a specific cell
    def is_valid(self, row, col, num):
        for i in range(9):
            # Check if the number is already in the row or column
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False
            # Check if the number is already in the 3x3 subgrid
            if self.grid[row - row % 3 + i // 3][col - col % 3 + i % 3] == num:
                return False
        return True # If no conflicts, the number is valid for the cell

    # Find and solve cells with only one possible number (Naked Single)
    def find_naked_single(self):
        found = False
        for row in range(9):
            for col in range(9):
                # Check empty cells
                if self.grid[row][col] == 0:
                    possible_nums = [num for num in range(1, 10) if self.is_valid(row, col, num)]
                    # If only one number is possible, place it in the cell
                    if len(possible_nums) == 1:
                        self.grid[row][col] = possible_nums[0]
                        self.naked_singles.append((row, col, possible_nums[0]))
                        found = True
        return found

    # Find and solve cells where a number can only appear in one position within a row, column, or subgrid
    def find_hidden_single(self):
        found = False
        for num in range(1, 10):
            for row in range(9):
                # Check row for Hidden Single
                possible_positions = [col for col in range(9) if
                                      self.grid[row][col] == 0 and self.is_valid(row, col, num)]
                if len(possible_positions) == 1:
                    col = possible_positions[0]
                    self.grid[row][col] = num
                    self.hidden_singles.append((row, col, num))
                    found = True

            for col in range(9):
                # Check column for Hidden Single
                possible_positions = [row for row in range(9) if
                                      self.grid[row][col] == 0 and self.is_valid(row, col, num)]
                if len(possible_positions) == 1:
                    row = possible_positions[0]
                    self.grid[row][col] = num
                    self.hidden_singles.append((row, col, num))
                    found = True
        return found

    # Find and eliminate Naked Pairs
    def find_naked_pairs(self):
        found = False
        for row in range(9):
            candidates = {}
            for col in range(9):
                # Check empty cells
                if self.grid[row][col] == 0:
                    possible_nums = [num for num in range(1, 10) if self.is_valid(row, col, num)]
                    # Store cells with exactly two possible numbers
                    if len(possible_nums) == 2:
                        candidates[(row, col)] = possible_nums

            seen = {}
            for cell, pair in candidates.items():
                pair_tuple = tuple(pair)
                # If a pair is found, eliminate it from other cells in the row
                if pair_tuple in seen:
                    other_cell = seen[pair_tuple]
                    for col in range(9):
                        if col not in {cell[1], other_cell[1]}:
                            for num in pair:
                                found = True
                    self.naked_pairs.append((cell, other_cell, pair))
                else:
                    seen[pair_tuple] = cell
        return found

    # Find and solve Pointing Pairs within subgrids
    def find_pointing_pairs(self):
        found = False
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                for num in range(1, 10):
                    # Get positions of the number in the subgrid
                    positions = [
                        (row, col)
                        for row in range(box_row, box_row + 3)
                        for col in range(box_col, box_col + 3)
                        if self.grid[row][col] == 0 and self.is_valid(row, col, num)
                    ]
                    # Check if the positions are confined to one row or one column
                    if len(positions) > 1:
                        rows = {pos[0] for pos in positions}
                        cols = {pos[1] for pos in positions}
                        if len(rows) == 1 or len(cols) == 1:
                            self.pointing_pairs.append((positions, num))
                            found = True
        return found

    # Find and solve Box-Line Reductions
    def find_box_line_reduction(self):
        found = False
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                for num in range(1, 10):
                    # Get positions of the number in the subgrid
                    positions = [
                        (row, col)
                        for row in range(box_row, box_row + 3)
                        for col in range(box_col, box_col + 3)
                        if self.grid[row][col] == 0 and self.is_valid(row, col, num)
                    ]
                    rows = {pos[0] for pos in positions}
                    cols = {pos[1] for pos in positions}
                    # Eliminate the number from other cells in the row
                    if len(rows) == 1:
                        row = list(rows)[0]
                        for col in range(9):
                            if col not in {pos[1] for pos in positions}:
                                found = True
                        self.box_line_reductions.append((positions, num, "row"))
                    # Eliminate the number from other cells in the column
                    elif len(cols) == 1:
                        col = list(cols)[0]
                        for row in range(9):
                            if row not in {pos[0] for pos in positions}:
                                found = True
                        self.box_line_reductions.append((positions, num, "column"))
        return found

    # Find and solve X-Wing patterns
    def find_x_wing(self):
        found = False
        for num in range(1, 10):
            rows = [[] for _ in range(9)]
            cols = [[] for _ in range(9)]
            for row in range(9):
                for col in range(9):
                    if self.grid[row][col] == 0 and self.is_valid(row, col, num):
                        rows[row].append(col)
                        cols[col].append(row)

            for r1 in range(8):
                for r2 in range(r1 + 1, 9):
                    # Check for X-Wing in rows
                    if len(rows[r1]) == 2 and len(rows[r2]) == 2 and set(rows[r1]) == set(rows[r2]):
                        c1, c2 = rows[r1]
                        for row in range(9):
                            if row != r1 and row != r2:
                                found = True
                        self.x_wings.append(((r1, r2), (c1, c2), num))
        return found

    # Apply all strategies iteratively until no further progress can be made
    def solve(self):
        while True:
            progress = False
            progress |= self.find_naked_single()
            progress |= self.find_hidden_single()
            progress |= self.find_naked_pairs()
            progress |= self.find_pointing_pairs()
            progress |= self.find_box_line_reduction()
            progress |= self.find_x_wing()
            if not progress:
                break