import tkinter as tk
from tkinter import messagebox

def preview_issues(issue_list):
    def show_issues():
        issue_window = tk.Toplevel()
        issue_window.title("Conversion Issues")
        
        text_widget = tk.Text(issue_window, wrap='word', height=20, width=50)
        text_widget.pack(expand=True, fill='both')
        
        for issue in issue_list:
            text_widget.insert('end', f"{issue}\n")
        
        text_widget.config(state='disabled')
        
        close_button = tk.Button(issue_window, text="Close", command=issue_window.destroy)
        close_button.pack(pady=10)
    
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    show_issues()
    root.mainloop()
