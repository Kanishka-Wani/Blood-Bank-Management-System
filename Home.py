# home.py
from tkinter import *
from PIL import Image, ImageTk
import donar_mng
import blood_stk
import blood_req
import search

def open_home_window():
    win = Tk()
    win.geometry("1000x700")
    win.title("Blood Bank Management System")
    win.config(bg="white")

    title_font = ('Arial', 26, 'bold')
    button_font = ('Arial', 16, 'bold')

    # Background Image
    bg = Image.open(r"E:\Blood_Bank_Management\images\lblood.jpg")
    bg = bg.resize((1000, 700), Image.LANCZOS)
    bg_img = ImageTk.PhotoImage(bg)
    lbl_bg = Label(win, image=bg_img)
    lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

    # ---------- Header ----------
    header = Frame(win, bg="black", height=60)
    header.pack(fill=X, side=TOP)

    title = Label(header, text="🩸 Blood Bank Management System",
                  font=("Arial", 20, "bold"), fg="white", bg="black")
    title.pack(side=LEFT, padx=20, pady=10)

    exit_btn = Button(header, text="Exit", font=("Arial", 12, "bold"),
                      fg="white", bg="grey20",
                      activebackground="darkred", activeforeground="white",
                      bd=0, relief="flat", padx=15, pady=6,
                      command=win.destroy)
    exit_btn.pack(side=RIGHT, padx=10, pady=10)

    def logout():
        win.destroy()
        import Login


    signout_btn = Button(header, text="Sign Out", font=("Arial", 12, "bold"),
                         fg="white", bg="red3",
                         activebackground="darkred", activeforeground="white",
                         bd=0, relief="flat", padx=15, pady=6,
                         command=logout)
    signout_btn.pack(side=RIGHT, padx=20, pady=10)

    # ---------- Center Frame ----------
    frame = Frame(win, bg="white", bd=3, relief=GROOVE)
    frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=500)

    Label(frame, text="Welcome!", font=title_font, fg="red3", bg="white").pack(pady=(30, 10))
    Label(frame, text="Choose an option below to continue",
          font=("Arial", 12), fg="grey20", bg="white").pack(pady=(0, 20))

    # ---------- Button Style ----------
    style = {"font": button_font, "fg": "white", "bg": "red3",
             "activebackground": "darkred", "activeforeground": "white",
             "bd": 0, "relief": "flat", "width": 25, "height": 2}

    # ---------- Buttons ----------
    Button(frame, text="🧑‍🤝‍🧑 Donor Management", **style,
           command=lambda: donar_mng.open_donor_mng(win)).pack(pady=12)
    Button(frame, text="📦 Blood Stock Management", **style,
           command=lambda: blood_stk.open_blood_stock_window(win)).pack(pady=12)
    Button(frame, text="📑 Blood Requests", **style,
           command=lambda: blood_req.open_blood_request_window(win)).pack(pady=12)
    Button(frame, text="🔍 Find Donor", **style,
           command=lambda: search.open_search_donor_window(win)).pack(pady=12)

    # ---------- Footer ----------
    footer = Label(win, text="© 2025 Blood Bank | Designed By Kanishka Wani",
                   font=("Arial", 11, "italic"), fg="white", bg="black")
    footer.pack(side=BOTTOM, fill=X)

    win.mainloop()
