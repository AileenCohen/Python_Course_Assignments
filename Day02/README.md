---
layout: default
title: About
---

## AI used for Class written assignment:
**Copilot**

## Prompts used:
1. Make a GUI from the provided code and use the tk library with 3 ways to provide the input including a command line, an input function and a GUI input, let me choose which one to use when I'm running the code.
The basic code (this python file is in the assignment submittion as well):
[Basic_code_Assignment2.py](https://github.com/user-attachments/files/23395704/Basic_code_Assignment2.py)
import pandas as pd
import numpy as np

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



qubit_file = pd.read_csv(r'Qubit_data_example.csv')
pool_dictionary = {'pool_1': 5, 'pool_2': 30, 'pool_3': 100}
result = calculate_pool_concentrations_from_qubit_data(qubit_file, pool_dictionary)

print(result)

