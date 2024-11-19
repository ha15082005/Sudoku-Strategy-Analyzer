import streamlit as st
import pandas as pd
import plotly.express as px
from Sudoku_Grid import Sudoku_Grid
from Sudoku_Solver import Sudoku_Solver
from Sudoku_Analyzer import Sudoku_Analyzer

# Application title and description
st.title("Sudoku Strategy Analyzer")
st.write("Analyze Sudoku puzzles, visualize solving strategies, and gain insights!")

# Sidebar
st.sidebar.title("Sudoku Options")
mode = st.sidebar.selectbox(
    "Choose an Option",
    ["Select Puzzle from Dataset", "Enter Puzzle Manually"]
)

# If the user chooses to select a puzzle from a dataset
if mode == "Select Puzzle from Dataset":
    # File uploader for CSV dataset
    uploaded_file = st.sidebar.file_uploader("Upload Sudoku Dataset CSV", type=["csv"])

    if uploaded_file:
        # Load dataset
        sudoku_data = pd.read_csv(uploaded_file)
        st.write("Dataset Loaded! Showing first 5 rows:")
        st.write(sudoku_data.head()) # Display the first 5 rows of the dataset

        # Number input to select a puzzle index
        puzzle_index = st.sidebar.number_input(
            "Enter Puzzle Index",  # Label for the number input
            min_value=0,  # Minimum value for the index
            max_value=len(sudoku_data) - 1,  # Maximum value for the index
            value=0,  # Default value for the index
            step=1  # Step size for the input
        )
        puzzle_string = sudoku_data.loc[puzzle_index, "puzzle"] # Get the selected puzzle string
        solution_string = sudoku_data.loc[puzzle_index, "solution"] # Get the solution string

        # Display the selected puzzle and solution
        st.write("Selected Puzzle:")
        st.write(Sudoku_Grid(puzzle_string).grid)

        st.write("Solution:")
        st.write(Sudoku_Grid(solution_string).grid)

        # Analyze solving strategies
        if st.sidebar.button("Analyze Puzzle"):
            grid = Sudoku_Grid(puzzle_string)
            solver = Sudoku_Solver(grid)
            solver.solve()

            # Collect all strategies
            strategies = {
                "Naked Singles": [str(move) for move in solver.naked_singles],
                "Hidden Singles": [str(move) for move in solver.hidden_singles],
                "Naked Pairs": [str(move) for move in solver.naked_pairs],
                "Pointing Pairs": [str(move) for move in solver.pointing_pairs],
                "Box-Line Reductions": [str(move) for move in solver.box_line_reductions],
                "X-Wings": [str(move) for move in solver.x_wings]
            }

            # Determine maximum length and pad lists
            max_length = max(len(strategy) for strategy in strategies.values())
            padded_strategies = {key: value + [""] * (max_length - len(value)) for key, value in strategies.items()}
            strategies_table = pd.DataFrame(padded_strategies)

            st.write("Strategies Table:")
            st.dataframe(strategies_table)

            # Visualize strategy usage
            all_strategies = (
                [(move, "Naked Single") for move in solver.naked_singles] +
                [(move, "Hidden Single") for move in solver.hidden_singles] +
                [(move, "Naked Pair") for move in solver.naked_pairs] +
                [(move, "Pointing Pair") for move in solver.pointing_pairs] +
                [(move, "Box-Line Reduction") for move in solver.box_line_reductions] +
                [(move, "X-Wing") for move in solver.x_wings]
            )
            strategy_counts = pd.DataFrame(all_strategies, columns=["Move", "Strategy"]).groupby("Strategy").size().reset_index(name="Frequency")

            # Plot a bar chart of strategy usage
            fig = px.bar(
                strategy_counts,
                x="Strategy",
                y="Frequency",
                title="Sudoku Strategy Usage",
                labels={"Strategy": "Strategy Type", "Frequency": "Frequency of Use"},
                text="Frequency"
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(template="plotly_white")
            st.plotly_chart(fig)

# If the user chooses to manually enter a puzzle
elif mode == "Enter Puzzle Manually":
    st.sidebar.write("Enter the Sudoku puzzle as a single 81-character string.")
    manual_puzzle = st.sidebar.text_input("Puzzle String (81 characters):", value="0" * 81)

    # Validate the input
    if len(manual_puzzle) != 81 or not manual_puzzle.isdigit():
        st.error("Please enter a valid 81-character numeric string.")
    else:
        grid = Sudoku_Grid(manual_puzzle)

        st.write("Entered Puzzle:")
        st.write(grid.grid)

        # Solve the puzzle
        if st.sidebar.button("Solve Puzzle"):
            solver = Sudoku_Solver(grid)
            solver.solve()
            st.write("Solved Puzzle:")
            st.write(grid.grid)

            # Analyze solving strategies
            strategies = {
                "Naked Singles": [str(move) for move in solver.naked_singles],
                "Hidden Singles": [str(move) for move in solver.hidden_singles],
                "Naked Pairs": [str(move) for move in solver.naked_pairs],
                "Pointing Pairs": [str(move) for move in solver.pointing_pairs],
                "Box-Line Reductions": [str(move) for move in solver.box_line_reductions],
                "X-Wings": [str(move) for move in solver.x_wings]
            }

            # Determine maximum length and pad lists
            max_length = max(len(strategy) for strategy in strategies.values())
            padded_strategies = {key: value + [""] * (max_length - len(value)) for key, value in strategies.items()}
            strategies_table = pd.DataFrame(padded_strategies)

            st.write("Strategies Table:")
            st.dataframe(strategies_table)

            # Visualize strategy usage
            all_strategies = (
                    [(move, "Naked Single") for move in solver.naked_singles] +
                    [(move, "Hidden Single") for move in solver.hidden_singles] +
                    [(move, "Naked Pair") for move in solver.naked_pairs] +
                    [(move, "Pointing Pair") for move in solver.pointing_pairs] +
                    [(move, "Box-Line Reduction") for move in solver.box_line_reductions] +
                    [(move, "X-Wing") for move in solver.x_wings]
            )
            strategy_counts = pd.DataFrame(all_strategies, columns=["Move", "Strategy"]).groupby(
                "Strategy").size().reset_index(name="Frequency")

            # Plot a bar chart of strategy usage
            fig = px.bar(
                strategy_counts,
                x="Strategy",
                y="Frequency",
                title="Sudoku Strategy Usage",
                labels={"Strategy": "Strategy Type", "Frequency": "Frequency of Use"},
                text="Frequency"
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(template="plotly_white")
            st.plotly_chart(fig)