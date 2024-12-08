import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
from fallback_handler import heic_to_pdf_with_fallback

class DragDropEntry(tk.Entry):
    """Custom Entry widget with drag and drop support"""
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.drop)
        self.bind('<3>', self.show_context_menu)  # Right-click menu
        
    def drop(self, event):
        path = event.data
        if os.path.exists(path):
            self.delete(0, tk.END)
            self.insert(0, path)
            
    def show_context_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Paste", command=self.paste)
        menu.add_command(label="Clear", command=lambda: self.delete(0, tk.END))
        menu.post(event.x_root, event.y_root)
        
    def paste(self):
        self.event_generate('<<Paste>>')

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
    """Create the tkinter GUI with drag-drop and shortcuts."""
    root = TkinterDnD.Tk()  # Use TkinterDnD instead of regular Tk
    root.title("HEIC, JPEG, PNG to PDF Converter")
    
    # Keyboard shortcuts
    def handle_shortcuts(event):
        if event.state & 4:  # Control key
            if event.keysym == 'o':  # Ctrl+O
                browse_folder(input_entry)
                return "break"
            elif event.keysym == 's':  # Ctrl+S
                browse_file(output_entry)
                return "break"
            elif event.keysym == 'Return':  # Ctrl+Enter
                start_conversion(input_entry, output_entry, quality_entry, progress_bar, status_label)
                return "break"

    root.bind('<Key>', handle_shortcuts)

    # Create tooltip function
    def create_tooltip(widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
            
        widget.bind('<Enter>', show_tooltip)

    # Modify input/output entries to use drag-drop
    input_entry = DragDropEntry(root, width=50)
    input_entry.grid(row=0, column=1, padx=10, pady=5)
    create_tooltip(input_entry, "Drag & drop folder here or Ctrl+O to browse")

    output_entry = DragDropEntry(root, width=50)
    output_entry.grid(row=1, column=1, padx=10, pady=5)
    create_tooltip(output_entry, "Drag & drop or Ctrl+S to save PDF")

    # Add shortcut hints to labels
    tk.Label(root, text="Input Folder (Ctrl+O):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(root, text="Output PDF (Ctrl+S):").grid(row=1, column=0, padx=10, pady=5, sticky="e")

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

    # Update Convert button with shortcut hint
    convert_btn = tk.Button(root, text="Convert (Ctrl+Enter)", 
                          command=lambda: start_conversion(
                              input_entry, output_entry, quality_entry, progress_bar, status_label
                          ))
    convert_btn.grid(row=5, column=0, columnspan=3, pady=10)

    # Keyboard shortcut label
    shortcuts_text = """
    Shortcuts:
    Ctrl+O: Browse Input Folder
    Ctrl+S: Save PDF
    Ctrl+Enter: Convert
    """
    shortcuts_label = tk.Label(root, text=shortcuts_text, justify=tk.LEFT, font=("Courier", 8))
    shortcuts_label.grid(row=6, column=0, columnspan=3, pady=5)

    return root

if __name__ == "__main__":
    root = create_gui()
    root.mainloop()
