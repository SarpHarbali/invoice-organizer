from welcome import HomePage
import sqlite3

if __name__ == '__main__':
    # Create the database or connect to the existing database
    conn = sqlite3.connect('invoice_db.db')

    # Create a cursor instance
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS companies (
                        company_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        company_name TEXT,
                        company_address TEXT,
                        vat_number INTEGER)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS invoices (
                invoices_id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_type TEXT,
                invoice_number INTEGER,
                total INTEGER,
                currency TEXT,
                date DATE,
                company_id INTEGER,
                FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE SET NULL)""")
    # Commit changes
    conn.commit()

    # Close the connection
    conn.close()

    new = HomePage("Home", "1000x1000")
    new.mainloop()