from gui import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import *
import sqlite3


class InvoicePage(Others):

    def __init__(self, parent, name, dimensions):
        super().__init__(parent, name, dimensions)

        # Create treeview frame
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
            "Invoice ID", "Invoice Type", "Invoice Number", "Company ID", "Company Name", "Company Address",
            "VAT Number", "Total",
            "Currency", "Invoice Date")

        # Place the columns
        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column("Invoice ID", anchor=CENTER, width=100)
        self.tree.column("Invoice Type", anchor=CENTER, width=100)
        self.tree.column("Invoice Number", anchor=CENTER, width=100)
        self.tree.column("Company ID", anchor=CENTER, width=100)
        self.tree.column("Company Name", anchor=CENTER, width=200)
        self.tree.column("Company Address", anchor=CENTER, width=300)
        self.tree.column("VAT Number", anchor=CENTER, width=100)
        self.tree.column("Total", anchor=CENTER, width=100)
        self.tree.column("Currency", anchor=CENTER, width=50)
        self.tree.column("Invoice Date", anchor=CENTER, width=100)

        # Create headings for columns
        self.tree.heading("#0", text="", anchor=W)
        self.tree.heading("Invoice ID", text="Invoice ID", anchor=CENTER)
        self.tree.heading("Invoice Type", text="Invoice Type", anchor=CENTER)
        self.tree.heading("Invoice Number", text="Invoice Number", anchor=CENTER)
        self.tree.heading("Company ID", text="Company ID", anchor=CENTER)
        self.tree.heading("Company Name", text="Company Name", anchor=CENTER)
        self.tree.heading("Company Address", text="Company Address", anchor=CENTER)
        self.tree.heading("VAT Number", text="VAT Number", anchor=CENTER)
        self.tree.heading("Total", text="Total", anchor=CENTER)
        self.tree.heading("Currency", text="Currency", anchor=CENTER)
        self.tree.heading("Invoice Date", text="Invoice Date", anchor=CENTER)

        self.sort_frame = LabelFrame(self, text="Sort")
        self.sort_frame.grid(row=0, column=1)

        self.asc_total_button = Button(self.sort_frame, text="Sort by Ascending Total",
                                       command=lambda: self.sorting(True, 7))
        self.asc_total_button.grid(row=0, column=0)

        self.des_total_button = Button(self.sort_frame, text="Sort by Descending Total",
                                       command=lambda: self.sorting(False, 7))
        self.des_total_button.grid(row=1, column=0)

        self.asc_date_button = Button(self.sort_frame, text="Sort by Ascending Date",
                                      command=lambda: self.sorting(True, 9))
        self.asc_date_button.grid(row=2, column=0)

        self.des_date_button = Button(self.sort_frame, text="Sort by Descending Date",
                                      command=lambda: self.sorting(False, 9))
        self.des_date_button.grid(row=3, column=0)

        # Create the data frame to record data
        self.data_frame = LabelFrame(self, text="Record")
        self.data_frame.grid(row=1, column=0)

        self.invoice_type_label = Label(self.data_frame, text="Invoice Type:")
        self.invoice_type_label.grid(row=0, column=0, pady=10)
        self.invoice_type_entry = Entry(self.data_frame)
        self.invoice_type_entry.grid(row=0, column=1, pady=10)

        self.invoice_number_label = Label(self.data_frame, text="Invoice Number:")
        self.invoice_number_label.grid(row=0, column=2, pady=10)
        self.invoice_number_entry = Entry(self.data_frame)
        self.invoice_number_entry.grid(row=0, column=3, padx=5, pady=10)

        self.company_id_label = Label(self.data_frame, text="Company ID:")
        self.company_id_label.grid(row=0, column=4, pady=10)
        self.company_id_entry = Entry(self.data_frame)
        self.company_id_entry.grid(row=0, column=5, pady=10)

        self.total_label = Label(self.data_frame, text="Total:")
        self.total_label.grid(row=0, column=6, pady=10)
        self.total_entry = Entry(self.data_frame)
        self.total_entry.grid(row=0, column=7, pady=10)

        self.currency_label = Label(self.data_frame, text="Currency:")
        self.currency_label.grid(row=0, column=8, pady=10)
        self.currency_entry = Entry(self.data_frame)
        self.currency_entry.grid(row=0, column=9, pady=10)

        self.invoice_date_label = Label(self.data_frame, text="Invoice Date:")
        self.invoice_date_label.grid(row=0, column=10, pady=10)
        self.invoice_date_entry = DateEntry(self.data_frame, date_pattern='y-mm-dd')
        self.invoice_date_entry.grid(row=0, column=11, pady=10)

        # Create buttons
        self.button_frame = LabelFrame(self, text="Commands")
        self.button_frame.grid(row=2, column=0, padx=20)

        self.add_button = Button(self.button_frame, text="Add Invoice", command=self.add)
        self.add_button.grid(row=0, column=0, padx=20, pady=10)

        self.update_button = Button(self.button_frame, text="Update Invoice", command=self.update)
        self.update_button.grid(row=0, column=1, padx=20, pady=10)

        self.remove_all_button = Button(self.button_frame, text="Remove All Invoices", command=self.remove_all)
        self.remove_all_button.grid(row=0, column=2, padx=20, pady=10)

        self.remove_many_button = Button(self.button_frame, text="Remove Selected", command=self.remove_selected)
        self.remove_many_button.grid(row=0, column=3, padx=20, pady=10)

        self.go_back_button = Button(self.button_frame, text="Go Back", command=self.go_back)
        self.go_back_button.grid(row=0, column=4, padx=20, pady=20)

        self.clear_entries_button = Button(self.data_frame, text="Clear Entry Boxes", command=self.clear_entries)
        self.clear_entries_button.grid(row=1, column=13, padx=5, pady=10)

        self.tree.bind("<ButtonRelease-1>", self.select)

        self.style = ttk.Style()

        self.style.map("Treeview",
                       foreground=self.fixed_map("foreground"),
                       background=self.fixed_map("background"))

        self.query()

    def sort(self, array, index):
        if len(array) > 1:

            middle = len(array) // 2

            L = array[:middle]  # left part of the array

            R = array[middle:]  # right part of the array

            self.sort(L, index)

            self.sort(R, index)

            i = j = k = 0

            while i < len(L) and j < len(R):
                if L[i][index] < R[j][index]:
                    array[k] = L[i]
                    i += 1
                else:
                    array[k] = R[j]
                    j += 1
                k += 1

            while i < len(L):
                array[k] = L[i]
                i += 1
                k += 1

            while j < len(R):
                array[k] = R[j]
                j += 1
                k += 1

    def sorting(self, ascending, index):
        # Clear the treeview table
        for record in self.tree.get_children():
            self.tree.delete(record)

        # Create the database or connect to the existing database
        conn = sqlite3.connect('invoice_db.db')

        # Create a cursor instance
        cursor = conn.cursor()

        # Fetch the data
        cursor.execute("""SELECT invoices.invoices_id, invoices.invoice_type, invoices.invoice_number, 
                                companies.company_id, companies.company_name, companies.company_address, companies.vat_number,
                                invoices.total, invoices.currency, invoices.date
                                FROM invoices JOIN companies ON companies.company_id = invoices.company_id""")

        records = cursor.fetchall()
        self.sort(records, index)
        if not ascending:
            records.reverse()
        count = 1
        for record in records:
            if record[1] == 'debit':
                self.tree.insert(parent='', index='end', text='', iid=count,
                                 values=(
                                     record[0], record[1], record[2], record[3], record[4], record[5], record[6],
                                     record[7], record[8], record[9]), tags=('debit'))
            elif record[1] == 'credit':
                self.tree.insert(parent='', index='end', text='', iid=count,
                                 values=(
                                     record[0], record[1], record[2], record[3], record[4], record[5], record[6],
                                     record[7], record[8], record[9]), tags=('credit'))
            count += 1

        self.tree.tag_configure('debit', background='#ff6347', foreground='black')
        self.tree.tag_configure('credit', background='#90EE90', foreground='black')

        # Commit changes
        conn.commit()

        # Close the connection
        conn.close()

    def fixed_map(self, option):
        return [x for x in self.style.map("Treeview", query_opt=option)
                if x[:2] != ("!disabled", "!selected")]

    def query(self):

        # Clear the treeview table
        for record in self.tree.get_children():
            self.tree.delete(record)

        # Create the database or connect to the existing database
        conn = sqlite3.connect('invoice_db.db')

        # Create a cursor instance
        cursor = conn.cursor()

        # Fetch the data
        cursor.execute("""SELECT invoices.invoices_id, invoices.invoice_type, invoices.invoice_number, 
                        companies.company_id, companies.company_name, companies.company_address, companies.vat_number,
                        invoices.total, invoices.currency, invoices.date
                        FROM invoices JOIN companies ON companies.company_id = invoices.company_id""")

        records = cursor.fetchall()
        count = 1
        for record in records:
            if record[1] == 'debit':
                self.tree.insert(parent='', index='end', text='', iid=count,
                                 values=(
                                     record[0], record[1], record[2], record[3], record[4], record[5], record[6],
                                     record[7],
                                     record[8],
                                     record[9]), tags=('debit'))
            elif record[1] == 'credit':
                self.tree.insert(parent='', index='end', text='', iid=count,
                                 values=(
                                     record[0], record[1], record[2], record[3], record[4], record[5], record[6],
                                     record[7],
                                     record[8],
                                     record[9]), tags=('credit'))
            count += 1

        self.tree.tag_configure('debit', background='#ff6347', foreground='black')
        self.tree.tag_configure('credit', background='#90EE90', foreground='black')

        # Commit changes
        conn.commit()

        # Close the connection
        conn.close()

    def clear_entries(self):
        self.invoice_type_entry.delete(0, END)
        self.invoice_number_entry.delete(0, END)
        self.company_id_entry.delete(0, END)
        self.total_entry.delete(0, END)
        self.currency_entry.delete(0, END)
        self.invoice_date_entry.delete(0, END)

    def select(self, e):

        self.clear_entries()

        selected = self.tree.focus()

        values = self.tree.item(selected, 'values')

        try:
            self.invoice_type_entry.insert(0, values[1])
            self.invoice_number_entry.insert(0, values[2])
            self.company_id_entry.insert(0, values[3])
            self.total_entry.insert(0, values[7])
            self.currency_entry.insert(0, values[8])
            self.invoice_date_entry.insert(0, values[9])
        except:
            pass

    def update(self):

        conn = sqlite3.connect('invoice_db.db')

        # Create a cursor instance
        cursor = conn.cursor()

        selected = self.tree.focus()

        id = self.tree.item(selected).get('values')[0]

        cursor.execute("""UPDATE invoices SET
                invoice_type = ?,
              invoice_number = ?,
              total = ?,
              currency = ?,
              date = ?,
              company_id = ?
              WHERE invoices_id = ?""", (
            self.invoice_type_entry.get(),
            self.invoice_number_entry.get(),
            self.total_entry.get(),
            self.currency_entry.get(),
            self.invoice_date_entry.get(),
            self.company_id_entry.get(),
            id))

        conn.commit()

        cursor.execute("""SELECT invoices.invoices_id, invoices.invoice_type, invoices.invoice_number, companies.company_id, 
                        companies.company_name, companies.company_address, companies.vat_number, invoices.total, invoices.currency, 
                        invoices.date FROM invoices JOIN companies ON companies.company_id = invoices.company_id""")

        x = self.tree.index(selected)
        records = cursor.fetchall()

        self.tree.item(selected, text="", values=(
            records[x][0], records[x][2], records[x][3], records[x][4], records[x][5],
            records[x][6], records[x][7], records[x][8], records[x][9]))

        conn.commit()

        conn.close()

        self.clear_entries()

        self.query()

    def remove_selected(self):
        # Ask a yes/no question
        response = messagebox.askyesno(message="Are you sure you want to delete the selected invoices?")
        # Delete the invoice from the treeview
        if response == 1:

            selection = self.tree.selection()

            # Create a list to store ids of invoices to be removed
            removed = []

            # Add selections to the list
            for x in selection:
                removed.append(self.tree.item(x, 'values')[0])

            for x in selection:
                self.tree.delete(x)

            conn = sqlite3.connect('invoice_db.db')

            cursor = conn.cursor()

            cursor.executemany("DELETE FROM invoices WHERE invoices_id = ?", [(x,) for x in removed])

            conn.commit()

            conn.close()

            self.clear_entries()

        # Check if the user really wants to delete the invoices

    def remove_all(self):
        # Ask a yes/no question
        response = messagebox.askyesno(message="Are you sure you want to delete all invoices?")
        # Delete the invoice from the treeview
        if response == 1:
            for x in self.tree.get_children():
                self.tree.delete(x)

            self.clear_entries()

            conn = sqlite3.connect('invoice_db.db')

            cursor = conn.cursor()

            cursor.execute("DELETE FROM invoices")

            conn.commit()

            conn.close()

    def add(self):
        # Create the database or connect to the existing database
        conn = sqlite3.connect('invoice_db.db')

        # Create a cursor instance
        cursor = conn.cursor()

        # Add new invoice
        cursor.execute(
            "INSERT INTO invoices (invoice_type, invoice_number, total, currency, date, company_id) VALUES (?, ?, ?, ?, ?, ?)",
            (self.invoice_type_entry.get(), self.invoice_number_entry.get(), self.total_entry.get(),
             self.currency_entry.get(),
             self.invoice_date_entry.get(), self.company_id_entry.get()))

        # Commit changes
        conn.commit()

        # Close the connection
        conn.close()

        # Clear the entry boxes
        self.clear_entries()

        # Clear The treeview table
        self.tree.delete(*self.tree.get_children())

        # Pull data from database
        self.query()

    def go_back(self):
        self.destroy()
