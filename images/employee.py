from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3

class employee:
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

        #--All Variables
        self.search_by = StringVar()
        self.search_txt = StringVar()

        self.var_emp_id = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_address = StringVar()
        self.var_salary = StringVar()

        #--SearchFrame
        SearchFrame = LabelFrame(self.root,text="Search Employee", font=("times new roman", 12, "bold"), bg="#d5821e" ,bd=2, relief=RIDGE)
        SearchFrame.place(x=200,y=10,width=950,height=80)

        #--options
        cmd_search=ttk.Combobox(SearchFrame,textvariable=self.search_by,values=("Select","Eid","Ename","Contact","Email"),font=("goudy old style", 12, "bold"), state="readonly", justify=CENTER)
        cmd_search.place(x=10, y=10, width=300, height=30)
        cmd_search.current(0)

        #--search
        txt_search = Entry(SearchFrame,textvariable=self.search_txt, font=("goudy old style", 15), bg="lightyellow")
        txt_search.place(x=330, y=10, width=450, height=30)

        #--search button
        search_btn = Button(SearchFrame, text="Search",command=self.search,font=("goudy old style", 12, "bold"), bg="#b48a58", fg="black", cursor="hand2")
        search_btn.place(x=830, y=10, width=100, height=30)

        #--Title
        title = Label(self.root, text="Employee Details", font=("times new roman", 20, "bold"), bg="#d5821e", fg="black")
        title.place(x=200, y=100, width=950, height=35)

        #--Table
        table_frame = Frame(self.root, bd=3,bg="#d5821e", relief=RIDGE)
        table_frame.place(x=200, y=140, width=950, height=550)

        #--content
        lbl_empid = Label(self.root, text="Emp ID", font=("times new roman", 15, "bold"), bg="#d5821e").place(x=220, y=160)
        lbl_gender = Label(self.root, text="Gender", font=("times new roman", 15, "bold"), bg="#d5821e").place(x=520, y=160)
        lbl_contact = Label(self.root, text="Contact", font=("times new roman", 15, "bold"), bg="#d5821e").place(x=820, y=160)

        txt_empid = Entry(self.root, textvariable=self.var_emp_id, font=("goudy old style", 15), bg="lightyellow")
        txt_empid.place(x=220, y=190, width=180)
        cmd_gender = ttk.Combobox(self.root, textvariable=self.var_gender,values=("Select","Male","Female","Other"), font=("goudy old style", 15), state="readonly")
        cmd_gender.place(x=520, y=190, width=180)
        cmd_gender.current(0)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow")
        txt_contact.place(x=820, y=190, width=180)

        #--name
        lbl_name = Label(self.root, text="Name", font=("times new roman", 15, "bold"), bg="#d5821e").place(x=220, y=230)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow")
        txt_name.place(x=220, y=260, width=180)

        #--dob
        lbl_dob = Label(self.root, text="D.O.B", font=("times new roman", 15, "bold"), bg="#d5821e").place(x=520, y=230)
        txt_dob = Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15), bg="lightyellow")
        txt_dob.place(x=520, y=260, width=180)

        #--doj
        lbl_doj = Label(self.root, text="D.O.J", font=("times new roman", 15, "bold"), bg="#d5821e").place(x=820, y=230)
        txt_doj = Entry(self.root, textvariable=self.var_doj, font=("goudy old style", 15), bg="lightyellow")
        txt_doj.place(x=820, y=260, width=180)

        #--email
        lbl_email = Label(self.root, text="Email", font=("times new roman", 15, "bold"), bg="#d5821e").place(x=220, y=300)
        txt_email = Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15), bg="lightyellow")
        txt_email.place(x=220, y=330, width=180)

        #--search
        lbl_pass = Label(self.root, text="Password", font=("times new roman", 15, "bold"), bg="#d5821e").place(x=520, y=300)
        txt_pass = Entry(self.root, textvariable=self.var_pass, font=("goudy old style", 15), bg="lightyellow")
        txt_pass.place(x=520, y=330, width=180)

        lbl_utype = Label(self.root, text="User Type", font=("times new roman", 15, "bold"), bg="#d5821e").place(x=820, y=300)
        cmd_utype = ttk.Combobox(self.root, textvariable=self.var_utype,values=("Select","Admin","Employee"), font=("goudy old style", 15), state="readonly")
        cmd_utype.place(x=820, y=330, width=180)
        cmd_utype.current(0)
        
        lbl_address = Label(self.root, text="Address", font=("times new roman", 15, "bold"), bg="#d5821e").place(x=220, y=380)
        self.txt_address = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_address.place(x=220, y=410, width=480, height=128)

        lbl_salary = Label(self.root, text="Salary", font=("times new roman", 15, "bold"), bg="#d5821e").place(x=820, y=380)
        self.txt_salary = Entry(self.root, textvariable=self.var_salary,font=("goudy old style", 15), bg="lightyellow")
        self.txt_salary.place(x=820, y=410, width=180)

        #--buttons
        btn_add = Button(self.root, text="Save",command=self.add, font=("times new roman", 12, "bold"), bg="#b48a58", fg="black", cursor="hand2").place(x=820, y=450, width=110, height=40)
        btn_update = Button(self.root, text="Update",command=self.update, font=("times new roman", 12, "bold"), bg="#b48a58", fg="black", cursor="hand2").place(x=950, y=450, width=110, height=40)
        btn_delete = Button(self.root, text="Delete",command=self.delete, font=("times new roman", 12, "bold"), bg="#b48a58", fg="black", cursor="hand2").place(x=820, y=500, width=110, height=40)
        btn_clear = Button(self.root, text="Clear",command=self.clear, font=("times new roman", 12, "bold"), bg="#b48a58", fg="black", cursor="hand2").place(x=950, y=500, width=110, height=40)

        #--Employee Details
        emp_frame = Frame(self.root, bd=3, relief=RIDGE,bg="lightyellow")
        emp_frame.place(x=200, y=550, width=950, height=140)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)
        self.EmployeeTable = ttk.Treeview(emp_frame, columns=("eid", "ename", "email", "gender","contact","dob", "doj", "pass", "utype", "address", "salary"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)
        self.EmployeeTable.heading("eid", text="Employee ID")
        self.EmployeeTable.heading("ename", text="Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("dob", text="D.O.B")
        self.EmployeeTable.heading("doj", text="D.O.J")
        self.EmployeeTable.heading("pass", text="Password")
        self.EmployeeTable.heading("utype", text="User Type")
        self.EmployeeTable.heading("address" ,text="Address")
        self.EmployeeTable.heading("salary" ,text="Salary")
        self.EmployeeTable["show"] = "headings"
        

        self.EmployeeTable.column("eid", width=100)
        self.EmployeeTable.column("ename", width=100)
        self.EmployeeTable.column("email", width=100)
        self.EmployeeTable.column("gender", width=100)
        self.EmployeeTable.column("contact", width=100)
        self.EmployeeTable.column("dob", width=100)
        self.EmployeeTable.column("doj", width=100)
        self.EmployeeTable.column("pass", width=100)
        self.EmployeeTable.column("utype", width=100)
        self.EmployeeTable.column("address", width=100)
        self.EmployeeTable.column("salary", width=100)
        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

#============================================================================

    def add(self):
        conn = sqlite3.connect(database=r'DB PROJECT.db')
        cur=conn.cursor()
        try:
            if self.var_emp_id.get() == "" or self.var_name.get() == "":
                messagebox.showerror("Error", "emp_id and name required", parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "This employee id already assigned, try different", parent=self.root)
                else:
                    cur.execute("Insert into employee (eid, ename, email, gender, contact, dob, doj, pass, utype, address, salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                        self.var_emp_id.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get("1.0", END),
                        self.var_salary.get()
                    ))
                    conn.commit()
                    messagebox.showinfo('Success', 'Employee Added Successfully', parent=self.root)
                    self.show()
                    conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)
    
    def show(self):
        conn = sqlite3.connect(database=r'DB PROJECT.db')
        cur=conn.cursor()
        try:
            cur.execute("select * from employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                row = list(row)  # Convert tuple to list to modify it
                #row[7] = '********' 
                self.EmployeeTable.insert('', END, values=row)
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)
    
    def get_data(self, ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete("1.0", END)
        self.txt_address.insert(END, row[9])
        self.var_salary.set(row[10])

    def update(self):
        conn=sqlite3.connect(database=r'DB PROJECT.db')
        cur=conn.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee id must be required", parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid employee id", parent=self.root)
                else:
                    cur.execute("Update employee set ename=?, email=?, gender=?, contact=?, dob=?, doj=?, pass=?, utype=?, address=?, salary=? where eid=?",(
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0', END),
                        self.var_salary.get(),
                        self.var_emp_id.get()
                    ))
                    conn.commit()
                    messagebox.showinfo('Success', 'Employee Details Updated Successfully', parent=self.root)
                    self.show()
                    conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)
    
    def delete(self):
        if self.var_emp_id.get() == "":
            messagebox.showerror("Error", "Employee id must be required", parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Delete", "Do you really want to delete?", parent=self.root)
                if delete>0:
                    conn=sqlite3.connect(database=r'DB PROJECT.db')
                    cur=conn.cursor()
                    sql="delete from employee where eid=?"
                    cur.execute(sql, (self.var_emp_id.get(),))
                conn.commit()
                self.show()
                self.clear()
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)
   

    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utyape.set("Select")
        self.txt_address.delete("1.0", END)
        self.var_salary.set("")
        self.search_txt.set("")
        self.search_by.set("Select")
        self.show()
    
    def search(self):
        conn = sqlite3.connect(database=r'DB PROJECT.db')
        cur = conn.cursor()
        try:
            if self.search_by.get() == "Select":
                messagebox.showerror("Error", "Select Search By Option", parent=self.root)
            elif self.search_txt.get() == "":
                messagebox.showerror("Error", "Search Input should be required", parent=self.root)
            else:
                cur.execute("select * from employee where "+self.search_by.get()+" LIKE '%"+self.search_txt.get()+"%'")
                rows = cur.fetchall()
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No Data Found !!!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)


if __name__ == "__main__":
# Initialize the root window
    root = Tk()
# Create an instance of the IMS class
    obj = employee(root)
# Start the main loop
    root.mainloop()