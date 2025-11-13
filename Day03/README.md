# Pool Concentration Calculator

This code calculates the required volume (the "Amount to Take") for DNA samples based on their measured concentration and a set of target "pool" concentrations.

---

## Installation and Setup

1. **Clone the repository:**

```bash
git clone https://github.com/AileenCohen/Python_Course_Assignments
```

2. **Change into the correct directory:**

```bash
cd Python_Course_Assignments/Day03/
```

3. **Install required Python packages:**

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
python PoolCalculatorApp.py
```


## When will you need to use something like that?

When you’re preparing DNA for next-generation sequencing, you often have many different samples or libraries that you want to sequence together in the same run.
To do this safely and efficiently, you need to mix the samples in the right proportions so that:

* Each sample contributes enough DNA to be properly sequenced.
* No sample overpowers the others (so you don’t get too many results from one and too few from another).

A pool concentration calculator tells you exactly how much of each sample to add to the pool based on:

* The measured concentration of each DNA sample.
* The desired final concentration for sequencing.

Think of it like making a smoothie from fruits of different sizes: you want each fruit to contribute the right amount so that every flavor is balanced.

---

## Folder Structure

* **Basic_code_Assignment.py**: Contains the core calculation function.
* **PoolCalculatorApp.py**: The main application runner, providing GUI, CLI, interactive modes, and a dedicated test runner.
* **test_calculations.py**: Pytest unit tests for validating the code.
* **Qubit_data_example.csv**: Sample data file for testing the application. **This application requires a CSV file of concentrations!**
* **requirements.txt**: Lists all required Python packages for easy installation.

---

## Prompts I used:

### AI used: Gemini

Make testing functions using pytest for the provided code (pasted the Basic_code and the calculator app) and add a testing function to the original calculator app. The tests should be in a file called test_calculations.py that can be called upon using pytest.
