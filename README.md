# Sudoku Strategy Analyzer

The **Sudoku Strategy Analyzer** is a Python-based web application that allows users to analyze and visualize solving strategies for Sudoku puzzles. Built with Streamlit, this app supports dataset uploads, manual puzzle entry, and provides insights into various solving techniques like Naked Singles, Hidden Singles, and advanced strategies like X-Wings.

## Features

- **Upload Sudoku Datasets**: Analyze multiple puzzles from a dataset (CSV format).
- **Manual Puzzle Entry**: Enter a custom puzzle for solving and strategy analysis.
- **Visualization**: Generates a bar chart showing the frequency of different solving strategies.
- **Advanced Strategies**: Supports techniques such as Naked Singles, Hidden Singles, Naked Pairs, Pointing Pairs, Box-Line Reductions, and X-Wings.

## Tech Stack

- **Python**: Core programming language
- **Streamlit**: For building an interactive web interface
- **Plotly**: For data visualization
- **Pandas**: For handling and processing datasets
- **NumPy**: For matrix operations on Sudoku grids

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ha15082005/Sudoku-Strategy-Analyzer.git
   cd Sudoku-Strategy-Analyzer
   
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt

3. Run the app:
   ``` bash
   streamlit run app.py

## Usage

### Select Puzzle from Dataset

1. Choose "Select Puzzle from Dataset" in the sidebar.
2. Upload a CSV file containing `puzzle` and `solution` columns.
3. Enter the puzzle index to analyze.
4. Click "Analyze Puzzle" to view solving strategies or "Solve Puzzle" to see the solution.

### Enter Puzzle Manually

1. Choose "Enter Puzzle Manually" in the sidebar.
2. Input an 81-character string representing the Sudoku puzzle (`0` for empty cells).
3. Click "Solve Puzzle" to solve and analyze the puzzle.

### Visualization

A bar chart is generated to display the frequency of strategies used during solving.

## File Structure

```bash
sudoku-strategy-analyzer/
├── app.py               # Main Streamlit application
├── Sudoku_Grid.py       # Sudoku grid handling logic
├── Sudoku_Solver.py     # Solver implementation with advanced strategies
├── Sudoku_Analyzer.py   # Dataset analyzer for multiple puzzles
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Example Dataset Format
| **Puzzle**                                                                                   | **Solution**                                                                               |
|---------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| 530070000600195000098000060800060003400803001700020006060000280000419005000080079           | 534678912672195348198342567859761423426853791713924856961537284287419635345286179         |
| 070000043040009610800634900094052000358460020000800530080070091902100005007040802           | 679518243543729618821634957794352186358461729216897534485276391962183475137945862         |
| 301086504046521070500000001400800002080347900009050038004090200008734090007208103           | 371986524846521379592473861463819752285347916719652438634195287128734695957268143         |
| 048301560360008090910670003020000935509010200670020010004002107090100008150834029           | 748391562365248791912675483421786935589413276673529814834962157296157348157834629         |
| 008317000004205109000040070327160904901450000045700800030001060872604000416070080           | 298317645764285139153946278327168954981453726645792813539821467872634591416579382         |

## Customization
Increase File Upload Size: The app supports large datasets by setting `maxUploadSize` to 2GB in `~/.streamlit/config.toml`
