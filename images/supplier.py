from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3

class supplier:
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

        self.var_sup_invoice = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        

        #--SearchFrame
        SearchFrame = LabelFrame(self.root,text="Search supplier", font=("times new roman", 12, "bold"), bg="#d5821e" ,bd=2, relief=RIDGE)
        SearchFrame.place(x=200,y=10,width=950,height=80)

        #--options
        lbl_search=Label(SearchFrame,text='Search By Invoice no',bg="#d5821e", font=("goudy old style", 15,"bold"),bd=2, fg="black")
        lbl_search.place(x=30, y=10, height=30)

        #--search
        txt_search = Entry(SearchFrame,textvariable=self.search_txt, font=("goudy old style", 15), bg="lightyellow")
        txt_search.place(x=260, y=10, width=550, height=30)

        #--search button
        search_btn = Button(SearchFrame, text="Search",command=self.search,font=("goudy old style", 12, "bold"), bg="#b48a58", fg="black", cursor="hand2")
        search_btn.place(x=830, y=10, width=100, height=30)

        #--Title
        title = Label(self.root, text="Supplier Details", font=("times new roman", 20, "bold"), bg="#d5821e", fg="black")
        title.place(x=200, y=100, width=950, height=35)

        #--Table
        table_frame = Frame(self.root, bd=3,bg="#d5821e", relief=RIDGE)
        table_frame.place(x=200, y=140, width=950, height=550)

        #--content
        lbl_supp_invoice = Label(self.root, text="Invoice no", font=("times new roman", 15, "bold"), bg="#d5821e").place(x=220, y=160)

        txt_supp_invoice = Entry(self.root, textvariable=self.var_sup_invoice, font=("goudy old style", 15), bg="lightyellow")
        txt_supp_invoice.place(x=220, y=190, width=180)

        #--name
        lbl_name = Label(self.root, text="Name", font=("times new roman", 15, "bold"), bg="#d5821e").place(x=220, y=230)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow")
        txt_name.place(x=220, y=260, width=180)

        #--contact
        lbl_contact= Label(self.root, text="Contact", font=("times new roman", 15, "bold"), bg="#d5821e").place(x=220, y=300)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow")
        txt_contact.place(x=220, y=330, width=180)

        #--search
        lbl_desc = Label(self.root, text="Description", font=("times new roman", 15, "bold"), bg="#d5821e").place(x=220, y=380)
        self.txt_desc = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_desc.place(x=220, y=410, width=480, height=128)

        #--buttons
        btn_add = Button(self.root, text="Save",command=self.add, font=("times new roman", 12, "bold"), bg="#b48a58", fg="black", cursor="hand2").place(x=220, y=570, width=110, height=40)
        btn_update = Button(self.root, text="Update",command=self.update, font=("times new roman", 12, "bold"), bg="#b48a58", fg="black", cursor="hand2").place(x=340, y=570, width=110, height=40)
        btn_delete = Button(self.root, text="Delete",command=self.delete, font=("times new roman", 12, "bold"), bg="#b48a58", fg="black", cursor="hand2").place(x=460, y=570, width=110, height=40)
        btn_clear = Button(self.root, text="Clear",command=self.clear, font=("times new roman", 12, "bold"), bg="#b48a58", fg="black", cursor="hand2").place(x=580, y=570, width=110, height=40)

        #--supplier Details
        emp_frame = Frame(self.root, bd=3, relief=RIDGE,bg="lightyellow")
        emp_frame.place(x=720, y=160, width=410, height=450)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)
        self.supplierTable = ttk.Treeview(emp_frame, columns=("invoice", "name", "contact", "desc"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)
        self.supplierTable.heading("invoice", text="supplier ID")
        self.supplierTable.heading("name", text="Name")
        self.supplierTable.heading("contact", text="Contact")
        self.supplierTable.heading("desc", text="Description")
        self.supplierTable["show"] = "headings"
        

        self.supplierTable.column("invoice", width=100)
        self.supplierTable.column("name", width=100)
        self.supplierTable.column("contact", width=100)
        self.supplierTable.column("desc", width=100)
        
        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

#============================================================================

    def add(self):
        conn = sqlite3.connect(database=r'DB PROJECT.db')
        cur=conn.cursor()
        try:
            if self.var_sup_invoice.get() == "" :
                messagebox.showerror("Error", "Invoice must be required", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "This supplier invoice is already assigned, try different", parent=self.root)
                else:
                    cur.execute("Insert into supplier (invoice,name,contact,desc) values(?,?,?,?)",(
                        self.var_sup_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get("1.0", END),
                    ))
                    conn.commit()
                    messagebox.showinfo('Success', 'Supplier Added Successfully', parent=self.root)
                    self.show()
                    conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)
    
    def show(self):
        conn = sqlite3.connect(database=r'DB PROJECT.db')
        cur=conn.cursor()
        try:
            cur.execute("select * from supplier")
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())

            self.supplierTable.column("invoice", anchor=CENTER)
            self.supplierTable.column("name", anchor=CENTER)
            self.supplierTable.column("contact", anchor=CENTER)
            self.supplierTable.column("desc", anchor=CENTER)

            for row in rows:
                self.supplierTable.insert('', END, values=row,)
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)
    
    def get_data(self, ev):
        f=self.supplierTable.focus()
        content=(self.supplierTable.item(f))
        row=content['values']
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete("1.0", END)
        self.txt_desc.insert(END, row[3])

    def update(self):
        conn=sqlite3.connect(database=r'DB PROJECT.db')
        cur=conn.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "supplier invoice no must be required", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Invoice no", parent=self.root)
                else:
                    cur.execute("Update supplier set name=?, contact=?, desc=? where invoice=?",(
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0', END),
                        self.var_sup_invoice.get()
                    ))
                    conn.commit()
                    messagebox.showinfo('Success', 'Suppliers Details Updated Successfully', parent=self.root)
                    self.show()
                    conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)
    
    def delete(self):
        if self.var_sup_invoice.get() == "":
            messagebox.showerror("Error", "supplier invoice no must be required", parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Delete", "Do you really want to delete?", parent=self.root)
                if delete>0:
                    conn=sqlite3.connect(database=r'DB PROJECT.db')
                    cur=conn.cursor()
                    sql="delete from supplier where invoice=?"
                    cur.execute(sql, (self.var_sup_invoice.get(),))
                conn.commit()
                self.show()
                self.clear()
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)
   

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete("1.0", END)
        self.search_txt.set("")
        self.show()
    
    def search(self):
        conn = sqlite3.connect(database=r'DB PROJECT.db')
        cur = conn.cursor()
        try:
            if self.search_txt.get() == "":
                messagebox.showerror("Error", "Invoice no should be required", parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?",(self.search_txt.get(),))
                row = cur.fetchone()
                if row!=None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No Data Found !!!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)


if __name__ == "__main__":
# Initialize the root window
    root = Tk()
# Create an instance of the IMS class
    obj = supplier(root)
# Start the main loop
    root.mainloop()