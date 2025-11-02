import tkinter as tk
from tkinter import messagebox


genetic_code = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
    'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W',
}


disorder_prone_residues = {'P', 'E', 'S', 'Q', 'K', 'R', 'G'}

def check_DNA_sequence(sequence):
    valid_nucleotides = {'A', 'T', 'C', 'G'}
    for nucleotide in sequence:
        if nucleotide not in valid_nucleotides:
            return False
    return len(sequence) % 3 == 0

def translate_DNA(sequence):
    protein = ''
    for i in range(0, len(sequence) - 2, 3):
        codon = sequence[i:i+3]
        protein += genetic_code.get(codon, 'X')  # 'X' for unknown codons
    return protein

def predict_disorder(protein):
    if not protein:
        return "N/A"
    count = sum(1 for aa in protein if aa in disorder_prone_residues)
    percent = (count / len(protein)) * 100
    if percent > 30:
        return f"Likely disordered ({percent:.1f}% disorder-prone residues)"
    else:
        return f"Likely ordered ({percent:.1f}% disorder-prone residues)"

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
            text="❌ Invalid sequence. Use only A, T, G, C and \nlength must be a multiple of 3.",
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

if __name__ == "__main__":
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

    root.mainloop()
