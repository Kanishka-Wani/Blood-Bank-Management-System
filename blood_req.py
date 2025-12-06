
from tkinter import *
from tkinter import messagebox, simpledialog
import tkinter.ttk as ttk
import mysql.connector
import datetime

def connect_db():
    return mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        database="bloodbank"
    )

def open_blood_request_window(parent):
    """Open Blood Request Management Window"""
    win = Toplevel(parent)
    win.title("Blood Request Management")
    win.geometry("1250x650")
    win.configure(bg="#f5f5f5")
    win.grab_set()  

    Label(win, text="Blood Request Management", font=("Helvetica", 22, "bold"),
          bg="#4A0606", fg="white").pack(fill=X)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview.Heading", background="#1976d2", foreground="white",
                    font=("Helvetica", 12, "bold"))
    style.configure("Treeview", font=("Helvetica", 11), rowheight=30)

    tree_frame = Frame(win, bg="white")
    tree_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

    tree_scroll = ttk.Scrollbar(tree_frame, orient=VERTICAL)
    tree_scroll.pack(side=RIGHT, fill=Y)

    columns = ("Request ID", "Patient Name", "Blood Type", "Quantity Needed", 
               "Urgency", "Hospital Name", "Contact Phone", "Request Date", "Status")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=tree.yview)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor=CENTER)

    tree.pack(fill=BOTH, expand=True)

    def clear_table():
        for row in tree.get_children():
            tree.delete(row)

    def load_requests(priority_filter=None):
        clear_table()
        try:
            db = connect_db()
            cur = db.cursor()

            sql = """SELECT request_id, patient_name, blood_type, quantity_needed, 
                     urgency, hospital_name, contact_phone, request_date, status 
                     FROM blood_requests"""

            if priority_filter:
                sql += " WHERE urgency IN ('High', 'Critical')"

            sql += """ ORDER BY FIELD(urgency,'Critical','High','Normal','Low'), request_date ASC"""
            cur.execute(sql)
            results = cur.fetchall()

            for i, row in enumerate(results):
                urgency = row[4]
                if urgency == "Critical":
                    tag = "critical"
                elif urgency == "High":
                    tag = "high"
                elif urgency == "Normal":
                    tag = "normal"
                elif urgency == "Low":
                    tag = "low"
                elif i % 2 == 0:
                    tag = "evenrow"
                else:
                    tag = "oddrow"
                tree.insert("", END, values=row, tags=(tag,))

            # Tag colors
            tree.tag_configure("critical", background="#FF9999")  # Red
            tree.tag_configure("high", background="#FFD699")      # Orange
            tree.tag_configure("normal", background="#ffffff")    # White
            tree.tag_configure("low", background="#CCFFCC")       # Greenish
            tree.tag_configure("oddrow", background="#f9f9f9")
            tree.tag_configure("evenrow", background="#e6e6e6")

            if not results:
                messagebox.showinfo("Info", "No blood requests found.")
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_status():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a request to update.")
            return
        item = tree.item(selected[0])
        req_id = item['values'][0]

        new_status = simpledialog.askstring("Update Status", "Enter new status (Pending/Fulfilled/Cancelled):", parent=win)
        if new_status not in ["Pending", "Fulfilled", "Cancelled"]:
            messagebox.showwarning("Warning", "Invalid status entered.")
            return
        try:
            db = connect_db()
            cur = db.cursor()
            cur.execute("UPDATE blood_requests SET status=%s WHERE request_id=%s", (new_status, req_id))
            db.commit()
            messagebox.showinfo("Success", f"Request {req_id} status updated to {new_status}.")
            load_requests()
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def new_request():
        new_win = Toplevel(win)
        new_win.title("New Blood Request")
        new_win.geometry("450x550")
        new_win.configure(bg="#f5f5f5")
        new_win.grab_set()

        Label(new_win, text="New Blood Request", font=("Helvetica", 16, "bold"), 
              bg="#4A0606", fg="white").pack(fill=X, pady=10)

        # Input Fields
        def make_label(entry_text):
            Label(new_win, text=entry_text, font=("Helvetica", 12), bg="#f5f5f5").pack(anchor="w", padx=20, pady=(10,0))

        make_label("Patient Name:")
        name_entry = Entry(new_win)
        name_entry.pack(fill=X, padx=20, pady=5)

        make_label("Blood Type:")
        blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        blood_var = StringVar()
        blood_var.set("Select")
        OptionMenu(new_win, blood_var, *blood_types).pack(fill=X, padx=20, pady=5)

        make_label("Quantity Needed (ml):")
        qty_entry = Entry(new_win)
        qty_entry.pack(fill=X, padx=20, pady=5)
        qty_entry.insert(0, "450")

        make_label("Urgency:")
        urgency_var = StringVar()
        urgency_var.set("Normal")
        OptionMenu(new_win, urgency_var, "Low", "Normal", "High", "Critical").pack(fill=X, padx=20, pady=5)

        make_label("Hospital Name:")
        hospital_entry = Entry(new_win)
        hospital_entry.pack(fill=X, padx=20, pady=5)

        make_label("Contact Phone:")
        contact_entry = Entry(new_win)
        contact_entry.pack(fill=X, padx=20, pady=5)

        # Submit function
        def submit_request():
            patient_name = name_entry.get()
            blood_type = blood_var.get()
            quantity = qty_entry.get()
            urgency = urgency_var.get()
            hospital = hospital_entry.get()
            contact = contact_entry.get()
            request_date = datetime.date.today()
            status = "Pending"

            if not patient_name or blood_type=="Select" or not quantity or not hospital or not contact:
                messagebox.showwarning("Warning", "Please fill all required fields.")
                return

            try:
                db = connect_db()
                cur = db.cursor()
                sql = """INSERT INTO blood_requests
                         (patient_name, blood_type, quantity_needed, urgency, hospital_name, contact_phone, request_date, status)
                         VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
                val = (patient_name, blood_type, quantity, urgency, hospital, contact, request_date, status)
                cur.execute(sql, val)
                db.commit()

                if urgency == "Critical":
                    messagebox.showwarning("Critical Request!", f"New Critical request added for {patient_name}!")

                messagebox.showinfo("Success", "Blood request added successfully!")
                new_win.destroy()
                load_requests()
                db.close()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        # Buttons
        btn_frame = Frame(new_win, bg="#f5f5f5")
        btn_frame.pack(pady=20)
        Button(btn_frame, text="Submit", font=("Helvetica", 12, "bold"), bg="#1976d2", fg="white",
               height=2, width=15, command=submit_request).pack(side=LEFT, padx=10)
        Button(btn_frame, text="Cancel", font=("Helvetica", 12, "bold"), bg="#f58181", fg="white",
               height=2, width=15, command=new_win.destroy).pack(side=LEFT, padx=10)

    # Main Buttons
    btn_frame_main = Frame(win, bg="#f5f5f5")
    btn_frame_main.pack(pady=10)

    Button(btn_frame_main, text="New Request", font=("Helvetica", 12, "bold"), bg="#4A0606", fg="white",
           width=18, height=2, command=new_request).pack(side=LEFT, padx=10)
    Button(btn_frame_main, text="Update Status", font=("Helvetica", 12, "bold"), bg="#FFA500", fg="white",
           width=18, height=2, command=update_status).pack(side=LEFT, padx=10)
    Button(btn_frame_main, text="High/Critical Only", font=("Helvetica", 12, "bold"),
           bg="#E74C3C", fg="white", width=18, height=2,
           command=lambda: load_requests(priority_filter=True)).pack(side=LEFT, padx=10)
    Button(btn_frame_main, text="Refresh All", font=("Helvetica", 12, "bold"),
           bg="#1976d2", fg="white", width=18, height=2,
           command=lambda: load_requests(priority_filter=None)).pack(side=LEFT, padx=10)
    Button(btn_frame_main, text="Cancel", font=("Helvetica", 12, "bold"),
           bg="#9E9E9E", fg="white", width=18, height=2,
           command=win.destroy).pack(side=LEFT, padx=10)

    load_requests()
