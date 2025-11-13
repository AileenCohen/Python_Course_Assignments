import pandas as pd
import numpy as np

def calculate_pool_concentrations_from_qubit_data(conc_file: pd.DataFrame, pool_dict: dict) -> pd.DataFrame:
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




# qubit_file = pd.read_csv(r'Qubit_data_example.csv')
# pool_dictionary = {'pool_1': 5, 'pool_2': 30, 'pool_3': 100}
# result = calculate_pool_concentrations_from_qubit_data(qubit_file, pool_dictionary)

# print(result)

