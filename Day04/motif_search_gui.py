
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Dict
from motif_search import search_jaspar_motifs, download_file 


class JasparDownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JASPAR Motif Downloader (Human TFs)")
        self.geometry("600x400") 
        self.results_data: List[Dict[str, str]] = [] 
        
        style = ttk.Style(self)
        style.theme_use('clam')  
        style.configure('TButton', font=('Helvetica', 10, 'bold'))
        style.configure('TLabel', font=('Helvetica', 10))
        
        self.grid_rowconfigure(2, weight=1) 
        self.grid_columnconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="15") 
        main_frame.grid(row=0, column=0, sticky="nsew", rowspan=4)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        search_frame.columnconfigure(1, weight=1) # Make entry field expand
        
        ttk.Label(search_frame, text="TF Name (e.g., 'FOS', 'STAT1'):").grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")
        self.keyword_entry = ttk.Entry(search_frame, width=30)
        self.keyword_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=5)
        self.search_button = ttk.Button(search_frame, text="Search JASPAR", command=self.handle_search)
        self.search_button.grid(row=0, column=2, sticky="e")

        self.status_var = tk.StringVar(value="Enter a human TF name and click Search.")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.RIDGE, anchor=tk.W) 
        self.status_label.grid(row=1, column=0, sticky="ew", pady=(0, 10), ipady=5)
        
        results_frame = ttk.Frame(main_frame)
        results_frame.grid(row=2, column=0, sticky="nsew", padx=(0, 0))
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        self.results_list = ttk.Treeview(results_frame, columns=('Matrix ID', 'TF Name'), show='headings', selectmode='browse')
        
        self.results_list.heading('Matrix ID', text='Matrix ID', anchor=tk.W)
        self.results_list.column('Matrix ID', width=120, stretch=tk.NO)
        self.results_list.heading('TF Name', text='Transcription Factor Name', anchor=tk.W)
        self.results_list.column('TF Name', stretch=tk.YES)
        
        vsb = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_list.yview)
        self.results_list.configure(yscrollcommand=vsb.set)
        
        self.results_list.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky='ns')
        
        self.results_list.bind('<<TreeviewSelect>>', self.enable_download) 

        download_frame = ttk.Frame(main_frame)
        download_frame.grid(row=3, column=0, sticky="ew", pady=(15, 0))
        self.download_button = ttk.Button(download_frame, text="⬇️ Download Selected Motif (PFM Format)", 
                                          state=tk.DISABLED, command=self.handle_download)
        self.download_button.pack(fill=tk.X)


    def update_status(self, message: str, is_error: bool = False):
        """Updates the GUI status label."""
        self.status_var.set(message)
        self.status_label.config(foreground='red' if is_error else 'black')
        self.update_idletasks()

    def handle_search(self):
        """Calls the business logic to search and updates the UI."""
        keyword = self.keyword_entry.get().strip()
        self.update_status(f"Searching JASPAR for motifs matching '{keyword}'...")
        
        for i in self.results_list.get_children():
            self.results_list.delete(i)
        self.download_button.config(state=tk.DISABLED)

        self.results_data = search_jaspar_motifs(keyword) 
        
        if not self.results_data:
            self.update_status("No motifs found. Check spelling or try a broader search.", is_error=True)
            return

        for item in self.results_data:
            self.results_list.insert('', tk.END, iid=item['id'], values=(item['matrix_id'], item['name']))

        self.update_status(f"Found {len(self.results_data)} matching motifs. Select one to download.")

    def enable_download(self, event):
        """Enables the download button when a result is selected."""
        if self.results_list.selection():
            self.download_button.config(state=tk.NORMAL)
        else:
            self.download_button.config(state=tk.DISABLED)

    def handle_download(self):
        """Calls the business logic to download the selected file."""
        try:
            selected_item_id = self.results_list.selection()[0]
            selected_result = next(r for r in self.results_data if r["id"] == selected_item_id)
        except (IndexError, StopIteration):
            self.update_status("Please select a motif from the list.", is_error=True)
            return

        url = selected_result['url']
        default_filename = f"{selected_result['matrix_id']}_{selected_result['name']}.pfm"
        
        output_path = filedialog.asksaveasfilename(
            defaultextension=".pfm",
            initialfile=default_filename.replace('::', '-'),
            title="Save JASPAR Motif File",
            filetypes=[("PFM Motif Files", "*.pfm"), ("All files", "*.*")]
        )

        if not output_path:
            self.update_status("Download canceled by user.")
            return

        self.download_button.config(state=tk.DISABLED)
        
        success = download_file(url, output_path, update_callback=self.update_status)
        
        self.download_button.config(state=tk.NORMAL)
        if success:
            messagebox.showinfo("Success", f"Motif file downloaded successfully to:\n{output_path}")
        else:
            messagebox.showerror("Error", self.status_var.get())