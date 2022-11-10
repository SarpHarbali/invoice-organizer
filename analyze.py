from tkinter import *
from datetime import date
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import *
import sqlite3
from PIL import ImageTk, Image
import plotly.graph_objects as go
import pandas as pd
import requests
from gui import *
import plotly.io as pio
import os
pio.kaleido.scope.chromium_args = tuple([arg for arg in pio.kaleido.scope.chromium_args if arg != "--disable-dev-shm-usage"])

class AnalyzePage(Others):
    def __init__(self, parent, name, dimensions):
        super().__init__(parent, name, dimensions)

        conn = sqlite3.connect('invoice_db.db')

        cursor = conn.cursor()

        self.frame1 = LabelFrame(self, text="Analyze Data")
        self.frame1.grid(row=0, column=0, padx=10, pady=5)

        self.frame2 = LabelFrame(self, text="Graph")
        self.frame2.grid(row=1, column=0, padx=10, pady=5)

        self.choices = ["", "", "", "", ""]

        self.select_type = ttk.Combobox(self.frame1, value=("Income", "Expense", "Net Profit"))
        self.select_type.current(0)
        self.select_type.bind("<<ComboboxSelected>>", self.click_type)
        self.select_type.grid(row=0, column=0)

        self.company_list = ["All Companies"]
        cursor.execute("SELECT company_name FROM companies"),
        self.companies = cursor.fetchall()
        for x in self.companies: self.company_list.append(x[0])

        self.select_company = ttk.Combobox(self.frame1, value=self.company_list)
        self.select_company.current(0)
        self.select_company.bind("<<ComboboxSelected>>", self.click_company)
        self.select_company.grid(row=0, column=1)

        self.start_date_calendar = DateEntry(self.frame1, date_pattern='y-mm-dd')
        self.start_date_calendar.grid(row=0, column=2, padx=10, pady=10)
        self.start_date_calendar.bind("<<DateEntrySelected>>", self.start_date)

        self.end_date_calendar = DateEntry(self.frame1, date_pattern='y-mm-dd')
        self.end_date_calendar.grid(row=0, column=3, padx=10, pady=10)
        self.end_date_calendar.bind("<<DateEntrySelected>>", self.end_date)

        self.currency_entry = Entry(self.frame1)
        self.currency_entry.grid(row=0, column=4, padx=10, pady=10)

        self.show_results_button = Button(self.frame1, text="Show Results", command=self.show_results)
        self.show_results_button.grid(row=1, column=1, padx=10, pady=10)

        self.go_back_button = Button(self.frame1, text="Go Back", command=self.go_back)
        self.go_back_button.grid(row=1, column=2, padx=10, pady=10)


        self.monthly_graph_button = Button(self.frame2, text="Create Monthly Graph", command=lambda: self.create_graph("monthly"))
        self.monthly_graph_button.grid(row=0, column=0, padx=10, pady=10)

        self.yearly_graph_button = Button(self.frame2, text="Create Yearly Graph", command=lambda: self.create_graph("yearly"))
        self.yearly_graph_button.grid(row=0, column=1, padx=10, pady=10)


        conn.commit()
        conn.close()

    def click_type(self,event):
        self.choices[0] = self.select_type.get()

    def click_company(self,event):
        self.choices[1] = self.select_company.get()

    def start_date(self,e):
        self.choices[2] = self.start_date_calendar.get_date()

    def end_date(self,e):
        self.choices[3] = self.end_date_calendar.get_date()


    def show_results(self):

        # Create the database or connect to the existing database
        conn = sqlite3.connect('invoice_db.db')

        # Create a cursor instance
        cursor = conn.cursor()

        self.sum_label = Label(self.frame1, text="")
        self.sum_label.grid(row=2, column=1, padx=10, pady=10)
        self.sum_label.grid_forget()

        if self.select_company.get() == "All Companies":
            cursor.execute("""SELECT total, currency FROM invoices 
                            WHERE invoices.invoice_type = ? AND invoices.date BETWEEN ? AND ?""",
                           ("debit", self.choices[2], self.choices[3]))
            debit = cursor.fetchall()

            cursor.execute("""SELECT total, currency FROM invoices
                            WHERE invoices.invoice_type = ? AND invoices.date BETWEEN ? AND ?""",
                           ("credit", self.choices[2], self.choices[3]))
            credit = cursor.fetchall()

        else:
            cursor.execute("""SELECT invoices.total, invoices.currency FROM invoices JOIN companies ON companies.company_id = invoices.company_id 
                            WHERE invoices.invoice_type = ? AND companies.company_name = ? 
                            AND invoices.date BETWEEN ? AND ?""",
                           ("debit", self.choices[1], self.choices[2], self.choices[3]))
            debit = cursor.fetchall()

            cursor.execute("""SELECT invoices.total, invoices.currency FROM invoices JOIN companies ON companies.company_id = invoices.company_id
                            WHERE invoices.invoice_type = ? AND companies.company_name = ? 
                            AND invoices.date BETWEEN ? AND ?""",
                           ("credit", self.choices[1], self.choices[2], self.choices[3]))
            credit = cursor.fetchall()

        try:
            debit_total = 0
            for x in debit:
                url = f'https://v6.exchangerate-api.com/v6/047719de29e747e4c47ff286/latest/{x[1]}'


                response = requests.get(url)
                data = response.json()

                debit_total += (x[0] * data['conversion_rates'][f'{self.currency_entry.get()}'])

            credit_total = 0
            for x in credit:
                url = f'https://v6.exchangerate-api.com/v6/047719de29e747e4c47ff286/latest/{x[1]}'

                response = requests.get(url)
                data = response.json()

                credit_total += (x[0] * data['conversion_rates'][f'{self.currency_entry.get()}'])

            net_profit = credit_total - debit_total

            if self.choices[0] == "Income":
                value = debit_total
            elif self.choices[0] == "Expense":
                value = credit_total
            else:
                value = net_profit

            self.sum_label = Label(self.frame1, text=str(round(value, 2)))
            self.sum_label.grid(row=2, column=1, padx=10, pady=10)

        except KeyError:
            messagebox.showerror(message="There was an error converting betweeen two currencies")
        except TypeError:
            messagebox.showerror(message="There was an error calculating the total")
        except requests.exceptions.RequestException:
            messagebox.showerror(message="There was an error connecting to the currency API")

        # Commit changes
        conn.commit()
        # Close the connection
        conn.close()

    def go_back(self):
        self.destroy()


    def create_graph(self, graph_type):

        conn = sqlite3.connect('invoice_db.db')

        # Create a cursor instance
        cursor = conn.cursor()

        label1 = Label(self.frame2)
        label1.grid(row=1, column=0)
        label1.grid_forget()

        if graph_type == "monthly":
            cursor.execute("""SELECT total, currency, date FROM invoices 
                                    WHERE invoice_type = ? AND date BETWEEN date('now', '-1 year') AND date('now')""",
                           ("credit",))

            credit = cursor.fetchall()

            cursor.execute("""SELECT total, currency, date FROM invoices 
                                    WHERE invoice_type = ? AND date BETWEEN date('now', '-1 year') AND date('now')""",
                           ("debit",))

            debit = cursor.fetchall()

            conv_debit = []
            for x in debit:
                url = f'https://v6.exchangerate-api.com/v6/1110e25a39bd30a4865f39be/latest/{x[1]}'

                response = requests.get(url)
                data = response.json()

                conv_debit.append(x[0] * data['conversion_rates']['USD'])

            conv_credit = []
            for x in credit:
                url = f'https://v6.exchangerate-api.com/v6/1110e25a39bd30a4865f39be/latest/{x[1]}'

                response = requests.get(url)
                data = response.json()

                conv_credit.append(x[0] * data['conversion_rates']['USD'])

            df_debit = pd.DataFrame()
            df_debit['dates'] = [x[2] for x in debit]
            df_debit['values'] = [x for x in conv_debit]
            df_debit['dates'] = pd.to_datetime(df_debit['dates'])
            df_debit['dates'] = df_debit['dates'].apply(lambda x: str(x.year) + '-' + str(x.month))
            df_debit['dates'] = pd.to_datetime(df_debit['dates'], format='%Y-%m')

            df_credit = pd.DataFrame()
            df_credit['dates'] = [x[2] for x in credit]
            df_credit['values'] = [x for x in conv_credit]
            df_credit['dates'] = pd.to_datetime(df_credit['dates'])
            df_credit['dates'] = df_credit['dates'].apply(lambda x: str(x.year) + '-' + str(x.month))
            df_credit['dates'] = pd.to_datetime(df_credit['dates'], format='%Y-%m')

            layout = go.Layout(
                title='Income and Expenses',
                xaxis={'title': 'Month', 'dtick': 'M1'},
                yaxis={'title': 'Total'}
            )

        elif graph_type == "yearly":
            cursor.execute("SELECT total, currency, date FROM invoices WHERE invoice_type = ?", ("credit",))

            credit = cursor.fetchall()

            cursor.execute("SELECT total, currency, date FROM invoices WHERE invoice_type = ?", ("debit",))

            debit = cursor.fetchall()

            conv_debit = []
            for x in debit:
                url = f'https://v6.exchangerate-api.com/v6/047719de29e747e4c47ff286/latest/{x[1]}'

                response = requests.get(url)
                data = response.json()

                conv_debit.append(x[0] * data['conversion_rates']['USD'])

            conv_credit = []
            for x in credit:
                url = f'https://v6.exchangerate-api.com/v6/047719de29e747e4c47ff286/latest/{x[1]}'


                response = requests.get(url)
                data = response.json()

                conv_credit.append(x[0] * data['conversion_rates']['USD'])


            df_debit = pd.DataFrame()
            df_debit['dates'] = [x[2] for x in debit]
            df_debit['values'] = [x for x in conv_debit]
            df_debit['dates'] = pd.to_datetime(df_debit['dates'])
            df_debit['dates'] = df_debit['dates'].apply(lambda x: x.year)


            df_credit = pd.DataFrame()
            df_credit['dates'] = [x[2] for x in credit]
            df_credit['values'] = [x for x in conv_credit]
            df_credit['dates'] = pd.to_datetime(df_credit['dates'])
            df_credit['dates'] = df_credit['dates'].apply(lambda x: x.year)

            layout = go.Layout(
                title='Income and Expenses',
                xaxis={'title': 'Year'},
                yaxis={'title': 'Total'}
            )



        debit_data = df_debit.groupby(df_debit['dates'])['values'].sum()
        credit_data = df_credit.groupby(df_credit['dates'])['values'].sum()

        data = [
            go.Bar(
                x=credit_data.index,
                y=credit_data.values,
                name='Income',
                marker={'color': '#3FC1C9'}
            ),
            go.Bar(
                x=debit_data.index,
                y=debit_data.values,
                name='Expenses',
                marker={'color': '#95E1D3'}
            )
        ]
        fig = go.Figure(data = data, layout = layout)
        path = "D:/PycharmProjects/IA/images"
        if not os.path.exists(path):
            os.mkdir(path)

        fig.write_image(f"images/{graph_type}_{date.today()}.png")

        image1 = Image.open(f"images/{graph_type}_{date.today()}.png")
        img = ImageTk.PhotoImage(image1)
        image1.close()

        label1 = Label(self.frame2, image=img)
        label1.image = img
        label1.grid(row=1, column=0)

        # Commit changes
        conn.commit()
        # Close the connection
        conn.close()