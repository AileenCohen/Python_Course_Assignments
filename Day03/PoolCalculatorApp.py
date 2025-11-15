import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import argparse
import sys
import os
import pytest
from Basic_code_Assignment2 import calculate_pool_concentrations_from_qubit_data

# ---------------- GUI ----------------
def start_gui():
    root = tk.Tk()
    root.withdraw() 

    def run_calculation():
        file_path = file_path_var.get()
        pool_values_str = pool_values_var.get()

        if not file_path:
            messagebox.showerror("Error", "Please select a file.")
            return

        try:
            # Check if pool values string is empty
            if not pool_values_str.strip():
                messagebox.showerror("Error", "Pool values cannot be empty.")
                return
                
            pool_values = [float(v.strip()) for v in pool_values_str.split(",")]
        except ValueError:
            messagebox.showerror("Error", "Invalid pool values. Use numbers separated by commas (e.g., 5, 30, 100).")
            return

        pool_dict = {f"pool_{i+1}": val for i, val in enumerate(pool_values)}
        
        try:
            df = pd.read_csv(file_path)
            result = calculate_pool_concentrations_from_qubit_data(df, pool_dict)
            
            # Use a new Toplevel window for results
            result_window = tk.Toplevel() 
            result_window.title("Calculation Result")
            text = tk.Text(result_window, wrap="none")
            text.insert("1.0", result.to_string(index=False))
            text.pack(expand=True, fill="both")
        except Exception as e:
            messagebox.showerror("Error", f"Calculation failed: {str(e)}")

    def browse_file():
        # Open file dialog relative to the hidden root
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if path:
            file_path_var.set(path)
            # Bring the input window back to focus after dialog closes
            input_window.lift()

    # --- Setup the input window (Toplevel allows for a secondary functional window) ---
    input_window = tk.Toplevel(root)
    input_window.title("Pool Concentration Calculator")

    # File path input
    tk.Label(input_window, text="CSV File:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    file_path_var = tk.StringVar()
    tk.Entry(input_window, textvariable=file_path_var, width=40).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(input_window, text="Browse", command=browse_file).grid(row=0, column=2, padx=5, pady=5)

    # Pool values input
    tk.Label(input_window, text="Pool values (comma-separated):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    pool_values_var = tk.StringVar(value="5, 30, 100")
    tk.Entry(input_window, textvariable=pool_values_var, width=40).grid(row=1, column=1, padx=5, pady=5)

    # Run button
    tk.Button(input_window, text="Run Calculation", command=run_calculation).grid(row=2, column=0, columnspan=3, pady=10)

    root.mainloop() # Start the Tkinter event loop

# ---------------- Interactive ----------------
def interactive_mode():

    try:
        file_path = input("Enter the path to your CSV file: ").strip()
        pool_values_str = input("Enter pool values separated by commas (e.g. 5, 30, 100): ").strip()
        
        # Parse and validate inputs
        if not pool_values_str.strip():
            print("\nError: Pool values cannot be empty.")
            return

        pool_values = [float(v.strip()) for v in pool_values_str.split(",")]
        pool_dict = {f"pool_{i+1}": val for i, val in enumerate(pool_values)}

        df = pd.read_csv(file_path)
        result = calculate_pool_concentrations_from_qubit_data(df, pool_dict)
        print("\n--- Calculation Result ---\n")
        print(result.to_string(index=False))

    except FileNotFoundError:
        print(f"\nError: File not found at '{file_path}'.")
    except ValueError as e:
        print(f"\nError processing input: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

# ---------------- CLI ----------------
def cli_mode(args):
    try:
        if not args.file or not args.pools:

            print("\n--- CLI Mode Usage ---")
            print("CLI mode requires arguments to be provided when the script starts.")
            print("Please run the script again using the following format:")
            print(f"python {os.path.basename(sys.argv[0])} --file **INSERT YOUR FILE PATH** --pools **INSERT POOL SIZES WITH A SPACE**")
            print("Example: python PoolCalculatorApp.py --file data.csv --pools 5 30 100")
            print("\nExiting...")
            sys.exit(1)

        # Execution for valid CLI arguments
        pool_dict = {f"pool_{i+1}": val for i, val in enumerate(args.pools)}
        df = pd.read_csv(args.file)
        result = calculate_pool_concentrations_from_qubit_data(df, pool_dict)
        print(result.to_string(index=False))
        
    except FileNotFoundError:
        print(f"\nError: File not found at '{args.file}'.")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred in CLI mode: {e}")
        sys.exit(1)

# ---------------- Pytest Test Mode ----------------
def test_mode():

    """Runs all unit tests defined in test_calculations.py using pytest."""
    print("\n--- Running Pytest Unit Tests ---\n")
    
    # Get the directory of the currently running script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_file_path = os.path.join(current_dir, "test_calculations.py")
    
    if not os.path.exists(test_file_path):
        print(f"ERROR: Test file not found at expected path: {test_file_path}")
        print("Please ensure 'test_calculations.py' is in the same directory as this script.")
        return

    # Use pytest.main to run the tests programmatically
    # The exit code from pytest determines success/failure
    exit_code = pytest.main([test_file_path])

    if exit_code == 0:
        print("\n--- ALL TESTS PASSED SUCCESSFULLY! ---")
    else:
        print(f"\n--- TESTS FAILED (Exit Code: {exit_code}) ---")

# ---------------- Mode selection ----------------
def choose_mode():
    print("\nSelect Mode:")
    print("1. Interactive (manual console input)")
    print("2. Command-line (use --file and --pools arguments)")
    print("3. GUI (graphical interface)")
    print("4. Run Unit Tests\n")

    while True:
        choice = input("Enter 1, 2, 3, or 4: ").strip()
        if choice in ["1", "2", "3", "4"]:
            return {"1": "interactive", "2": "cli", "3": "gui", "4": "test"}[choice]
        else:
            print("Invalid choice. Please try again.")

# ---------------- Main ----------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pool Concentration Calculator")
    parser.add_argument("--mode", choices=["interactive", "cli", "gui", "test"], help="Choose input mode")
    parser.add_argument("--file", help="Path to CSV file (CLI mode only)")
    parser.add_argument("--pools", nargs="+", type=float, help="Pool concentration values (CLI mode only)")
    args = parser.parse_args()


    mode = args.mode 

    if args.file and args.pools:
        mode = "cli"

    if not mode:

        if args.file or args.pools:
             print("Error: In CLI mode, both --file and --pools arguments must be provided.")
             sys.exit(1)
             

        mode = choose_mode()

    if mode == "interactive":
        interactive_mode()
    elif mode == "cli":
        cli_mode(args) 
    elif mode == "gui":
        start_gui()
    elif mode == "test":
        test_mode()