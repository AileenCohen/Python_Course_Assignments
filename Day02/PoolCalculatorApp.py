import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import argparse
import sys
# Assuming Basic_code_Assignment2 is available in the environment
from Basic_code_Assignment2 import calculate_pool_concentrations_from_qubit_data
import re # We need the regex module for parsing the complex user input

# ---------------- GUI ----------------
# ... (GUI code remains the same as before) ...
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

# ---------------- Interactive (Original) ----------------
def interactive_mode():
    file_path = input("Enter the path to your CSV file: ").strip()
    pool_values_str = input("Enter pool values separated by commas (e.g. 5, 30, 100): ").strip()
    try:
        pool_values = [float(v.strip()) for v in pool_values_str.split(",")]
    except ValueError:
        print("Error: Invalid pool values. Use numbers separated by commas.")
        sys.exit(1)
        
    pool_dict = {f"pool_{i+1}": val for i, val in enumerate(pool_values)}
    try:
        df = pd.read_csv(file_path)
        result = calculate_pool_concentrations_from_qubit_data(df, pool_dict)
        print("\nResult:\n")
        print(result)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

# ---------------- CLI (Original) ----------------
def cli_mode(args):
    # This is only executed if arguments were passed upon script startup.
    if not args.file or not args.pools:
        print("Error: --file and --pools are required in CLI mode.")
        sys.exit(1)

    pool_dict = {f"pool_{i+1}": val for i, val in enumerate(args.pools)}
    
    try:
        df = pd.read_csv(args.file)
        result = calculate_pool_concentrations_from_qubit_data(df, pool_dict)
        print(result)
    except FileNotFoundError:
        print(f"Error: File not found at path: {args.file}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during calculation: {e}")
        sys.exit(1)

# ---------------- INTERACTIVE CLI INPUT ----------------
def interactive_cli_prompt():
    
    print("\n--- Command-line Mode Selected ---")
    print("Please enter the command you would normally use, but omit the 'python' and script name.")
    print("Example (copy and paste, replacing the bolded parts):")
    print("  --file **INSERT YOUR FILE PATH** --pools **INSERT POOL SIZES WITH A SPACE**")
    
    user_input = input("\nEnter your CLI arguments: ").strip()
  
    try:
      
        temp_parser = argparse.ArgumentParser()
        temp_parser.add_argument("--file", required=True)
        temp_parser.add_argument("--pools", nargs="+", type=float, required=True)
        
        args_list = re.findall(r'(?:[^\s"]|"(?:\\.|[^"])*")+', user_input)
        
        temp_args = temp_parser.parse_args(args_list)
        
    except argparse.ArgumentError as e:
        print(f"\nError: Could not parse input. Please check your format.")
        print(f"Detail: {e}")
        sys.exit(1)
    except Exception:
        print("\nError: Invalid input format. Ensure you have --file and --pools followed by values.")
        sys.exit(1)

    
    cli_mode(temp_args)


# ---------------- Mode selection ----------------
def choose_mode():
    print("\nSelect mode:")
    print("1. Interactive (manual input)")
    print("2. Command-line (use arguments)") # This now leads to the interactive_cli_prompt
    print("3. GUI (graphical interface)\n")

    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice in ["1", "2", "3"]:
            return {"1": "interactive", "2": "cli_prompt", "3": "gui"}[choice] # Changed 'cli' to 'cli_prompt'
        else:
            print("Invalid choice. Please try again.")

# ---------------- Main ----------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pool Concentration Calculator")
    parser.add_argument("--mode", choices=["interactive", "cli", "gui"], help="Choose input mode")
    parser.add_argument("--file", help="Path to CSV file (CLI mode only)")
    parser.add_argument("--pools", nargs="+", type=float, help="Pool concentration values (CLI mode only)")
    args = parser.parse_args()

    mode = args.mode 

    
    if args.file and args.pools:
        mode = "cli"
    
    # 2. Manual mode selection if no arguments were provided or --mode was used
    if not mode:
        
        if args.file or args.pools:
             print("Error: When starting the script, --file and --pools must both be provided.")
             sys.exit(1)
             
        mode = choose_mode()


    if mode == "interactive":
        interactive_mode()
    elif mode == "cli":
        cli_mode(args)
    elif mode == "cli_prompt": # Execute the new interactive function when 2 is chosen
        interactive_cli_prompt()
    elif mode == "gui":
        start_gui()