import os
import logging
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD

from fallback_handler import heic_to_pdf_with_fallback

class DragDropEntry(tk.Entry):
    """Custom Entry widget with drag and drop support."""
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
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )
    if file_path:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, file_path)

def start_conversion(
    input_entry, output_entry, quality_entry, progress_bar, status_label,
    recursive=True, min_date=None, skip_converted=True, delete_source=False,
    pdf_options=None
):
    """Start the HEIC, JPEG, PNG, BMP, and GIF to PDF conversion process."""
    input_folder = input_entry.get()
    output_pdf = output_entry.get()
    try:
        compression_quality = int(quality_entry.get())
    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Compression quality must be an integer!"
        )
        return

    if not input_folder or not output_pdf:
        messagebox.showerror(
            "Missing Input",
            "Please provide both input folder and output PDF path!"
        )
        return

    # Call the function from fallback_handler
    supported_formats = (".heic", ".jpeg", ".jpg", ".png", ".bmp", ".gif")
    heic_to_pdf_with_fallback(
        input_folder, output_pdf, compression_quality, supported_formats,
        progress_bar, status_label, pdf_options=pdf_options,
        recursive=recursive, min_date=min_date,
        skip_converted=skip_converted, delete_source=delete_source
    )

def show_error_logs():
    """Display error logs in a new window."""
    log_window = tk.Toplevel()
    log_window.title("Error Logs")
    log_window.geometry("600x400")

    text_widget = tk.Text(log_window, wrap=tk.WORD)
    text_widget.pack(expand=True, fill='both')

    scrollbar = tk.Scrollbar(log_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text_widget.yview)

    try:
        log_files = sorted(
            [f for f in os.listdir("logs") if f.endswith(".log")],
            reverse=True
        )
        if log_files:
            with open(os.path.join("logs", log_files[0])) as f:
                text_widget.insert('1.0', f.read())
        else:
            text_widget.insert('1.0', "No log files found.")
    except Exception as e:
        text_widget.insert('1.0', f"Error reading logs: {str(e)}")

