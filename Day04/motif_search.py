
import requests
from typing import List, Dict

JASPAR_BASE_URL = "https://jaspar.genereg.net/api/v1/"
HUMAN_TAX_ID = "9606" 

def search_jaspar_motifs(keyword: str) -> List[Dict[str, str]]:
    """
    Searches the JASPAR CORE collection for human motifs, filtering by keyword 
    and human tax_id. Returns motif metadata.
    """
    keyword = keyword.strip()
    if not keyword:
        return []

    search_url = (
        f"{JASPAR_BASE_URL}matrix/?"
        f"search={keyword}&tax_id={HUMAN_TAX_ID}&collection=CORE"
    )
    
    print(f"[LOGIC] Searching JASPAR for: '{keyword}' at {search_url}")

    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status() 
        data = response.json()
        
        results = []
        for i, motif in enumerate(data.get('results', [])):
            if i >= 10: 
                break
            
            download_url = f"{JASPAR_BASE_URL}motif/{motif.get('matrix_id')}/?fmt=pfm"
            
            results.append({
                "id": str(i + 1),
                "matrix_id": motif.get('matrix_id'),
                "name": motif.get('name'),
                "url": download_url
            })
            
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"[LOGIC] JASPAR API search error: {e}")
        return []


def download_file(url: str, output_path: str, update_callback=None) -> bool:
    """
    Downloads the actual motif data (PFM format) from the JASPAR API.
    """
    try:
        if update_callback:
            update_callback(f"Starting data fetch from: {url}")
            
        response = requests.get(url, timeout=30)
        response.raise_for_status() 

        with open(output_path, 'w') as file_handle:
            file_handle.write(response.text)

        if update_callback:
            update_callback(f"Download complete. Motif saved to: {output_path}")
        return True

    except requests.exceptions.RequestException as e:
        if update_callback:
            update_callback(f"Error during download: {e}", is_error=True)
        return False
    except Exception as e:
        if update_callback:
            update_callback(f"An unexpected error occurred: {e}", is_error=True)
        return False