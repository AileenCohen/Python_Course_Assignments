# JASPAR Motif finder (of human transcription factors only)

A simple tool, using Python + Tkinter, that lets you **search and download transcription factor (TF) binding motifs** from the **JASPAR CORE (human) database**.
---

##  What Is a Motif, and What Can You Use This Application For?
A **motif** is a short DNA sequence that a TF recognizes and binds to (on our DNA). 

- Each TF has its own preferred sequence pattern.
- These patterns are usually described using a **Position Frequency Matrix (PFM)**, which counts how often each nucleotide appears at each position.
- You can use PFMs for:  
  - Predicting where TFs bind in the genome  
  - Studying gene regulation  
  - Scanning promoter regions  
  - Motif enrichment analysis  


---

## Folder Structure

| File | Purpose |
|------|---------|
| **motif_search.py** | Connecting to JASPAR: searching motifs, downloading PFMs. |
| **motif_search_gui.py** | The Tkinter interface. Buttons, lists, and calling the search function. |
| **main.py** | The launcher file. It loads and starts the GUI. |

---

## How to Run
### 1. Install Dependencies
```bash
pip install requests
```

### 2. Start the App
```bash
python main.py
```

---

If you need this for your TF binding analysis, there you go!
Enjoy!

### AI usage:
#### AI used:
Gemini

#### Prompts:
- Build me a function that searches JASPAR for the best possible motifs of human TFs (only) of my choosing. I provide a TF's name and the input, and I get the top PFM results as the output, allowing me to download the PFM of my choice.
- Add a gui to this function in which I can input my TF of choice and get the list of outputs to choose what to download.
- Separate the search and download function from the gui function, separate that from the calling of the function.