def create_gui():
    """Create the tkinter GUI with PDF customization options."""
    root = TkinterDnD.Tk()  # Use TkinterDnD instead of regular Tk
    root.title("HEIC, JPEG, PNG, BMP, GIF to PDF Converter")

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
                enhanced_start_conversion()
                return "break"

    root.bind('<Key>', handle_shortcuts)

    # Create tooltip function
    def create_tooltip(widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")

            label = tk.Label(
                tooltip, text=text, background="#ffffe0",
                relief="solid", borderwidth=1
            )
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
    tk.Label(
        root, text="Input Folder (Ctrl+O):"
    ).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(
        root, text="Output PDF (Ctrl+S):"
    ).grid(row=1, column=0, padx=10, pady=5, sticky="e")

    # Compression quality
    tk.Label(
        root, text="Compression Quality (1-100):"
    ).grid(row=2, column=0, padx=10, pady=5, sticky="e")
    quality_entry = tk.Entry(root, width=10)
    quality_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    quality_entry.insert(0, "85")  # Default value

    # Add date filter frame
    date_frame = ttk.LabelFrame(root, text="Filter Options")
    date_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    # Date filter
    tk.Label(date_frame, text="Modified after:").pack(side=tk.LEFT, padx=5)
    date_var = tk.StringVar(value="")
    date_entry = tk.Entry(date_frame, textvariable=date_var, width=10)
    date_entry.pack(side=tk.LEFT, padx=5)

    # File management options
    options_frame = ttk.LabelFrame(root, text="Options")
    options_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    recursive_var = tk.BooleanVar(value=True)
    tk.Checkbutton(
        options_frame, text="Scan subfolders",
        variable=recursive_var
    ).pack(side=tk.LEFT, padx=5)

    skip_converted_var = tk.BooleanVar(value=True)
    tk.Checkbutton(
        options_frame, text="Skip converted files",
        variable=skip_converted_var
    ).pack(side=tk.LEFT, padx=5)

    delete_source_var = tk.BooleanVar(value=False)
    tk.Checkbutton(
        options_frame, text="Delete source files",
        variable=delete_source_var
    ).pack(side=tk.LEFT, padx=5)

    # Progress bar
    progress_bar = ttk.Progressbar(
        root, orient="horizontal", length=400, mode="determinate"
    )
    progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    # Status label
    status_label = tk.Label(root, text="Ready", anchor="w")
    status_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

    # Add PDF options frame
    pdf_frame = ttk.LabelFrame(root, text="PDF Options")
    pdf_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    # Orientation
    orientation_var = tk.StringVar(value="P")
    ttk.Radiobutton(
        pdf_frame, text="Portrait", variable=orientation_var,
        value="P"
    ).pack(side=tk.LEFT, padx=5)
    ttk.Radiobutton(
        pdf_frame, text="Landscape", variable=orientation_var,
        value="L"
    ).pack(side=tk.LEFT, padx=5)

    # Page size
    tk.Label(pdf_frame, text="Page Size:").pack(side=tk.LEFT, padx=5)
    size_var = tk.StringVar(value="A4")
    size_combo = ttk.Combobox(
        pdf_frame, textvariable=size_var,
        values=["A4", "Letter", "Legal", "Custom"]
    )
    size_combo.pack(side=tk.LEFT, padx=5)

    # Custom size fields (initially hidden)
    custom_frame = ttk.Frame(pdf_frame)
    width_var = tk.StringVar(value="210")
    height_var = tk.StringVar(value="297")
    tk.Label(custom_frame, text="W:").pack(side=tk.LEFT)
    ttk.Entry(custom_frame, textvariable=width_var, width=5).pack(side=tk.LEFT)
    tk.Label(custom_frame, text="H:").pack(side=tk.LEFT)
    ttk.Entry(custom_frame, textvariable=height_var, width=5).pack(side=tk.LEFT)

    def toggle_custom_size(*args):
        if size_var.get() == "Custom":
            custom_frame.pack(side=tk.LEFT, padx=5)
        else:
            custom_frame.pack_forget()

    size_var.trace('w', toggle_custom_size)

    # Watermark
    watermark_var = tk.StringVar()
    tk.Label(pdf_frame, text="Watermark:").pack(side=tk.LEFT, padx=5)
    ttk.Entry(pdf_frame, textvariable=watermark_var, width=15).pack(side=tk.LEFT, padx=5)

    # Page numbers
    page_numbers_var = tk.BooleanVar(value=False)
    ttk.Checkbutton(
        pdf_frame, text="Page Numbers",
        variable=page_numbers_var
    ).pack(side=tk.LEFT, padx=5)

    # PDF Merging
    merge_var = tk.BooleanVar(value=False)
    merge_files = []

    def add_pdf_to_merge():
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        merge_files.extend(files)
        if merge_files:
            merge_label.config(text=f"{len(merge_files)} PDFs selected")

    merge_frame = ttk.Frame(pdf_frame)
    merge_frame.pack(side=tk.LEFT, padx=5)
    ttk.Checkbutton(
        merge_frame, text="Merge PDFs",
        variable=merge_var
    ).pack(side=tk.LEFT)
    ttk.Button(
        merge_frame, text="Add PDFs",
        command=add_pdf_to_merge
    ).pack(side=tk.LEFT)
    merge_label = tk.Label(merge_frame, text="No PDFs selected")
    merge_label.pack(side=tk.LEFT)

    # Custom fonts
    font_var = tk.StringVar()
    tk.Label(pdf_frame, text="Font:").pack(side=tk.LEFT, padx=5)
    ttk.Entry(pdf_frame, textvariable=font_var, width=15).pack(side=tk.LEFT, padx=5)

    # Background color
    bg_color_var = tk.StringVar()
    tk.Label(pdf_frame, text="Background Color:").pack(side=tk.LEFT, padx=5)
    ttk.Entry(pdf_frame, textvariable=bg_color_var, width=15).pack(side=tk.LEFT, padx=5)

    # Update start_conversion to use new options
    def enhanced_start_conversion():
        try:
            min_date = None
            if date_var.get():
                min_date = datetime.strptime(date_var.get(), "%Y-%m-%d").timestamp()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return

        pdf_options = {
            'orientation': orientation_var.get(),
            'page_size': size_var.get(),
            'custom_size': (int(width_var.get()), int(height_var.get()))
                          if size_var.get() == "Custom" else None,
            'watermark': watermark_var.get() or None,
            'page_numbers': page_numbers_var.get(),
            'merge_files': merge_files if merge_var.get() else None,
            'font': font_var.get() or None,
            'background_color': bg_color_var.get() or None
        }

        start_conversion(
            input_entry, output_entry, quality_entry,
            progress_bar, status_label,
            recursive=recursive_var.get(),
            min_date=min_date,
            skip_converted=skip_converted_var.get(),
            delete_source=delete_source_var.get(),
            pdf_options=pdf_options
        )

    # Update Convert button with shortcut hint
    convert_btn = tk.Button(
        root, text="Convert (Ctrl+Enter)",
        command=enhanced_start_conversion
    )
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

    # Add error log viewer button
    error_log_btn = tk.Button(root, text="View Error Logs", command=show_error_logs)
    error_log_btn.grid(row=7, column=0, columnspan=3, pady=5)

    # Add history viewer button
    def show_history():
        history = load_conversion_history()
        history_window = tk.Toplevel(root)
        history_window.title("Conversion History")

        text = tk.Text(history_window, wrap=tk.WORD)
        text.pack(expand=True, fill='both')

        for file_hash, info in history.items():
            text.insert('end', f"File: {info['path']}\n")
            text.insert('end', f"Converted: {datetime.fromtimestamp(info['timestamp'])}\n")
            text.insert('end', f"Output: {info['output']}\n\n")

    history_btn = tk.Button(root, text="View History", command=show_history)
    history_btn.grid(row=8, column=0, columnspan=3, pady=5)

    return root

if __name__ == "__main__":
    root = create_gui()
    root.mainloop()
