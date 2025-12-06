from tkinter import *
from tkinter import messagebox
import mysql.connector
import datetime

def connect_db():
    return mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        database="bloodbank"
    )


win = Tk()
win.title("Add Blood Unit")
win.geometry("450x500")
win.configure(bg="#f5f5f5")

Label(win, text="Add Blood Unit", font=("Helvetica", 16, "bold"), bg="#4A0606", fg="white").pack(fill=X, pady=10)

# Blood Type
Label(win, text="Blood Type:", font=("Helvetica", 12), bg="#f5f5f5").pack(anchor="w", padx=20, pady=(10,0))
blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
blood_var = StringVar()
blood_var.set("Select")
OptionMenu(win, blood_var, *blood_types).pack(fill=X, padx=20, pady=5)

# Donor ID
Label(win, text="Donor ID (Optional):", font=("Helvetica", 12), bg="#f5f5f5").pack(anchor="w", padx=20, pady=(10,0))
donor_entry = Entry(win)
donor_entry.pack(fill=X, padx=20, pady=5)

Label(win, text="Collection Date (YYYY-MM-DD):", font=("Helvetica", 12), bg="#f5f5f5").pack(anchor="w", padx=20, pady=(10,0))
collection_entry = Entry(win)
collection_entry.pack(fill=X, padx=20, pady=5)
collection_entry.insert(0, str(datetime.date.today()))

Label(win, text="Expiry Date (YYYY-MM-DD):", font=("Helvetica", 12), bg="#f5f5f5").pack(anchor="w", padx=20, pady=(10,0))
expiry_entry = Entry(win)
expiry_entry.pack(fill=X, padx=20, pady=5)

def calculate_expiry(event=None):
    try:
        collection_date = datetime.datetime.strptime(collection_entry.get(), "%Y-%m-%d").date()
        expiry_date = collection_date + datetime.timedelta(days=30)  # Blood expires after 30 days
        expiry_entry.delete(0, END)
        expiry_entry.insert(0, str(expiry_date))
    except Exception as e:
        expiry_entry.delete(0, END)
        expiry_entry.insert(0, "Invalid Date")

# Trigger expiry calculation when collection date changes
collection_entry.bind("<FocusOut>", calculate_expiry)

# Initial calculation
calculate_expiry()
Label(win, text="Quantity (ml):", font=("Helvetica", 12), bg="#f5f5f5").pack(anchor="w", padx=20, pady=(10,0))
qty_entry = Entry(win)
qty_entry.pack(fill=X, padx=20, pady=5)
qty_entry.insert(0, "450")

def save_unit():
    blood_type = blood_var.get()
    donor_id = donor_entry.get() if donor_entry.get() else None
    collection_date = collection_entry.get()
    expiry_date = expiry_entry.get()
    quantity_ml = qty_entry.get()

    if blood_type == "Select" or not collection_date or not expiry_date or not quantity_ml:
        messagebox.showwarning("Warning", "Please fill all required fields.")
        return

    status = "Available"

    try:
        db = connect_db()
        cur = db.cursor()
        sql = """INSERT INTO blood_stock 
                (blood_type, donor_id, collection_date, expiry_date, quantity_ml, status)
                VALUES (%s, %s, %s, %s, %s, %s)"""
        val = (blood_type, donor_id, collection_date, expiry_date, quantity_ml, status)
        cur.execute(sql, val)
        db.commit()
        messagebox.showinfo("Success", "Blood unit added successfully!")
        win.destroy()
    except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def cancel():
    win.destroy()
    import blood_stk


btn_frame = Frame(win, bg="#f5f5f5")
btn_frame.pack(pady=30)

Button(btn_frame, text="Save", font=("Helvetica", 12, "bold"),
       bg="#1976d2", fg="white", activebackground="#1565c0", cursor="hand2",
       height=2, width=15, command=save_unit).pack(side=LEFT, padx=10)

Button(btn_frame, text="Cancel", font=("Helvetica", 12, "bold"),
       bg="#f58181", fg="white", activebackground="#d32f2f", cursor="hand2",
       height=2, width=15, command=cancel).pack(side=LEFT, padx=10)

win.mainloop()


