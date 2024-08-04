import tkinter as tk
from tkinter import ttk

PLACEHOLDER_TXT = "חפשי..."
APP_NAME = "HR App"
RTL_ANCHOR = "e"
COLUMNS_NAMES = ("Department", "Name", "ID")
COLUMNS_TEXTS = {"ID": "מספר זהות", "Name": "שם", "Department": "מחלקה"}
SEARCH_FIELDS = ("מחלקה", "שם", "מספר זהות")


class HRApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("600x400")
        # Sample data
        self.data = [
            ('מכירות', 'יוסי כהן', '999999999'),
            ('שירות', 'ישראל ישראלי', '123456789'),
            ('פיתוח', 'דוד לוי', '987654321'),
            ('משאבים', 'שרה כהן', '456123789')
        ]
        # Search Frame
        self.search_frame = tk.Frame(self.root, bg='#f0f0f0', pady=10)
        self.search_frame.pack(fill='x')
        # Search Field Combo Box
        self.search_field_var = tk.StringVar(value=SEARCH_FIELDS[2])
        self.search_field_combo = ttk.Combobox(self.search_frame, textvariable=self.search_field_var,
                                               values=SEARCH_FIELDS, state='readonly', width=10)
        self.search_field_combo.pack(side='right', padx=5)
        # Search Entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, font=('Helvetica italic', 14),
                                      width=30, foreground='gray', justify='right')
        self.search_entry.insert(0, PLACEHOLDER_TXT)
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.set_placeholder)
        self.search_entry.bind("<Return>", self.trigger_search)  # Bind the Enter key to trigger search
        self.search_entry.pack(side='right', padx=20)
        # Search Button
        self.search_button = ttk.Button(self.search_frame, text="🔍", command=self.search, width=3, cursor="hand2")
        self.search_button.pack(side='left', padx=10)
        # Results Frame
        self.results_frame = tk.Frame(self.root)
        self.results_frame.pack(fill='both', expand=True, pady=15)
        # Treeview for Results
        self.results_tree = ttk.Treeview(self.results_frame, columns=COLUMNS_NAMES, show='headings')
        self.configure_columns()
        self.configure_headings()
        self.results_tree.pack(fill='both', expand=True)
        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side='right', fill='y')

    def configure_columns(self):
        for name in COLUMNS_NAMES:
            self.results_tree.column(name, anchor=RTL_ANCHOR)

    def configure_headings(self):
        for text in COLUMNS_TEXTS:
            self.results_tree.heading(text, text=COLUMNS_TEXTS[text])

    def clear_placeholder(self, event):
        if self.search_entry.get() == PLACEHOLDER_TXT:
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(foreground='black')

    def set_placeholder(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, PLACEHOLDER_TXT)
            self.search_entry.config(foreground='gray')

    def search(self):
        search_query = self.search_var.get().strip()
        search_field_index = SEARCH_FIELDS.index(self.search_field_var.get())
        if search_query and search_query != PLACEHOLDER_TXT:
            filtered_data = [row for row in self.data if search_query.lower() in row[search_field_index].lower()]
            self.display_results(filtered_data)

    def display_results(self, results):
        for row in self.results_tree.get_children():
            self.results_tree.delete(row)
        for result in results:
            self.results_tree.insert('', 'end', values=result)

    def trigger_search(self, event):
        self.search()


if __name__ == "__main__":
    root = tk.Tk()
    app = HRApp(root)
    root.mainloop()
