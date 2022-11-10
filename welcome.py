from gui import *
from company import CompanyPage
from invoice import InvoicePage
from analyze import AnalyzePage
from tkinter import *


class HomePage(MainWindow):
    def __init__(self, name, dimensions):
        super().__init__(name, dimensions)

        # Create the starting label and buttons
        self.welcome = Label(self, text="Invoice Organizer", font=("Helvetica", 36))
        self.welcome.place(relx=.5, rely=.1, anchor="center")

        self.company_button = Button(self, text="Companies", font=("Helvetica", 18), command=self.company_page)
        self.company_button.place(relx=.3, rely=.5, anchor="center")

        self.invoice_button = Button(self, text="Invoice", font=("Helvetica", 18), command=self.invoice_page)
        self.invoice_button.place(relx=.5, rely=.5, anchor="center")

        self.analyze_button = Button(self, text="Analyze", font=("Helvetica", 18), command=self.analyze_page)
        self.analyze_button.place(relx=.7, rely=.5, anchor="center")


    def company_page(self):
        company = CompanyPage(self, "Company", "1000x1000")

    def analyze_page(self):
        analyze = AnalyzePage(self, "Analyze", "1000x1000")

    def invoice_page(self):
        invoice = InvoicePage(self, "Invoice", "1500x1000")
