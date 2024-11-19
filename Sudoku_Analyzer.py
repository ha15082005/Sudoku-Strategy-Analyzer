import pandas as pd
from Sudoku_Grid import Sudoku_Grid
from Sudoku_Solver import Sudoku_Solver

# Analyze a dataset of Sudoku puzzles and applied solvers to each puzzle
class Sudoku_Analyzer:

    # Initialize with a dataset of puzzles and solutions
    def __init__(self, dataset):
        self.dataset = dataset

    # Analyze a single Sudoku puzzle and create a table of solving strategies
    def analyze_puzzle(self, puzzle_string):
        grid = Sudoku_Grid(puzzle_string) # Create a Sudoku grid from the puzzle string
        solver = Sudoku_Solver(grid) # Initialize the solver with the grid and solve the puzzle
        solver.solve()

        # Combine moves from Naked Singles and Hidden Singles
        combined_moves = solver.naked_singles + solver.hidden_singles

        # Create a table showing the moves for each strategy and combined strategies
        table = pd.DataFrame({
            "Naked Singles": [str(move) for move in solver.naked_singles] + [""] * (len(combined_moves) - len(solver.naked_singles)),
            "Hidden Singles": [str(move) for move in solver.hidden_singles] + [""] * (len(combined_moves) - len(solver.hidden_singles)),
            "Combined Strategies": [str(move) for move in combined_moves],
        })
        return table

    # Analyze multiple puzzles from the dataset
    def analyze_dataset(self, num_samples=100):
        results = [] # Initialize a list to store analysis results
        for index, row in self.dataset.iterrows():
            # Stop if the number of samples exceeds the specified limit
            if index >= num_samples:
                break
            # Analyze the puzzle and record the results
            steps = self.analyze_puzzle(row["puzzle"], row["solution"])
            results.append({
                "puzzle": row["puzzle"], # The original puzzle string
                "solution": row["solution"], # The solution string
                "num_steps": len(steps), # Number of steps to solve the puzzle
                "strategies_used": [step[3] for step in steps] # List of strategies used
            })
        return pd.DataFrame(results) # Return a DataFrame containing the results