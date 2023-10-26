import tkinter as tk
from tkinter import filedialog, messagebox
import tabula
from PyPDF2 import PdfReader
import pandas as pd

def extract_text_and_tables():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    
    if file_path:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "File uploaded successfully.\nExtracting text and tables...")
        result_text.update_idletasks()
        
        try:
            pdf_reader = PdfReader(file_path)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            result_text.insert(tk.END, "\n\nText from PDF:\n")
            result_text.insert(tk.END, text)
        except Exception as e:
            result_text.insert(tk.END, f"\n\nAn error occurred while extracting text: {str(e)}")

        try:
            tables = tabula.read_pdf(file_path, pages="all", multiple_tables=True)

            if tables:
                result_text.insert(tk.END, "\n\nTables extracted successfully.\n")
                
                consolidated_table = pd.concat(tables, ignore_index=True)

                result_text.insert(tk.END, "\nConsolidated Table:\n")
                result_text.insert(tk.END, consolidated_table.to_string())

                def export_to_csv():
                    csv_filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
                    if csv_filename:
                        consolidated_table.to_csv(csv_filename, index=False)
                        result_text.insert(tk.END, f"\n\nConsolidated table exported to {csv_filename}")

                export_button = tk.Button(root, text="Export Consolidated Table to CSV", command=export_to_csv)
                export_button.pack()

            else:
                result_text.insert(tk.END, "\n\nNo tables found in the PDF.")
        except Exception as e:
            result_text.insert(tk.END, f"\n\nAn error occurred while processing tables: {str(e)}")
    
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Upload a PDF file to start the extraction.")

root = tk.Tk()
root.title("PDF Text and Table Extractor")

upload_button = tk.Button(root, text="Upload a PDF file", command=extract_text_and_tables)
upload_button.pack()

result_text = tk.Text(root, wrap=tk.WORD, width=80, height=20)
result_text.pack()

root.mainloop()
