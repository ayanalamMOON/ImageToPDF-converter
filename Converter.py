# file: main_converter.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from fallback_handler import heic_to_pdf_with_fallback

def browse_folder(entry_field):
    """Open a folder browser dialog and set the selected folder path."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, folder_path)


def browse_file(entry_field):
    """Open a file save dialog and set the selected file path."""
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, file_path)


def start_conversion(input_entry, output_entry, quality_entry, progress_bar, status_label):
    """Start the HEIC, JPEG, and PNG to PDF conversion process."""
    input_folder = input_entry.get()
    output_pdf = output_entry.get()
    try:
        compression_quality = int(quality_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Compression quality must be an integer!")
        return

    if not input_folder or not output_pdf:
        messagebox.showerror("Missing Input", "Please provide both input folder and output PDF path!")
        return

    # Call the function from fallback_handler (File B)
    supported_formats = (".heic", ".jpeg", ".jpg", ".png")
    heic_to_pdf_with_fallback(input_folder, output_pdf, compression_quality, supported_formats, progress_bar, status_label)


def create_gui():
    """Create the tkinter GUI."""
    root = tk.Tk()
    root.title("HEIC, JPEG, PNG to PDF Converter")

    # Input folder
    tk.Label(root, text="Input Folder:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    input_entry = tk.Entry(root, width=50)
    input_entry.grid(row=0, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=lambda: browse_folder(input_entry)).grid(row=0, column=2, padx=10, pady=5)

    # Output PDF file
    tk.Label(root, text="Output PDF:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    output_entry = tk.Entry(root, width=50)
    output_entry.grid(row=1, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=lambda: browse_file(output_entry)).grid(row=1, column=2, padx=10, pady=5)

    # Compression quality
    tk.Label(root, text="Compression Quality (1-100):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    quality_entry = tk.Entry(root, width=10)
    quality_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    quality_entry.insert(0, "85")  # Default value

    # Progress bar
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    # Status label
    status_label = tk.Label(root, text="Ready", anchor="w")
    status_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

    # Convert button
    tk.Button(root, text="Convert", command=lambda: start_conversion(
        input_entry, output_entry, quality_entry, progress_bar, status_label
    )).grid(row=5, column=0, columnspan=3, pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
