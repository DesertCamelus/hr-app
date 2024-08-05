import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

PLACEHOLDER_TXT = "חפשי..."
APP_NAME = "HR App"
RTL_ANCHOR = "e"
COLUMNS_NAMES = ("Status", "Salary", "Department", "Name", "ID")
COLUMNS_TEXTS = {"ID": "מספר זהות", "Name": "שם", "Department": "מחלקה", "Salary": "שכר", "Status": "סטטוס"}
SEARCH_FIELDS = ("מחלקה", "שם", "מספר זהות")
TOTAL_FIELDS = 5  # update when a field is added / removed
SEARCH_FIELDS_DELTA = TOTAL_FIELDS - len(SEARCH_FIELDS)


class HRApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("900x800")
        # Sample data
        self.data = [
            ('Active', '5000', 'מכירות', 'יוסי כהן', '999999999'),
            ('Inactive', '6000', 'שירות', 'ישראל ישראלי', '123456789'),
            ('Active', '7000', 'פיתוח', 'דוד לוי', '987654321'),
        ]
        # Define styles
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat")
        style.map("TButton",
                  foreground=[('disabled', 'gray')],
                  background=[('disabled', 'light gray')])

        # Search Frame
        self.search_frame = tk.Frame(self.root, bg='#f0f0f0', pady=10)
        self.search_frame.pack(fill='x')
        # Search Field Combo Box
        self.search_field_var = tk.StringVar(value=SEARCH_FIELDS[2])
        self.search_field_combo = ttk.Combobox(self.search_frame, textvariable=self.search_field_var,
                                               values=SEARCH_FIELDS, state='readonly', width=10, justify='center')
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
        self.search_button.pack(side='right', padx=10)
        # Clear Selections Button with Eraser Symbol
        self.clear_selections_button = ttk.Button(self.search_frame, text="🧹", command=self.clear_selections, width=3,
                                                  cursor="hand2")
        self.clear_selections_button.pack(side='right', padx=10)
        # Add Employee Button
        self.add_employee_button = ttk.Button(self.search_frame, text="הוסיפי עובד/ת / מועמד/ת",
                                              command=self.add_employee,
                                              width=17, cursor="hand2")
        self.add_employee_button.pack(side='right', padx=10)

        # Image Placeholder
        self.image_placeholder = tk.Label(self.root, text="Image Placeholder", bg='gray', width=20, height=10)
        self.image_placeholder.pack(pady=30)

        # Edit Button Frame
        self.edit_button_frame = tk.Frame(self.root, pady=5)
        self.edit_button_frame.pack(fill='x')
        # Edit Employee Button
        self.edit_employee_button = ttk.Button(self.edit_button_frame, text="✎", command=self.edit_employee, width=3,
                                               cursor="hand2", state='disabled')
        self.edit_employee_button.pack(side='left', padx=5)

        # Results Frame
        self.results_frame = tk.Frame(self.root)
        self.results_frame.pack(fill='both', expand=True, pady=15)
        # Treeview for Results
        self.results_tree = ttk.Treeview(self.results_frame, columns=COLUMNS_NAMES, show='headings')
        self.configure_columns()
        self.configure_headings()
        self.results_tree.pack(side='left', fill='both', expand=True)
        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side='right', fill='y')

        # Documents Frame
        self.docs_frame = tk.Frame(self.root)
        # Initially hide the documents frame
        self.docs_frame.pack_forget()

        # Ensure the + and - buttons are correctly packed within the docs_button_frame
        self.docs_button_frame = tk.Frame(self.docs_frame)
        self.docs_button_frame.pack(side='top', anchor='w', padx=5, pady=5)

        self.add_doc_button = ttk.Button(self.docs_button_frame, text="+", command=self.add_document, width=3,
                                         cursor="hand2", state='disabled')
        self.remove_doc_button = ttk.Button(self.docs_button_frame, text="-", command=self.remove_document, width=3,
                                            cursor="hand2", state='disabled')

        self.add_doc_button.pack(side='left', padx=5)
        self.remove_doc_button.pack(side='left', padx=5)

        # Treeview for Documents
        self.docs_tree = ttk.Treeview(self.docs_frame, columns=("DocName", "DocType"), show='headings')
        self.docs_tree.heading("DocName", text="Document Name")
        self.docs_tree.heading("DocType", text="Document Type")
        self.docs_tree.pack(fill='both', expand=True)

        # Bind row selection
        self.results_tree.bind("<ButtonRelease-1>", self.on_row_select)
        # Bind double-click on documents
        self.docs_tree.bind("<Double-1>", self.on_doc_double_click)
        # Bind document selection
        self.docs_tree.bind("<<TreeviewSelect>>", self.on_doc_select)

        # Display all employees on startup
        self.display_results(self.data)

    def configure_columns(self):
        column_widths = {
            "Status": 80,
            "Salary": 80,
            "Department": 100,
            "Name": 120,
            "ID": 100
        }
        for name in COLUMNS_NAMES:
            self.results_tree.column(name, anchor=RTL_ANCHOR, width=column_widths.get(name, 100))

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
        search_field = self.search_field_var.get()
        if search_query and search_query != PLACEHOLDER_TXT:
            if search_field in SEARCH_FIELDS:
                search_field_index = SEARCH_FIELDS.index(search_field) + SEARCH_FIELDS_DELTA
                filtered_data = [row for row in self.data if search_query.lower() in row[search_field_index].lower()]
                if filtered_data:
                    self.display_results(filtered_data)
                else:
                    messagebox.showinfo("תוצאה", "לא נמצאו רשומות")
            else:
                self.display_results(self.data)
        else:
            self.display_results(self.data)

    def display_results(self, results):
        for row in self.results_tree.get_children():
            self.results_tree.delete(row)
        if not results:
            messagebox.showinfo("תוצאה", "לא נמצאו רשומות")
        for result in results:
            self.results_tree.insert('', 'end', values=result)

    def trigger_search(self, event):
        self.search()

    def on_row_select(self, event):
        selected_item = self.results_tree.selection()
        if selected_item:
            self.selected_data = self.results_tree.item(selected_item, "values")
            # Clear previous documents
            for row in self.docs_tree.get_children():
                self.docs_tree.delete(row)
            # Add sample documents for the selected person
            sample_docs = [("Document 1", "Type A"), ("Document 2", "Type B")]
            for doc in sample_docs:
                self.docs_tree.insert('', 'end', values=doc)
            # Enable add document button
            self.add_doc_button.config(state='normal')
            # Enable edit employee button
            self.edit_employee_button.config(state='normal')
            # Show documents frame
            self.docs_frame.pack(fill='both', expand=True, pady=15)
        else:
            # Disable edit employee button if no employee is selected
            self.edit_employee_button.config(state='disabled')
            # Hide documents frame
            self.docs_frame.pack_forget()

    def on_doc_double_click(self, event):
        selected_item = self.docs_tree.selection()
        if selected_item:
            doc_name = self.docs_tree.item(selected_item, "values")[0]
            messagebox.showinfo("Document", f"Opening document: {doc_name}")

    def on_doc_select(self, event):
        selected_item = self.docs_tree.selection()
        if selected_item:
            self.remove_doc_button.config(state='normal')
        else:
            self.remove_doc_button.config(state='disabled')

    # Change the employee adding prompt to a single form with all fields
    def add_employee(self):
        def save_new_employee():
            new_employee = {
                'ID': id_entry.get(),
                'Name': name_entry.get(),
                'Department': dept_entry.get(),
                'Salary': salary_entry.get(),
                'Status': status_entry.get()
            }
            if not new_employee['ID'] or not new_employee['Name']:
                messagebox.showerror("Error", "ID and Name are mandatory")
                return
            self.data.append(
                (new_employee['Status'], new_employee['Salary'], new_employee['Department'], new_employee['Name'],
                 new_employee['ID'])
            )
            self.display_results(self.data)
            add_window.destroy()

        add_window = tk.Toplevel(self.root)
        add_window.title("Add Employee")
        add_window.geometry("300x400")

        tk.Label(add_window, text="ID:").pack(pady=5)
        id_entry = tk.Entry(add_window)
        id_entry.pack(pady=5)

        tk.Label(add_window, text="Name:").pack(pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.pack(pady=5)

        tk.Label(add_window, text="Department:").pack(pady=5)
        dept_entry = tk.Entry(add_window)
        dept_entry.pack(pady=5)

        tk.Label(add_window, text="Salary:").pack(pady=5)
        salary_entry = tk.Entry(add_window)
        salary_entry.pack(pady=5)

        tk.Label(add_window, text="Status:").pack(pady=5)
        status_entry = tk.Entry(add_window)
        status_entry.pack(pady=5)

        save_button = tk.Button(add_window, text="Save", command=save_new_employee, bg="#00FF00")
        save_button.pack(pady=10)

    def edit_employee(self):
        if not hasattr(self, 'selected_data'):
            messagebox.showerror("Error", "No employee selected")
            return

        def save_changes():
            selected_field = field_var.get()
            new_value = new_value_entry.get()
            if not new_value:
                messagebox.showerror("Error", "Value cannot be empty")
                return
            index = COLUMNS_NAMES.index(selected_field)
            self.selected_data = list(self.selected_data)
            self.selected_data[index] = new_value
            for i, employee in enumerate(self.data):
                if employee[3] == self.selected_data[3]:  # Match by ID
                    self.data[i] = tuple(self.selected_data)
                    break
            self.display_results(self.data)
            edit_window.destroy()

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Employee")
        edit_window.geometry("300x200")

        field_var = tk.StringVar(value=COLUMNS_NAMES[0])
        for field in COLUMNS_NAMES:
            tk.Radiobutton(edit_window, text=field, variable=field_var, value=field).pack(anchor='w')

        tk.Label(edit_window, text="New Value:").pack(pady=10)
        new_value_entry = tk.Entry(edit_window)
        new_value_entry.pack(pady=5)

        tk.Button(edit_window, text="Save", command=save_changes).pack(pady=10)

    def add_document(self):
        # Placeholder for adding a document
        messagebox.showinfo("Add Document", "This is a placeholder for adding a document.")

    def remove_document(self):
        selected_item = self.docs_tree.selection()
        if selected_item:
            doc_name = self.docs_tree.item(selected_item, "values")[0]
            confirm = messagebox.askyesno("Confirm Deletion",
                                          f"Are you sure you want to delete the document: {doc_name}?")
            if confirm:
                self.docs_tree.delete(selected_item)
                self.remove_doc_button.config(state='disabled')

    # Implement clear_selections method
    def clear_selections(self):
        # Clear selections in results_tree and docs_tree
        self.results_tree.selection_remove(self.results_tree.selection())
        self.docs_tree.selection_remove(self.docs_tree.selection())
        # Clear all items in docs_tree
        for row in self.docs_tree.get_children():
            self.docs_tree.delete(row)
        # Disable buttons that depend on selections
        self.edit_employee_button.config(state='disabled')
        self.add_doc_button.config(state='disabled')
        self.remove_doc_button.config(state='disabled')
        # Reset search input to placeholder text
        self.search_var.set("")
        self.set_placeholder(None)
        # Display all data
        self.display_results(self.data)


if __name__ == "__main__":
    root = tk.Tk()
    app = HRApp(root)
    root.mainloop()
