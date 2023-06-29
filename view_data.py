import tkinter as tk
from tkinter import ttk
import sqlite3
import webbrowser

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Database Records")
        self.geometry("800x600")
        
        self.create_widgets()
        self.load_records()
        
    def create_widgets(self):
        # Treeview to display records
        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("col1", "col2", "col3")  # Modify the column names as per your database schema
        self.tree.heading("#0", text="ID")
        self.tree.column("#0", width=50)
        self.tree.heading("col1", text="Column 1")
        self.tree.column("col1", width=200)
        self.tree.heading("col2", text="Column 2")
        self.tree.column("col2", width=300)
        self.tree.heading("col3", text="Column 3")
        self.tree.column("col3", width=200)
        self.tree.pack(expand=True, fill=tk.BOTH)
        
        self.tree.bind("<Double-1>", self.open_url)  # Double-click event to open URL
        
    def load_records(self):
        # Connect to SQLite database
        conn = sqlite3.connect("database.db")  # Replace "your_database.db" with your database file
        
        # Retrieve records from the database
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")  # Replace "users" with your table name
        records = cursor.fetchall()
        
        # Clear existing records in the treeview
        self.tree.delete(*self.tree.get_children())
        
        # Insert records into the treeview
        for record in records:
            record_id = record[0]
            col1 = record[1]
            col2 = record[2]
            col3 = record[3]
            
            self.tree.insert("", "end", text=record_id, values=(col1, col2, col3))
        
        # Close the database connection
        cursor.close()
        conn.close()
        
    def open_url(self, event):
        item = self.tree.selection()[0]
        record_id = self.tree.item(item, "text")
        
        # Connect to SQLite database
        conn = sqlite3.connect("your_database.db")  # Replace "your_database.db" with your database file
        
        # Retrieve the URL for the selected record
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM users WHERE id=?", (record_id,))  # Replace "users" with your table name
        url = cursor.fetchone()[0]
        
        # Open the URL in a web browser
        webbrowser.open(url)
        
        # Close the database connection
        cursor.close()
        conn.close()
        
app = App()
app.mainloop()
