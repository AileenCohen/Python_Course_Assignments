import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import argparse
import sys

def calculate_pool_concentrations_from_qubit_data(conc_file, pool_dict):
    samples = conc_file["Sample Name"].astype(str).tolist()
    concentrations = pd.to_numeric(conc_file["Original Sample Conc."], errors='coerce')

    pools = sorted(pool_dict.values())
    amount_to_take = {}

    for i, conc in enumerate(concentrations):
        if pd.isna(conc) or conc == 0:
            amount_to_take[samples[i]] = np.nan
            continue

        assigned = False
        for pool in pools:
            if conc < pool:
                amount_to_take[samples[i]] = pool / conc
                assigned = True
                break

        if not assigned:
            amount_to_take[samples[i]] = pools[-1] / conc

    plate = pd.DataFrame(list(amount_to_take.items()), columns=['Sample', 'Amount_to_Take'])
    return plate



def start_gui():
    def run_calculation():
        file_path = file_path_var.get()
        pool_values_str = pool_values_var.get()

        if not file_path:
            messagebox.showerror("Error", "Please select a file.")
            return

        try:
            pool_values = [float(v.strip()) for v in pool_values_str.split(",")]
        except ValueError:
            messagebox.showerror("Error", "Invalid pool values. Use numbers separated by commas.")
            return

        pool_dict = {f"pool_{i+1}": val for i, val in enumerate(pool_values)}
        try:
            df = pd.read_csv(file_path)
            result = calculate_pool_concentrations_from_qubit_data(df, pool_dict)
            result_window = tk.Toplevel(root)
            result_window.title("Result")
            text = tk.Text(result_window, wrap="none")
            text.insert("1.0", result.to_string(index=False))
            text.pack(expand=True, fill="both")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def browse_file():
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if path:
            file_path_var.set(path)

    root = tk.Tk()
    root.title("Pool Concentration Calculator")

    tk.Label(root, text="CSV File:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    file_path_var = tk.StringVar()
    tk.Entry(root, textvariable=file_path_var, width=40).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse", command=browse_file).grid(row=0, column=2, padx=5, pady=5)

    tk.Label(root, text="Pool values (comma-separated):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    pool_values_var = tk.StringVar(value="5, 30, 100")
    tk.Entry(root, textvariable=pool_values_var, width=40).grid(row=1, column=1, padx=5, pady=5)

    tk.Button(root, text="Run", command=run_calculation).grid(row=2, column=0, columnspan=3, pady=10)

    root.mainloop()



def interactive_mode():
    file_path = input("Enter the path to your CSV file: ").strip()
    pool_values_str = input("Enter pool values separated by commas (e.g. 5, 30, 100): ").strip()
    pool_values = [float(v.strip()) for v in pool_values_str.split(",")]
    pool_dict = {f"pool_{i+1}": val for i, val in enumerate(pool_values)}

    df = pd.read_csv(file_path)
    result = calculate_pool_concentrations_from_qubit_data(df, pool_dict)
    print("\nResult:\n")
    print(result)



def cli_mode(args):
    if not args.file or not args.pools:
        print("Error: --file and --pools are required in CLI mode.")
        sys.exit(1)

    pool_dict = {f"pool_{i+1}": val for i, val in enumerate(args.pools)}
    df = pd.read_csv(args.file)
    result = calculate_pool_concentrations_from_qubit_data(df, pool_dict)
    print(result)



def choose_mode():
    print("\nSelect mode:")
    print("1. Interactive (manual input)")
    print("2. Command-line (use arguments)")
    print("3. GUI (graphical interface)\n")

    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice in ["1", "2", "3"]:
            return {"1": "interactive", "2": "cli", "3": "gui"}[choice]
        else:
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pool Concentration Calculator")
    parser.add_argument("--mode", choices=["interactive", "cli", "gui"], help="Choose input mode: interactive / cli / gui")
    parser.add_argument("--file", help="Path to the CSV file (CLI mode only)")
    parser.add_argument("--pools", nargs="+", type=float, help="Pool concentration values (CLI mode only)")
    args = parser.parse_args()

    # If no mode was provided, ask user interactively
    mode = args.mode or choose_mode()

    if mode == "interactive":
        interactive_mode()
    elif mode == "cli":
        cli_mode(args)
    elif mode == "gui":
        start_gui()
