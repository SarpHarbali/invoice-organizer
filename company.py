from gui import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class CompanyPage(Others):
    def __init__(self, parent, name, dimensions):
        super().__init__(parent, name, dimensions)

        self.tree_frame = Frame(self)
        self.tree_frame.grid(row=0, column=0, pady=10)

        # Create scrollbar for treeview
        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        # Create treeview
        self.tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, selectmode="extended")
        self.tree.pack()

        # Configure scrollbar
        self.tree_scroll.config(command=self.tree.yview)

        # Define the columns of the treeview
        self.tree['columns'] = (
            "Company ID", "Company Name", "Company Address", "VAT Number"
        )

        # Place the columns
        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column("Company ID", anchor=CENTER, width=100)
        self.tree.column("Company Name", anchor=CENTER, width=200)
        self.tree.column("Company Address", anchor=CENTER, width=300)
        self.tree.column("VAT Number", anchor=CENTER, width=140)

        # Create headings for columns
        self.tree.heading("#0", text="", anchor=W)
        self.tree.heading("Company ID", text="Company ID", anchor=CENTER)
        self.tree.heading("Company Name", text="Company Name", anchor=CENTER)
        self.tree.heading("Company Address", text="Company Address", anchor=CENTER)
        self.tree.heading("VAT Number", text="VAT Number", anchor=CENTER)

        self.data_frame = LabelFrame(self, text="Company")
        self.data_frame.grid(row=1, column=0)

        self.name_label = Label(self.data_frame, text="Company Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = Entry(self.data_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.address_label = Label(self.data_frame, text="Company Address:")
        self.address_label.grid(row=0, column=2, padx=10, pady=10)
        self.address_entry = Entry(self.data_frame)
        self.address_entry.grid(row=0, column=3, padx=10, pady=10)

        self.vat_number_label = Label(self.data_frame, text="VAT Number:")
        self.vat_number_label.grid(row=0, column=4, padx=5, pady=10)
        self.vat_number_entry = Entry(self.data_frame)
        self.vat_number_entry.grid(row=0, column=5, padx=5, pady=10)

        self.button_frame = LabelFrame(self, text="Commands")
        self.button_frame.grid(row=2, column=0, pady=10)

        self.add_company_button = Button(self.button_frame, text="Add Company", command=self.add)
        self.add_company_button.grid(row=0, column=0, padx=10, pady=10)

        self.update_company_button = Button(self.button_frame, text="Update Company Info", command=self.update)
        self.update_company_button.grid(row=0, column=1, padx=20, pady=10)

        self.remove_all_companies_button = Button(self.button_frame, text="Remove All Companies", command=self.remove_all)
        self.remove_all_companies_button.grid(row=0, column=2, padx=20, pady=10)

        self.remove_many_companies_button = Button(self.button_frame, text="Remove Selected Companies", command=self.remove_selected)
        self.remove_many_companies_button.grid(row=0, column=3, padx=20, pady=10)

        self.go_back_button = Button(self.button_frame, text="Go Back", command=self.go_back)
        self.go_back_button.grid(row=0, column=4, padx=10, pady=10)

        self.clear_entries_button = Button(self.data_frame, text="Clear Entries", command=self.clear_entries)
        self.clear_entries_button.grid(row=0, column=6, padx=10, pady=10)

        self.tree.bind("<ButtonRelease-1>", self.select)

        self.query()

    def go_back(self):
        self.destroy()

    def query(self):

        # Clear the treeview table
        for record in self.tree.get_children():
            self.tree.delete(record)

        # Create the database or connect to the existing database
        conn = sqlite3.connect('invoice_db.db')

        # Create a cursor instance
        cursor = conn.cursor()

        # Fetch the data
        cursor.execute("SELECT * FROM companies")
        records = cursor.fetchall()

        for record in records:
            self.tree.insert(parent='', index='end', text='', values=(record[0], record[1], record[2], record[3]))

        # Commit changes
        conn.commit()

        # Close the connection
        conn.close()

    def clear_entries(self):
        self.name_entry.delete(0, END)
        self.address_entry.delete(0, END)
        self.vat_number_entry.delete(0, END)

    def select(self, e):

        self.clear_entries()

        selected = self.tree.focus()

        values = self.tree.item(selected, 'values')

        # Output to entry boxes
        self.name_entry.insert(0, values[1])
        self.address_entry.insert(0, values[2])
        self.vat_number_entry.insert(0, values[3])

    def add(self):

        # Create the database or connect to the existing database
        conn = sqlite3.connect('invoice_db.db')

        # Create a cursor instance
        cursor = conn.cursor()

        cursor.execute("INSERT INTO companies (company_name, company_address, vat_number) VALUES (?,?,?)",
                       (self.name_entry.get(), self.address_entry.get(), self.vat_number_entry.get()))
        # Commit changes
        conn.commit()

        # Close the connection
        conn.close()

        self.clear_entries()

        # Clear The treeview table
        self.tree.delete(*self.tree.get_children())

        # Pull data from database
        self.query()

    def update(self):
        # Create the database or connect to the existing database
        conn = sqlite3.connect('invoice_db.db')

        # Create a cursor instance
        cursor = conn.cursor()

        selected = self.tree.focus()

        id = self.tree.item(selected).get('values')[0]

        cursor.execute("""UPDATE companies SET
                                    company_name = ?,
                                    company_address = ?,
                                    vat_number = ?
                                    WHERE company_id = ?""", (
            self.name_entry.get(),
            self.address_entry.get(),
            self.vat_number_entry.get(),
            id))

        # Commit changes
        conn.commit()

        cursor.execute("SELECT * FROM companies")

        x = self.tree.index(selected)

        records = cursor.fetchall()

        self.tree.item(selected, text="", values=(
            records[x][0], records[x][1], records[x][2], records[x][3]))

        # Commit changes
        conn.commit()

        # Close the connection
        conn.close()

        self.clear_entries()

        self.query()

    def remove_selected(self):
        # Ask a yes/no question
        response = messagebox.askyesno(message="Are you sure you want to delete the selected companies?")
        # Delete the invoice from the treeview
        if response == 1:

            selection = self.tree.selection()

            self.clear_entries()

            # Create a list to store ids of invoices to be removed
            removed = []

            # Add selections to the list
            for x in selection:
                removed.append(self.tree.item(x, 'values')[0])

            for x in selection:
                self.tree.delete(x)

            conn = sqlite3.connect('invoice_db.db')

            cursor = conn.cursor()

            cursor.executemany("DELETE FROM companies WHERE company_id = ?", [(x,) for x in removed])

            conn.commit()

            conn.close()

    def remove_all(self):
        # Ask a yes/no question
        response = messagebox.askyesno(message="Are you sure you want to delete all companies?")
        # Delete the invoice from the treeview
        if response == 1:
            for x in self.tree.get_children():
                self.tree.delete(x)

            self.clear_entries()

            conn = sqlite3.connect('invoice_db.db')

            cursor = conn.cursor()

            cursor.execute("DELETE FROM companies")

            conn.commit()

            conn.close()