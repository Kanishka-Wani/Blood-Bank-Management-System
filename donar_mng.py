from tkinter import *
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import mysql.connector
from tkinter import messagebox, simpledialog
import datetime
import donar_register 

def connect_db():
    return mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        database="bloodbank"
    )

def open_donor_mng(root):   
    win = Toplevel(root)
    win.geometry("1000x700")
    win.title("Donor Management")
    win.configure(bg="#f5f5f5")

    def add_donor():
        donar_register.open_register(win)

    def update_donor():
        import update_donor
        update_donor.open_search_window(win) 

        

    def delete_donor():
        donor_ID = simpledialog.askstring("Input", "Enter Donor ID to delete:")
        if not donor_ID:
            return
        if not donor_ID.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric Donor ID")
            return

        db = connect_db()
        mycur = db.cursor()
        mycur.execute("SELECT * FROM donors WHERE donor_id=%s", (donor_ID,))
        donor = mycur.fetchone()
        if not donor:
            messagebox.showerror("Error", f"No donor found with ID {donor_ID}")
            db.close()
            return

        ans = messagebox.askyesno("Delete", "Are you sure you want to delete this donor?")
        if ans:
            sql = "DELETE FROM donors WHERE donor_id = %s"
            val = (donor_ID,)
            mycur.execute(sql, val)
            db.commit()
            messagebox.showinfo("Delete", "Donor deleted successfully.")
        db.close()

    def view_donors_list():
        import view
        view.open_view_donors(win)

    def search_donor():
       import search
       search.open_search_donor_window(win)


    def home():
        win.destroy()

    title_font = ('Helvetica', 28, 'bold')
    card_font = ('Helvetica', 16, 'bold')
    button_font = ('Helvetica', 14, 'bold')

    bg = Image.open(r"E:\Blood_Bank_Management\images\donar.jpg")
    bg = bg.resize((1000, 700), Image.LANCZOS)
    bg_img = ImageTk.PhotoImage(bg)
    lbl_bg = Label(win, image=bg_img)
    lbl_bg.image = bg_img
    lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

    header = Frame(win, bg="#550404", height=60)
    header.pack(fill=X, side=TOP)

    title = Label(header, text="Donor Management", font=("Arial", 20, "bold"),
                  fg="white", bg="#4A0606")
    title.pack(side=LEFT, padx=20, pady=10)

    lbl = Label(win, text="Total Donors", font=card_font, fg="white",
                bg="#F40A0A", padx=30, pady=30, bd=0, relief=RIDGE)
    lbl.place(x=660, y=120)

    def get_total_donors():
        db = connect_db()
        mycur = db.cursor()
        mycur.execute("SELECT COUNT(*) FROM donors")
        result = mycur.fetchone()
        total = result[0] if result else 0
        return total

    def refresh_total_label():
        total_donors = get_total_donors()
        lbl_total.config(text=f"Total Donors: {total_donors}")

    card_font = ("Arial", 16, "bold")
    lbl_total = Label(win, text="Total Donors: 0", font=card_font,
                      fg="white", bg="#F40A0A", padx=30, pady=30,
                      bd=0, relief=RIDGE)
    lbl_total.place(x=660, y=120)

    def on_enter(e):
        e.widget['background'] = '#FF4500'

    def on_leave(e):
        e.widget['background'] = "#060000"

    btn_style = {"font": button_font, "fg": "white", "bg": "#060000",
                 "activeforeground": "white", "bd": 0, "relief": FLAT,
                 "width": 22, "height": 2, "cursor": "hand2"}

    btn_positions = [
        {"text": "➕ Add New Donor", "x": 620, "y": 250, "cmd":lambda: add_donor()},
        {"text": "✏️ Update Donor Info", "x": 620, "y": 320, "cmd": update_donor},
        {"text": "🗑️ Delete Donor", "x": 620, "y": 390, "cmd": delete_donor},
        {"text": "📋 View Donor List", "x": 620, "y": 460, "cmd": view_donors_list},
        {"text": "🔍 Search Donor", "x": 620, "y": 530, "cmd": search_donor},
    ]

    for b in btn_positions:
        btn = Button(win, text=b["text"], **btn_style, command=b["cmd"])
        btn.place(x=b["x"], y=b["y"])
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    back_btn = Button(win, text="Back", font=("Helvetica", 14, "bold"),
                      fg="black", bg="#9bffcd", bd=0, relief=FLAT,
                      cursor="hand2", command=home)
    back_btn.place(x=750, y=10, width=100, height=40)

    exit_btn = Button(win, text="Exit", font=("Helvetica", 14, "bold"),
                      fg="black", bg="#f58181", bd=0, relief=FLAT,
                      cursor="hand2", command=win.destroy)
    exit_btn.place(x=870, y=10, width=100, height=40)

    footer = Label(win, text="© 2025 Blood Bank | Designed By Kanishka Wani",
                   font=("Helvetica", 12, "italic"), fg="white", bg="#333")
    footer.pack(side=BOTTOM, fill=X)

    refresh_total_label()
