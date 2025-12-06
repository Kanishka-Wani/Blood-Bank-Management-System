from tkinter import *
from PIL import Image, ImageTk
import mysql.connector
from tkinter import messagebox
import datetime

# ----------------- Database Connection -----------------
def connect_db():
    return mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        database="bloodbank"
    )

# ----------------- Donor Registration Form -----------------
def open_register(parent=None):
    win = Toplevel(parent)
    win.geometry("530x700")
    win.title("Donor Registration - Blood Bank Management")

    # --- Background ---
    bg = Image.open(r"E:\Blood_Bank_Management\images\lblood.jpg")
    bg = bg.resize((600, 700), Image.LANCZOS)
    bg_img = ImageTk.PhotoImage(bg)
    Label(win, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)
    win.bg_img = bg_img  # keep reference

    Label(win, text="Donor Registration", font=('Arial',22,'bold'),
          fg="white", bg="#8f0909").pack(pady=15)

    container = Frame(win)
    container.pack(fill=BOTH, expand=True)

    canvas = Canvas(container, bg="white", highlightthickness=0)
    scrollbar = Scrollbar(container, orient=VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    form_frame = Frame(canvas, bg="white", bd=2, relief=RIDGE)
    canvas.create_window((0,0), window=form_frame, anchor='nw')

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox('all'))
    form_frame.bind('<Configure>', on_configure)

    f1 = ('Times New Roman', 14, 'bold')
    width_val = 45
    padx_val = 25

    # ---------- Form Fields ----------
    Label(form_frame, text="Donor ID", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    txt_donor_id = Entry(form_frame, font=f1, bd=1, relief=SOLID, width=width_val)
    txt_donor_id.pack(fill="x", padx=padx_val, pady=6)

    Label(form_frame, text="Full Name", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    txt_donor_name = Entry(form_frame, font=f1, bd=1, relief=SOLID, width=width_val)
    txt_donor_name.pack(fill="x", padx=padx_val, pady=6)

    Label(form_frame, text="Age", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    txt_age = Entry(form_frame, font=f1, bd=1, relief=SOLID, width=width_val)
    txt_age.pack(fill="x", padx=padx_val, pady=6)

    # Gender
    Label(form_frame, text="Gender", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    gender_var = IntVar()
    gender_frame = Frame(form_frame, bg="white")
    gender_frame.pack(fill="x", padx=padx_val, pady=6)
    Radiobutton(gender_frame, text="Male", font=("Arial",12), bg="white", variable=gender_var, value=1).pack(side=LEFT, padx=10)
    Radiobutton(gender_frame, text="Female", font=("Arial",12), bg="white", variable=gender_var, value=2).pack(side=LEFT, padx=10)

    # Blood Type
    Label(form_frame, text="Blood Type", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    blood_groups = ["A+","A-","B+","B-","AB+","AB-","O+","O-"]
    bg_var = StringVar()
    bg_var.set("Select")
    OptionMenu(form_frame, bg_var, *blood_groups).pack(fill="x", padx=padx_val, pady=6)

    # Phone, Email, Address
    Label(form_frame, text="Phone Number", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    txt_phone = Entry(form_frame, font=f1, bd=1, relief=SOLID, width=width_val)
    txt_phone.pack(fill="x", padx=padx_val, pady=6)

    Label(form_frame, text="Email", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    txt_email = Entry(form_frame, font=f1, bd=1, relief=SOLID, width=width_val)
    txt_email.pack(fill="x", padx=padx_val, pady=6)

    Label(form_frame, text="Address", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    txt_address = Entry(form_frame, font=f1, bd=1, relief=SOLID, width=width_val)
    txt_address.pack(fill="x", padx=padx_val, pady=6)

    # Last Donation & Next Donation
    Label(form_frame, text="Last Donation Date (YYYY-MM-DD)", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    txt_last_donation = Entry(form_frame, font=f1, bd=1, relief=SOLID, width=width_val)
    txt_last_donation.pack(fill="x", padx=padx_val, pady=6)

    Label(form_frame, text="Eligible Next Donation (YYYY-MM-DD)", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    txt_next_donation = Entry(form_frame, font=f1, bd=1, relief=SOLID, width=width_val)
    txt_next_donation.pack(fill="x", padx=padx_val, pady=6)

    # Registration Date
    Label(form_frame, text="Registration Date (YYYY-MM-DD)", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    txt_registration = Entry(form_frame, font=f1, bd=1, relief=SOLID, width=width_val)
    txt_registration.pack(fill="x", padx=padx_val, pady=6)
    txt_registration.insert(0, str(datetime.date.today()))
    txt_registration.config(state="readonly")

    # Calculate next donation automatically
    def calculate_next_donation(event=None):
        try:
            last_date = datetime.datetime.strptime(txt_last_donation.get(), "%Y-%m-%d").date()
            next_date = last_date + datetime.timedelta(days=90)
            txt_next_donation.delete(0, END)
            txt_next_donation.insert(0, str(next_date))
        except:
            txt_next_donation.delete(0, END)
    txt_last_donation.bind("<FocusOut>", calculate_next_donation)

    # Generate next Donor ID
    def maxrec():
        try:
            db = connect_db()
            cur = db.cursor()
            cur.execute("SELECT MAX(donor_id) FROM donors")
            mx = cur.fetchone()[0] or 0
            txt_donor_id.delete(0, END)
            txt_donor_id.insert(0, str(mx+1))
            db.close()
        except:
            txt_donor_id.insert(0, "1")
    maxrec()

    # Save Function
    def save():
        s1 = txt_donor_id.get()
        s2 = txt_donor_name.get()
        s3 = txt_age.get()
        s4 = "Male" if gender_var.get()==1 else "Female" if gender_var.get()==2 else None
        s5 = bg_var.get()
        s6 = txt_phone.get()
        s7 = txt_email.get()
        s8 = txt_address.get()
        s9 = txt_last_donation.get()
        s10 = txt_next_donation.get()
        s11 = txt_registration.get()

        if not (s1 and s2 and s3 and s4 and s5!="Select" and s6 and s7 and s8 and s9 and s10 and s11):
            messagebox.showerror("Error","Please fill all fields.")
            return

        try:
            db = connect_db()
            cur = db.cursor()
            sql = """INSERT INTO donors 
                     (donor_id, donor_name, age, gender, blood_type, phone, email, address, last_donation_date, eligible_next_donation, registration_date)
                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            val = (s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11)
            cur.execute(sql,val)
            db.commit()
            messagebox.showinfo("Success","Donor registered successfully.")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"{e}")

    # Buttons
    Button(form_frame, text="Submit", font=('Arial',14,'bold'), bg="#1976d2", fg="white", bd=0, relief=FLAT, cursor="hand2", height=2, width=12, command=save).pack(pady=15)
    Button(form_frame, text="Cancel", font=('Arial',14,'bold'), bg="#B22222", fg="white", bd=0, relief=FLAT, cursor="hand2", height=2, width=12, command=win.destroy).pack(pady=10)

    win.mainloop()

# Run the registration form
if __name__ == "__main__":
    open_register()
