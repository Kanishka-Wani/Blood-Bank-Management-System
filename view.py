from tkinter import *
import tkinter.ttk as ttk
import mysql.connector
from tkinter import messagebox

# PDF libraries
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def connect_db():
    return mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        database="bloodbank"
    )

# ----------------- PDF GENERATION FUNCTION -----------------
def generate_donor_report():
    try:
        db = connect_db()
        cur = db.cursor()
        cur.execute("SELECT donor_id, donor_name, age, gender, blood_type, phone FROM donors")
        results = cur.fetchall()
        db.close()

        if not results:
            messagebox.showinfo("Info", "No donors found to generate report.")
            return

        # Create PDF file
        pdf = SimpleDocTemplate("Donor_Report.pdf")
        data = [["Donor ID", "Name", "Age", "Gender", "Blood Type", "Phone"]]
        data.extend(results)

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.darkred),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 10),
            ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ]))

        pdf.build([table])
        messagebox.showinfo("Success", "PDF report created successfully as Donor_Report.pdf")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate report: {e}")


# ----------------- MAIN Donor View Window -----------------
def open_view_donors(parent):
    win = Toplevel(parent)
    win.title("View Donors")
    win.geometry("900x500")
    win.configure(bg="#f5f5f5")
    win.grab_set() 

    title = Label(win, text="Donors List", font=("Helvetica", 20, "bold"), bg="#4A0606", fg="white")
    title.pack(fill=X)

    tree_frame = Frame(win, bg="white")
    tree_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

    tree_scroll = ttk.Scrollbar(tree_frame, orient=VERTICAL)
    tree_scroll.pack(side=RIGHT, fill=Y)

    tree = ttk.Treeview(tree_frame, columns=("Donor ID", "Name", "Age", "Gender", "Blood Type", "Phone"),
                        show="headings", yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=tree.yview)

    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=140, anchor=CENTER)

    tree.pack(fill=BOTH, expand=True)

    # Insert data into table
    try:
        db = connect_db()
        cur = db.cursor()
        cur.execute("SELECT donor_id, donor_name, age, gender, blood_type, phone FROM donors")
        results = cur.fetchall()

        for row in results:
            tree.insert("", END, values=row)

        if not results:
            messagebox.showinfo("Info", "No donors found in the database.")
        db.close()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

    btn_frame = Frame(win, bg="#f5f5f5")
    btn_frame.pack(pady=10)

    report_btn = Button(btn_frame, text="Generate Report (PDF)", font=("Helvetica", 14, "bold"),
                        fg="white", bg="#4A0606", cursor="hand2",
                        command=generate_donor_report)
    report_btn.grid(row=0, column=0, padx=10)

    back_btn = Button(btn_frame, text="Back", font=("Helvetica", 14, "bold"),
                    fg="white", bg="#4A0606", cursor="hand2",
                    command=win.destroy)
    back_btn.grid(row=0, column=1, padx=10)

