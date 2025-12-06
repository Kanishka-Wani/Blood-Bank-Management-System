
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog
import mysql.connector
import datetime

def connect_db():
    return mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        database="bloodbank"
    )

def open_blood_stock_window(parent):
    """Open the Blood Stock Management window"""
    win = Toplevel(parent)
    win.title("Blood Stock Management")
    win.geometry("900x600")
    win.configure(bg="#f5f5f5")
    win.grab_set()  

    # Title
    title = Label(win, text="Blood Stock Management", font=("Helvetica", 20, "bold"),
                  bg="#4A0606", fg="white")
    title.pack(fill=X)

    # Treeview
    tree_frame = Frame(win, bg="white")
    tree_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

    tree_scroll = ttk.Scrollbar(tree_frame, orient=VERTICAL)
    tree_scroll.pack(side=RIGHT, fill=Y)

    columns = ("Blood Type", "Quantity (in ML)", "Expiry Date")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=tree.yview)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200, anchor=CENTER)

    tree.pack(fill=BOTH, expand=True)

    # Helper functions
    def clear_table():
        for row in tree.get_children():
            tree.delete(row)

    def load_stock():
        clear_table()
        try:
            db = connect_db()
            cur = db.cursor()
            cur.execute("SELECT blood_type, quantity_ml, expiry_date FROM blood_stock")
            results = cur.fetchall()
            for row in results:
                tree.insert("", END, values=row)
            if not results:
                messagebox.showinfo("Info", "No blood stock available.")
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def add_blood_units():
        win.destroy()
        import add_stk  # Assuming you have add_stk.py for adding blood units

    def check_expired_units():
        clear_table()
        today = datetime.date.today()
        try:
            db = connect_db()
            cur = db.cursor()
            cur.execute("SELECT blood_type, quantity_ml, collection_date FROM blood_stock")
            rows = cur.fetchall()

            expired_units = []
            for blood_type, quantity, collection_date in rows:
                expiry_date = collection_date + datetime.timedelta(days=30)
                if today > expiry_date:
                    expired_units.append((blood_type, quantity, expiry_date))

            if expired_units:
                for row in expired_units:
                    tree.insert("", END, values=row)
            else:
                messagebox.showinfo("Info", "No expired blood units.")
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def check_availability():
        blood_type1 = simpledialog.askstring("Blood Type", "Enter Blood Type to Check Availability:", parent=win)
        if not blood_type1:
            return
        clear_table()
        try:
            db = connect_db()
            cur = db.cursor()
            cur.execute(
                "SELECT blood_type, quantity_ml, expiry_date FROM blood_stock WHERE blood_type=%s AND quantity_ml>0",
                (blood_type1,)
            )
            results = cur.fetchall()
            for row in results:
                tree.insert("", END, values=row)
            if not results:
                messagebox.showinfo("Info", f"No available units for {blood_type1}.")
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Buttons
    btn_frame = Frame(win, bg="#f5f5f5")
    btn_frame.pack(pady=10)

    btn_style = {"font": ("Helvetica", 12, "bold"), "fg": "white", "bg": "#4A0606",
                 "activebackground": "#FF4500", "bd": 0, "relief": FLAT, "width": 20,
                 "height": 2, "cursor": "hand2"}

    Button(btn_frame, text="Add Blood Units", command=add_blood_units, **btn_style).grid(row=0, column=0, padx=10)
    Button(btn_frame, text="Check Availability", command=check_availability, **btn_style).grid(row=0, column=1, padx=10)
    Button(btn_frame, text="Check Expired Units", command=check_expired_units, **btn_style).grid(row=0, column=2, padx=10)
    Button(btn_frame, text="Refresh Stock", command=load_stock, **btn_style).grid(row=0, column=3, padx=10)

    # Load initial stock
    load_stock()
