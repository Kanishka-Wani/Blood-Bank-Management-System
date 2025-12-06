from tkinter import *
from PIL import Image, ImageTk
import mysql.connector
from tkinter import messagebox
import Home

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bloodbank"
)

mycur=mydb.cursor()



def on_login():
    username = txtuname.get()
    password = txtpwd.get()
    sql = "SELECT * FROM user WHERE username = %s AND password = %s"
    val = (username, password)
    mycur.execute(sql, val)
    result = mycur.fetchone()
    if result:
        messagebox.showinfo("Login", "Login successful!")
        win.destroy()  
        Home.open_home_window()


    else:
        messagebox.showerror("Login", "Incorrect username or password.")

win = Tk()
win.geometry("500x570")
win.title("Login")

f1 = ('Times New Roman', 14, 'bold')

bg = Image.open(r"E:\Blood_Bank_Management\images\lblood.jpg")
bg = bg.resize((500, 550), Image.LANCZOS)
bg_img = ImageTk.PhotoImage(bg)

lbl_bg = Label(win, image=bg_img)
lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

form_frame = Frame(win, bg="white", bd=2, relief=RIDGE)
form_frame.place(relx=0.5, rely=0.45, anchor="center", width=360, height=400)

icon = Image.open(r"E:\Blood_Bank_Management\images\login.png")
icon = icon.resize((70, 70), Image.LANCZOS)
icon_img = ImageTk.PhotoImage(icon)

lbl_icon = Label(form_frame, image=icon_img, bg="white")
lbl_icon.pack(pady=(15, 8))

h1 = Label(form_frame, text='User Login', font=('Arial', 22, 'bold'), fg='grey20', bg="white")
h1.pack(pady=(0, 20))

l1 = Label(form_frame, text='User Name', font=f1, fg="black", bg="white")
l1.pack(anchor="w", padx=25)
txtuname = Entry(form_frame, font=f1, bd=1, relief=SOLID)
txtuname.pack(fill="x", padx=25, pady=8)


l2 = Label(form_frame, text='Password', font=f1, fg="black", bg="white")
l2.pack(anchor="w", padx=25, pady=(12, 0))

pwd_frame = Frame(form_frame, bg="white")
pwd_frame.pack(fill="x", padx=25, pady=8)

txtpwd = Entry(pwd_frame, font=f1, show='*', bd=1, relief=SOLID)
txtpwd.pack(side=LEFT, fill="x", expand=True)

def toggle_password():
    if txtpwd.cget("show") == "":
        txtpwd.config(show="*")
        btn_eye.config(text="👁")
    else:
        txtpwd.config(show="")
        btn_eye.config(text="🚫")

btn_eye = Button(pwd_frame, text="👁", font=("Arial", 10), bd=0, bg="white",
                 command=toggle_password, cursor="hand2")
btn_eye.pack(side=RIGHT, padx=5)

def on_enter(e):
    e.widget.config(bg="#a50000")

def on_leave(e):
    e.widget.config(bg="#d32f2f")

b1 = Button(form_frame, text='Login', font=('Arial', 14, 'bold'),
            bg='#d32f2f', fg='white', activebackground="#a50000",
            activeforeground="white", cursor="hand2",
            bd=0, relief=FLAT, height=2, width=18, command=on_login)
b1.pack(pady=25)
b1.bind("<Enter>", on_enter)
b1.bind("<Leave>", on_leave)

bottom_frame = Frame(win, bg="white")
bottom_frame.place(relx=0.5, rely=0.88, anchor="center")

b2 = Button(bottom_frame, text='Register', font=('Arial', 12, 'bold'),
            bg="#d32f2f", fg='white', activebackground="#0d47a1",
            activeforeground="white", cursor="hand2",
            bd=0, relief=FLAT, width=12, height=2)
b2.grid(row=0, column=0, padx=12, pady=5)

b3 = Button(bottom_frame, text='Exit', font=('Arial', 12, 'bold'),
            bg='#424242', fg='white', activebackground="#212121",
            activeforeground="white", cursor="hand2",
            bd=0, relief=FLAT, width=12, height=2, command=win.destroy)
b3.grid(row=0, column=1, padx=12, pady=5)

win.mainloop()
