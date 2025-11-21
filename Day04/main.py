
import sys
import os
import tkinter as tk
try:
    import requests
except ImportError:
    print("Error: The 'requests' library is required. Please install it with: pip install requests")
    sys.exit(1)

from motif_search_gui import JasparDownloaderApp

def main():
    """Application entry point."""
    try:
        app = JasparDownloaderApp()
        app.mainloop()
    except Exception as e:
        print(f"An application error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()