from tkinter import *
from tkinter import messagebox
import mysql.connector
import datetime
from PIL import Image, ImageTk

# ---------------------- DB Connection ----------------------
def get_connection():
    return mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        database="bloodbank"
    )

# ---------------------- Fetch Donor ----------------------
def get_donor_by_id(donor_id):
    mydb = get_connection()
    mycur = mydb.cursor()
    mycur.execute("SELECT * FROM donors WHERE donor_id=%s", (donor_id,))
    data = mycur.fetchone()
    mydb.close()
    return data

# ---------------------- Update Donor in DB ----------------------
def update_donor_in_db(values):
    try:
        mydb = get_connection()
        mycur = mydb.cursor()
        sql = """UPDATE donors SET 
                    donor_name=%s, age=%s, gender=%s, blood_type=%s, 
                    phone=%s, email=%s, address=%s, 
                    last_donation_date=%s, eligible_next_donation=%s, registration_date=%s 
                 WHERE donor_id=%s"""
        mycur.execute(sql, values)
        mydb.commit()
        mydb.close()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Database Error: {e}")
        return False

# ---------------------- Update Donor Window ----------------------
def open_update_window(donor_id):
    donor_data = get_donor_by_id(donor_id)
    if not donor_data:
        messagebox.showerror("Error", f"No donor found with ID {donor_id}")
        return

    win = Tk()
    win.geometry("530x700")
    win.title("Update Donor - Blood Bank Management")

    f1 = ('Times New Roman', 14, 'bold')

    # Background Image
    bg = Image.open(r"E:\Blood_Bank_Management\images\lblood.jpg")
    bg = bg.resize((600, 700), Image.LANCZOS)
    bg_img = ImageTk.PhotoImage(bg)
    lbl_bg = Label(win, image=bg_img)
    lbl_bg.image = bg_img
    lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

    Label(win, text="Update Donor Information", font=('Arial', 22, 'bold'),
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
    canvas.create_window((0, 0), window=form_frame, anchor='nw')

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox('all'))

    form_frame.bind('<Configure>', on_configure)

    width_val = 45
    padx_val = 25

    # Donor ID
    Label(form_frame, text="Donor ID", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    txt_donor_id = Entry(form_frame, font=f1, bd=1, relief=SOLID, width=width_val)
    txt_donor_id.pack(fill="x", padx=padx_val, pady=6)
    txt_donor_id.insert(0, donor_data[0])
    txt_donor_id.config(state="readonly")

    # Full Name
    Label(form_frame, text="Full Name", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    txt_donor_name = Entry(form_frame, font=f1, bd=1, relief=SOLID, width=width_val)
    txt_donor_name.pack(fill="x", padx=padx_val, pady=6)
    txt_donor_name.insert(0, donor_data[1])

    # Age
    Label(form_frame, text="Age", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    txt_age = Entry(form_frame, font=f1, bd=1, relief=SOLID, width=width_val)
    txt_age.pack(fill="x", padx=padx_val, pady=6)
    txt_age.insert(0, donor_data[2])

    # Gender
    Label(form_frame, text="Gender", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    gender_frame = Frame(form_frame, bg="white")
    gender_frame.pack(fill="x", padx=padx_val, pady=6)
    gender_var = IntVar()
    Radiobutton(gender_frame, text="Male", font=("Arial", 12), bg="white", variable=gender_var, value=1).pack(side=LEFT, padx=10)
    Radiobutton(gender_frame, text="Female", font=("Arial", 12), bg="white", variable=gender_var, value=2).pack(side=LEFT, padx=10)
    gender_var.set(1 if donor_data[3] == "Male" else 2)

    # Blood Type
    Label(form_frame, text="Blood Type", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    bg_var = StringVar()
    bg_var.set(donor_data[4])
    OptionMenu(form_frame, bg_var, *blood_groups).pack(fill="x", padx=padx_val, pady=6)

    # Phone
    Label(form_frame, text="Phone Number", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    txt_phone = Entry(form_frame, font=f1, bd=1, relief=SOLID, width=width_val)
    txt_phone.pack(fill="x", padx=padx_val, pady=6)
    txt_phone.insert(0, donor_data[5])

    # Email
    Label(form_frame, text="Email", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    txt_email = Entry(form_frame, font=f1, bd=1, relief=SOLID, width=width_val)
    txt_email.pack(fill="x", padx=padx_val, pady=6)
    txt_email.insert(0, donor_data[6])

    # Address
    Label(form_frame, text="Address", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    txt_address = Entry(form_frame, font=f1, bd=1, relief=SOLID, width=width_val)
    txt_address.pack(fill="x", padx=padx_val, pady=6)
    txt_address.insert(0, donor_data[7])

    # Last Donation
    Label(form_frame, text="Last Donation Date (YYYY-MM-DD)", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    txt_last_donation = Entry(form_frame, font=f1, bd=1, relief=SOLID, width=width_val)
    txt_last_donation.pack(fill="x", padx=padx_val, pady=6)
    txt_last_donation.insert(0, donor_data[8])

    # Next Donation
    Label(form_frame, text="Eligible Next Donation (YYYY-MM-DD)", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    txt_next_donation = Entry(form_frame, font=f1, bd=1, relief=SOLID, width=width_val)
    txt_next_donation.pack(fill="x", padx=padx_val, pady=6)
    txt_next_donation.insert(0, donor_data[9])

    # Registration Date
    Label(form_frame, text="Registration Date (YYYY-MM-DD)", font=f1, bg="white").pack(anchor="w", padx=padx_val, pady=(10,0))
    txt_registration = Entry(form_frame, font=f1, bd=1, relief=SOLID, width=width_val)
    txt_registration.pack(fill="x", padx=padx_val, pady=6)
    txt_registration.insert(0, donor_data[10])
    txt_registration.config(state="readonly")

    # Auto-calc next donation
    def calculate_next_donation(event=None):
        try:
            last_donation = datetime.datetime.strptime(txt_last_donation.get(), "%Y-%m-%d").date()
            next_donation = last_donation + datetime.timedelta(days=90)
            txt_next_donation.delete(0, END)
            txt_next_donation.insert(0, str(next_donation))
        except:
            txt_next_donation.delete(0, END)

    txt_last_donation.bind("<FocusOut>", calculate_next_donation)

    # Save Updates
    def save_update():
        donor_id_val = txt_donor_id.get()
        donor_name = txt_donor_name.get()
        age = txt_age.get()
        gender = "Male" if gender_var.get() == 1 else "Female"
        blood_type = bg_var.get()
        phone = txt_phone.get()
        email = txt_email.get()
        address = txt_address.get()
        last_donation = txt_last_donation.get()
        next_donation = txt_next_donation.get()
        registration_date = txt_registration.get()

        if not (donor_name and age and phone and email and address and last_donation and next_donation):
            messagebox.showerror("Error", "Please fill all fields before updating.")
            return

        values = (donor_name, age, gender, blood_type, phone, email, address,
                  last_donation, next_donation, registration_date, donor_id_val)

        if update_donor_in_db(values):
            messagebox.showinfo("Success", "Donor details updated successfully.")
            win.destroy()

    Button(form_frame, text="Update", font=('Arial', 14, 'bold'),
           bg="#1976d2", fg="white", bd=0, relief=FLAT,
           cursor="hand2", height=2, width=12, command=save_update).pack(pady=15)

    win.mainloop()

# ---------------------- Search Window ----------------------
def open_search_window():
    win = Tk()
    win.geometry("400x200")
    win.title("Search Donor to Update")

    Label(win, text="Enter Donor ID", font=("Arial", 14, "bold")).pack(pady=20)
    donor_id_entry = Entry(win, font=("Arial", 14), width=20, bd=2, relief=SOLID)
    donor_id_entry.pack(pady=10)

    def search_donor():
        donor_id = donor_id_entry.get().strip()
        if not donor_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric Donor ID")
            return
        donor_data = get_donor_by_id(int(donor_id))
        if donor_data:
            win.destroy()
            open_update_window(int(donor_id))
        else:
            messagebox.showerror("Error", f"No donor found with ID {donor_id}")

    Button(win, text="Search", font=("Arial", 12, "bold"),
           bg="#1976d2", fg="white", width=12, height=2,
           command=search_donor).pack(pady=15)

    win.mainloop()

# Run search window
open_search_window()
