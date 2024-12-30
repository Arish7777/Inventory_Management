from tkinter import *
from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
import os,sys
import email_pass
import smtplib  
import time
import sqlite3

class Login_System:

    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Online Retail Store Database System | Developed By Arish")
        self.bg_img = Image.open("images/leftmenu.png")  # Replace with the correct image path
        self.bg_img = self.bg_img.resize((1366, 768), Image.Resampling.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)

        self.bg_label = Label(self.root, image=self.bg_img)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.focus_force()

        SearchFrame = LabelFrame(self.root, font=("times new roman", 12, "bold"), bg="#d5821e" ,bd=2, relief=RIDGE)
        SearchFrame.place(x=180,y=10,width=900,height=800)

        # === Images ===
        self.phone_image = ImageTk.PhotoImage(file="images/phone.png")
        self.lbl_Phone_image = Label(self.root, image=self.phone_image, bd=0,bg="#d5821e").place(x=200, y=50)

        # === Login Frame ===
        login_frame = Frame(self.root, bd=2, relief=RIDGE, bg="#f19f3c")
        login_frame.place(x=650, y=90, width=360, height=460)

        title = Label(login_frame, text="Login System", font=("Elephant", 30, "bold"), bg="#f19f3c", fg="black")
        title.place(x=27, y=30)

        lbl_user = Label(login_frame, text="Username", font=("Andalus", 15), bg="#f19f3c",fg="black")
        lbl_user.place(x=50, y=100)

        self.username = StringVar()
        self.password = StringVar()

        txt_username = Entry(login_frame, textvariable=self.username, font=("times new roman", 15), bg="white")
        txt_username.place(x=50, y=130, width=250)

        lbl_pass = Label(login_frame, text="Password", font=("Andalus", 15),  bg="#f19f3c",fg="black")
        lbl_pass.place(x=50, y=170)

        txt_pass = Entry(login_frame, textvariable=self.password, show="*", font=("times new roman", 15), bg="white")
        txt_pass.place(x=50, y=200, width=250)

        btn_login = Button(login_frame, command=self.login, text="Log In", font=("Arial Rounded MT Bold", 15), bg="#b48a58", fg="black")
        btn_login.place(x=50, y=250, width=250, height=35)

        hr = Label(login_frame, bg="lightgray").place(x=50, y=300, width=250, height=2)

        or_ = Label(login_frame, text="OR", bg="#f19f3c", fg="black", font=("times new roman", 15, "bold"))
        or_.place(x=150, y=320)

        btn_forget = Button(login_frame, text="Forget Password?", command=self.forget_window, font=("times new roman", 13), bg="#b48a58",fg="black")
        btn_forget.place(x=100, y=360)

        # === Frame2 ===
        register_frame = Frame(self.root, bd=2, relief=RIDGE, bg="#f19f3c")
        register_frame.place(x=650, y=570, width=360, height=60)

        lbl_reg = Label(register_frame, text="Don't have an account ?", font=("times new roman", 13), bg="#f19f3c", fg="black")
        lbl_reg.place(x=40, y=20)

        btn_signup = Button(register_frame, text="Sign Up", font=("times new roman", 13, "bold"), bg="#b48a58", fg="black")
        btn_signup.place(x=210, y=15)

        # === Animation Images ===
        self.im1 = ImageTk.PhotoImage(file="images/im1.png")
        self.im2 = ImageTk.PhotoImage(file="images/im2.png")
        self.im3 = ImageTk.PhotoImage(file="images/im3.png")

        self.lbl_change_image = Label(self.root, bg="white")
        self.lbl_change_image.place(x=367, y=153, width=240, height=428)

        self.animate()

    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000, self.animate)


    def login(self):
        conn = sqlite3.connect(database=r'DB PROJECT.db')
        cur = conn.cursor()

        try:
            # Check if username or password is empty
            if not self.username.get() or not self.password.get():
                messagebox.showerror("Error", "All fields are required", parent=self.root)
                return

            # Execute query to check user credentials
            cur.execute("SELECT utype FROM employee WHERE eid=? AND pass=?", 
                        (self.username.get(), self.password.get()))
            user = cur.fetchone()

            if user is None:
                messagebox.showerror("Error", "Invalid USERNAME/PASSWORD", parent=self.root)
            else:
                # Check user type and redirect accordingly
                target_script = "images/dashboard.py" if user[0] == "Admin" else "images/billing.py"
                self.root.destroy()  # Destroy the root only after everything else
                os.system(f"{sys.executable} {target_script}")

        except Exception as ex:
            # Handle exception before destroying the root
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def forget_window(self):
        conn = sqlite3.connect(database=r'DB PROJECT.db')
        cur = conn.cursor()
        try:
            print(f"self.root type before checks: {type(self.root)}")  # Debugging

            if self.username.get() == "":
                print("Username is empty")  # Debugging
                print(f"Parent type for messagebox: {type(self.root)}")
                messagebox.showerror('Error', 'Employee ID must be required', parent=self.root)
            else:
                cur.execute("SELECT email FROM employee WHERE eid=?", (self.username.get(),))
                email = cur.fetchone()
                print(f"Fetched email: {email}")  # Debugging

                if email is None:
                    print(f"Parent type for messagebox: {type(self.root)}")
                    messagebox.showerror('Error', 'Invalid Employee ID, try again', parent=self.root)
                else:
                    print(f"self.root type before Toplevel: {type(self.root)}")  # Debugging

                    self.var_otp = StringVar()
                    self.var_new_pass = StringVar()
                    self.var_conf_pass = StringVar()

                    self.forget_win = Toplevel(self.root)
                    print(f"self.forget_win type: {type(self.forget_win)}")  # Debugging
                    self.forget_win.title('RESET PASSWORD')
                    self.forget_win.geometry('400x350+500+100')
                    self.forget_win.focus_force()

                    chk = self.send_email(email[0])
                    print(f"Result of send_email: {chk}, type: {type(chk)}")  # Debugging

                    if chk == 'f':
                        print(f"Parent type for messagebox: {type(self.forget_win)}")
                        messagebox.showerror('Error', 'Failed to send OTP, try again', parent=self.forget_win)
                        self.forget_win.destroy()
                        return

                    Label(self.forget_win, text='Reset Password', font=('goudy old style', 15, 'bold')).place(x=0, y=10, relwidth=1)
                    Label(self.forget_win, text="Enter OTP Sent on Registered Email", font=("times new roman", 15)).place(x=20, y=50)
                    Entry(self.forget_win, textvariable=self.var_otp, font=("times new roman", 15)).place(x=20, y=90, width=250)
                    Button(self.forget_win, text="SUBMIT", command=self.validate_otp, font=("times new roman", 15), bg="lightblue", fg="black").place(x=280, y=90, width=100, height=30)

                    Label(self.forget_win, text="New Password", font=("times new roman", 15)).place(x=20, y=140)
                    Entry(self.forget_win, textvariable=self.var_new_pass, font=("times new roman", 15), show="*").place(x=20, y=170, width=250)
                    Label(self.forget_win, text="Confirm Password", font=("times new roman", 15)).place(x=20, y=210)
                    Entry(self.forget_win, textvariable=self.var_conf_pass, font=("times new roman", 15), show="*").place(x=20, y=240, width=250)

                    Button(self.forget_win, text="Update", command=self.update_password, font=("times new roman", 15), bg="lightblue", fg="black").place(x=150, y=300, width=100, height=30)
        except Exception as ex:
            print(f"Exception: {ex}")  # Debugging
            print(f"Parent type for messagebox: {type(self.root)}")
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            conn.close()


    def send_email(to_, root):
        try:
            # Establish SMTP connection
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()

            # Replace these with valid credentials
            email = "muhammadarishkhan555@gmail.com"  # Your Gmail address
            pass_ = "null"     # App Password generated in Google account

            # Login to the email account
            s.login(email, pass_)

            # Generate OTP
            otp = int(time.strftime("%H%S%M")) + int(time.strftime("%S"))

            # Email content
            subj = 'IMS-Reset Password OTP'
            msg = f'Dear Sir/Madam, \n\nYour Reset OTP is {otp}.\n\nWith Regards, \nIMS Team'
            msg = f"Subject: {subj}\n\n{msg}"

        # Send the email
            s.sendmail(email, to_, msg)
            chk = s.ehlo()  # Check connection status

            s.quit()  # Close the connection

        # Check response
            if chk[0] == 250:
                return 's'  # Success
            else:
                return 'f'  # Failure
        except smtplib.SMTPAuthenticationError:
            messagebox.showerror('Error', 'Invalid email credentials or account settings. Please check.', parent=root)
            return 'f'
        except Exception as ex:
            messagebox.showerror('Error', f"Error while sending email: {str(ex)}", parent=root)
            return 'f'



    
    

root = tk.Tk()
obj = Login_System(root)
root.mainloop()

# Replace with a valid recipient email
recipient_email = "muhammedarishkhan555@gmailcom"
result = Login_System.send_email(recipient_email, root)

if result == 's':
    print("Email sent successfully!")
else:
    print("Failed to send email.")