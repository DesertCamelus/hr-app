import tkinter as tk
from tkinter import ttk

PLACEHOLDER_TXT = "חפשי שם עובד"
APP_NAME = "HR App"
RTL_ANCHOR = "e"
COLUMNS_NAMES = ("Department", "Name", "ID")
COLUMNS_TEXTS = {"ID": "מספר זהות", "Name": "שם", "Department": "מחלקה"}


class HRApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("600x400")

        # Search Frame
        self.search_frame = tk.Frame(self.root, bg='#f0f0f0', pady=10)
        self.search_frame.pack(fill='x')

        # Search Entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, font=('Helvetica italic', 14),
                                      width=40, foreground='gray', justify='right')
        self.search_entry.insert(0, PLACEHOLDER_TXT)
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.set_placeholder)
        self.search_entry.bind("<Return>", self.trigger_search)  # Bind the Enter key to trigger search
        self.search_entry.pack(side='right', padx=20)

        # Search Button
        self.search_button = ttk.Button(self.search_frame, text="🔍", command=self.search, width=3)
        self.search_button.pack(side='left', padx=10)

        # Results Frame
        self.results_frame = tk.Frame(self.root)
        self.results_frame.pack(fill='both', expand=True, pady=15)

        # Treeview for Results
        self.results_tree = ttk.Treeview(self.results_frame, columns=COLUMNS_NAMES, show='headings')
        self.results_tree.column("ID", anchor=RTL_ANCHOR)
        self.results_tree.column("Name", anchor=RTL_ANCHOR)
        self.results_tree.column("Department", anchor=RTL_ANCHOR)
        self.results_tree.heading("ID", text="מספר זהות")
        self.results_tree.heading("Name", text="שם")
        self.results_tree.heading("Department", text="מחלקה")
        self.results_tree.pack(fill='both', expand=True)

        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side='right', fill='y')

    def clear_placeholder(self, event):
        if self.search_entry.get() == PLACEHOLDER_TXT:
            self.search_entry.delete(0, tk.END)

    def set_placeholder(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, PLACEHOLDER_TXT)

    def search(self):
        search_query = self.search_var.get()
        if search_query and search_query != PLACEHOLDER_TXT:
            self.display_results(
                [('כהן', 'יוסי', '999999999'), ('ישראלי', 'ישראל', '123456789')])  # Example static data

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
