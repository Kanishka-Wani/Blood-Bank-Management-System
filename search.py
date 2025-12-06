
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
import datetime

def connect_db():
    return mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        database="bloodbank"
    )

def open_search_donor_window(parent):
    """Open Donor Search Window"""
    win = Toplevel(parent)
    win.title("Donor Management - Blood Bank")
    win.geometry("900x600")
    win.config(bg="#f4f6f7")
    win.grab_set()

    current_view = ""  

    def clear_table():
        for row in tree.get_children():
            tree.delete(row)

    def show_table_frame():
        if not tree_frame.winfo_ismapped():
            tree_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

    def restore_donor_columns():
        nonlocal current_view
        current_view = "donors"
        tree["columns"] = ("Donor ID", "Name", "Age", "Gender", "Blood Type", "Phone")
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=140, anchor=CENTER)

    # ---------- Search Functions ----------
    def search_by_blood_type():
        restore_donor_columns()
        blood_type = simpledialog.askstring("Search Donors", "Enter Blood Type (e.g. A+, O-, B+):", parent=win)
        if not blood_type:
            return
        try:
            db = connect_db()
            cur = db.cursor()
            cur.execute(
                "SELECT donor_id, donor_name, age, gender, blood_type, phone FROM donors WHERE blood_type=%s",
                (blood_type,)
            )
            results = cur.fetchall()
            clear_table()
            show_table_frame()
            for row in results:
                tree.insert("", END, values=row)
            if not results:
                messagebox.showinfo("Info", f"No donors with {blood_type}")
            db.close()
        except Exception as e:
            messagebox.showerror("Error", e)

    def search_by_donor_id():
        restore_donor_columns()
        donor_id = simpledialog.askstring("Search Donor", "Enter Donor ID:", parent=win)
        if not donor_id:
            return
        try:
            db = connect_db()
            cur = db.cursor()
            cur.execute(
                "SELECT donor_id, donor_name, age, gender, blood_type, phone FROM donors WHERE donor_id=%s",
                (donor_id,)
            )
            results = cur.fetchall()
            clear_table()
            show_table_frame()
            for row in results:
                tree.insert("", END, values=row)
            if not results:
                messagebox.showinfo("Info", f"No donor found with ID {donor_id}")
            db.close()
        except Exception as e:
            messagebox.showerror("Error", e)

    def search_eligible_donors():
        restore_donor_columns()
        today = datetime.date.today()
        try:
            db = connect_db()
            cur = db.cursor()
            cur.execute(
                "SELECT donor_id, donor_name, age, gender, blood_type, phone FROM donors WHERE eligible_next_donation <= %s",
                (today,)
            )
            results = cur.fetchall()
            clear_table()
            show_table_frame()
            for row in results:
                tree.insert("", END, values=row)
            if not results:
                messagebox.showinfo("Info", "No eligible donors today")
            db.close()
        except Exception as e:
            messagebox.showerror("Error", e)

    # ---------- Styles ----------
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading",
                    font=("Arial", 12, "bold"),
                    foreground="white",
                    background="#8f0909")
    style.configure("Treeview",
                    font=("Arial", 11),
                    rowheight=28,
                    background="#ffffff",
                    fieldbackground="#f9f9f9")
    style.map("Treeview",
              background=[("selected", "#1976D2")],
              foreground=[("selected", "white")])

    # ---------- Title ----------
    Label(win, text="Donor Management", 
          font=("Arial", 20, "bold"), fg="white", 
          bg="#8f0909", pady=15).pack(fill=X)

    # ---------- Buttons ----------
    btn_frame = Frame(win, bg="#f4f6f7")
    btn_frame.pack(pady=15)

    def make_btn(text, color, cmd):
        return Button(btn_frame, text=text, font=("Arial", 12, "bold"),
                      bg=color, fg="white", activebackground="#333",
                      activeforeground="white", relief=FLAT,
                      width=22, height=2, cursor="hand2", command=cmd)

    make_btn("🔍 Search by Blood Type", "#009688", search_by_blood_type).grid(row=0, column=0, padx=10)
    make_btn("🔍 Search by Donor ID", "#607D8B", search_by_donor_id).grid(row=0, column=1, padx=10)
    make_btn("✅ Eligible Donors", "#3F51B5", search_eligible_donors).grid(row=0, column=2, padx=10)

    # ---------- Treeview ----------
    tree_frame = Frame(win, bg="white", bd=2, relief=RIDGE)
    tree = ttk.Treeview(tree_frame, columns=("Donor ID", "Name", "Age", "Gender", "Blood Type", "Phone"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col, anchor=CENTER)
        tree.column(col, width=140, anchor=CENTER)
    scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.pack(fill=BOTH, expand=True)

    # ---------- Back Button ----------
    back_btn = Button(win, text="Back", font=("Helvetica", 10, "bold"), fg="black",
                      bg="#9bffcd", bd=0, relief=FLAT, cursor="hand2", command=win.destroy)
    back_btn.place(x=800, y=20, width=70, height=30)

    # ---------- Footer ----------
    footer = Label(win, text="© 2025 Blood Bank | Designed By Kanishka Wani",
                   font=("Helvetica", 12, "italic"), fg="white", bg="#333")
    footer.pack(side=BOTTOM, fill=X)
