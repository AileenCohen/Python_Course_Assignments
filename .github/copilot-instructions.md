# Copilot instructions for this repository

Purpose: Give AI coding agents the minimal, concrete knowledge needed to be productive in this repo.

## Overview

This workspace contains self-contained daily Python exercises (Day01/ .. Day04/) for a Python course.
Each day is effectively its own mini-project: source, frontends, and tests live inside the day directory.

## Big picture & architecture (what to know immediately)

### Day 02 & 03 (Pool Calculator):

The canonical logic library is Basic_code_Assignment2.py.

Public API function: calculate_pool_concentrations_from_qubit_data(conc_file, pool_dict).

Day02 is the prototype; Day03 is the refined, production-ready version with pytest integration.

Frontend: PoolCalculatorApp.py handles the UI (Tkinter) and input parsing, calling the logic library.

### Day 04 (JASPAR Motif Finder):

Architecture: Distinct separation of concerns.

motif_search.py: Business Logic. Handles JASPAR API connection (requests), JSON parsing, and PFM downloading.

motif_search_gui.py: Frontend. Pure Tkinter UI. Calls motif_search functions but contains no API logic itself.

main.py: The entry point launcher.

## Project-specific conventions (Strict)

Bioinformatics Context First: Every README.md and every major module docstring must explain the biological "Why" (e.g., why do we care about protein disorder? why do we pool DNA?) before explaining the code.

Modularity:

Logic: Calculations and Data processing must happen in a dedicated file (e.g., Basic_code_Assignment2.py, motif_search.py).

GUI: Interface code (tkinter) must be in a separate file (e.g., motif_search_gui.py, PoolCalculatorApp.py).

**Never mix them.**

## Data Handling:

Use pandas DataFrames for tabular data (concentrations, plate maps).

Motif data is handled as Position Frequency Matrices (PFMs).

Key Dependencies: pandas, numpy, requests, pytest, tkinter.

Key files to inspect / copy patterns from

Logic Pattern: Day03/Basic_code_Assignment2.py — Clean function definition taking raw data and returning a processed DataFrame.

GUI Pattern: Day04/motif_search_gui.py — Shows how to build a Tkinter class that takes user input and calls the backend logic.

Testing Pattern: Day03/test_calculations.py — Uses pytest to validate the core logic. Note how it imports from the local directory.

API Pattern: Day04/motif_search.py — Shows how to query an external DB (JASPAR), handle errors, and parse results.

## Developer workflows & commands

Run a specific application: Navigate to the folder and run the launcher.
```
cd Day04
python main.py
```

Run Tests: Navigate to the folder and run pytest.
```
cd Day03
python -m pytest
```

Dependencies: Check requirements.txt in the specific Day folder (e.g., Day03/requirements.txt).

## Patterns, error handling & integration points

Error Model: Backend functions should raise exceptions (e.g., ValueError if TF not found). Frontends catch these and display user-friendly popups (messagebox).

Input Data: The Pool Calculator expects a CSV with specific headers ("Sample Name", "Original Sample Conc."). Ensure new mock data follows Qubit_data_example.csv.

Small actionable rules for an AI coding agent

Read the README first: Before writing code, check the local README.md to understand the biological goal.

Separate Logic/UI: If asked to create a new tool, immediately create two files: tool_logic.py and tool_gui.py.

Use Pytest: If modifying Day03 or creating Day05+, always create a test_*.py file.

No Hardcoding: Do not hardcode paths to CSVs. Allow the user to select files via GUI or CLI arguments.

Environment: Assume Python 3.8+.