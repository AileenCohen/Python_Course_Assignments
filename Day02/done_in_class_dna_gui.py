import tkinter as tk
from tkinter import messagebox
from done_in_class_dna_utils import check_DNA_sequence, translate_DNA, predict_disorder


def validate_sequence(event=None):
    sequence = entry.get("1.0", tk.END).strip().upper()
    length = len(sequence)
    length_label.config(text=f"Length: {length} ({'✓' if length % 3 == 0 else '✗'})")

    invalid = [n for n in sequence if n not in {'A', 'T', 'C', 'G'}]
    if invalid:
        result_label.config(text=f"❌ Invalid characters: {', '.join(set(invalid))}", fg="red")
        protein_label.config(text="")
        disorder_label.config(text="")
        return

    if not check_DNA_sequence(sequence):
        result_label.config(
            text="❌ Invalid sequence. Use only A, T, G, C and length must be a multiple of 3.",
            fg="red"
        )
        protein_label.config(text="")
        disorder_label.config(text="")
        return

    result_label.config(text="✅ Valid DNA sequence.", fg="green")
    protein = translate_DNA(sequence)
    disorder = predict_disorder(protein)
    protein_label.config(text=f"Protein: {protein}")
    disorder_label.config(text=f"Disorder Prediction: {disorder}")

def clear_input():
    entry.delete("1.0", tk.END)
    result_label.config(text="")
    protein_label.config(text="")
    disorder_label.config(text="")
    length_label.config(text="Length: 0")

def start_gui():
    global root, entry, result_label, protein_label, disorder_label, length_label

    root = tk.Tk()
    root.title("DNA Sequence Validator & Translator")
    root.geometry("600x350")
    root.resizable(False, False)

    label = tk.Label(root, text="Enter your DNA sequence:")
    label.grid(row=0, column=0, columnspan=2, pady=(15, 5), padx=10)

    entry = tk.Text(root, height=4, width=70)
    entry.grid(row=1, column=0, columnspan=2, padx=10)
    entry.bind("<Return>", validate_sequence)
    entry.bind("<KeyRelease>", validate_sequence)

    result_label = tk.Label(root, text="", font=("Arial", 10))
    result_label.grid(row=3, column=0, columnspan=2, pady=5)

    protein_label = tk.Label(root, text="", font=("Courier", 10), wraplength=550, justify="left")
    protein_label.grid(row=4, column=0, columnspan=2, pady=5)

    disorder_label = tk.Label(root, text="", font=("Arial", 10))
    disorder_label.grid(row=5, column=0, columnspan=2, pady=5)

    length_label = tk.Label(root, text="Length: 0", font=("Arial", 9))
    length_label.grid(row=6, column=0, columnspan=2, pady=(0, 10))

    clear_button = tk.Button(root, text="Clear", command=clear_input)
    clear_button.grid(row=7, column=0, columnspan=2, pady=5)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
