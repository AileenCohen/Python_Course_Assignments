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


def check_DNA_sequence(sequence: str) -> bool:
    """Check that sequence contains only valid nucleotides and length is multiple of 3."""
    valid_nucleotides = {'A', 'T', 'C', 'G'}
    if not all(n in valid_nucleotides for n in sequence):
        return False
    return len(sequence) % 3 == 0

def translate_DNA(sequence: str) -> str:
    """Translate a DNA sequence into a protein sequence."""
    protein = ''
    for i in range(0, len(sequence) - 2, 3):
        codon = sequence[i:i+3]
        protein += genetic_code.get(codon, 'X')  # X for unknown codons
    return protein

def predict_disorder(protein: str) -> str:
    """Predict whether a protein is likely disordered based on disorder-prone residues."""
    if not protein:
        return "N/A"
    count = sum(1 for aa in protein if aa in disorder_prone_residues)
    percent = (count / len(protein)) * 100
    if percent > 30:
        return f"Likely disordered ({percent:.1f}% disorder-prone residues)"
    else:
        return f"Likely ordered ({percent:.1f}% disorder-prone residues)"
