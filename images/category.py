from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3

class category:
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

        #variables
        self.var_cat_id=StringVar()
        self.var_name=StringVar()

        #title
        lbl_title=Label(self.root,text="Manage Product Category",font=("times new roman", 30, "bold"),bg="#d5821e", fg="black",bd=2, relief=RIDGE).place(x=160,y=10,width=1050,height=80)
        
        #frame
        table_frame = Frame(self.root, bd=3,bg="#d5821e", relief=RIDGE)
        table_frame.place(x=160, y=110, width=1050, height=580)
        
        #labels and entries
        lbl_name=Label(self.root,text="Enter Category Name",font=("times new roman", 20, "bold"),bg="#d5821e", fg="black").place(x=200, y=150)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("times new roman", 20, "bold"),bg="white", fg="black").place(x=200, y=200)

        #buttons
        btn_add = Button(self.root, text="Add",command=self.add, font=("times new roman", 12, "bold"), bg="#b48a58", fg="black", cursor="hand2").place(x=530, y=200, width=110, height=38)
        btn_delete = Button(self.root, text="Delete",command=self.delete,font=("times new roman", 12, "bold"), bg="#b48a58", fg="black", cursor="hand2").place(x=660, y=200, width=110, height=38)
        
        #TreeView
        cat_farme = Frame(self.root, bd=3, relief=RIDGE,bg="lightyellow")
        cat_farme.place(x=780, y=200, width=410, height=450)

        scrolly = Scrollbar(cat_farme, orient=VERTICAL)
        scrollx = Scrollbar(cat_farme, orient=HORIZONTAL)
        self.category_Table = ttk.Treeview(cat_farme, columns=("cid", "name"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.category_Table.xview)
        scrolly.config(command=self.category_Table.yview)
        self.category_Table.heading("cid", text="category ID")
        self.category_Table.heading("name", text="Name")
        self.category_Table["show"] = "headings"
        
        self.category_Table.column("cid", width=100)
        self.category_Table.column("name", width=100)
        
        self.category_Table.pack(fill=BOTH, expand=1)
        self.category_Table.bind("<ButtonRelease-1>", self.get_data)

        #images
        self.img1=Image.open("images/cat2.jpg")
        self.img1=self.img1.resize((600,450), Image.Resampling.LANCZOS)
        self.img1=ImageTk.PhotoImage(self.img1)

        self.lbl_img1=Label(self.root, image=self.img1)
        self.lbl_img1.place(x=200, y=250, width=570, height=400)

        self.show()

    def add(self):
            conn = sqlite3.connect(database=r'DB PROJECT.db')
            cur=conn.cursor()
            try:
                if self.var_name.get() == "" :
                   messagebox.showerror("Error", "Cateogory Name must be required", parent=self.root)
                else:
                    cur.execute("Select * from category where name=?",(self.var_name.get(),))
                    row = cur.fetchone()
                    if row != None:
                        messagebox.showerror("Error", "Category  already present, try different", parent=self.root)
                        self.clear()
                    else:
                        cur.execute("Insert into category (name) values(?)",(self.var_name.get(),))

                        cur.execute("SELECT cid FROM category ORDER BY cid")
                        rows = cur.fetchall()

                        for new_id, row in enumerate(rows, start=1):
                            cur.execute("UPDATE category SET cid = ? WHERE cid = ?", (new_id, row[0]))

                        conn.commit()
                        messagebox.showinfo('Success', 'Category Added Successfully', parent=self.root)
                        self.clear()
                        self.show()
                        conn.close()
            except Exception as e:
                    messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)

    def show(self):
        conn = sqlite3.connect(database=r'DB PROJECT.db')
        cur=conn.cursor()
        try:
            cur.execute("select * from category")
            rows = cur.fetchall()
            self.category_Table.delete(*self.category_Table.get_children())

            self.category_Table.column("name", anchor=CENTER)

            for row in rows:
                self.category_Table.insert('', END, values=row,)
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)

    def get_data(self, ev):
        f=self.category_Table.focus()
        content=(self.category_Table.item(f))
        row=content['values']
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    def delete(self):
        if self.var_cat_id.get() == "":
            messagebox.showerror("Error", "Please select a Category name", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Delete", "Do you really want to delete?", parent=self.root)
                if delete > 0:
                    conn = sqlite3.connect(database=r'DB PROJECT.db')
                    cur = conn.cursor()

                # Delete the selected category
                cur.execute("DELETE FROM category WHERE cid = ?", (self.var_cat_id.get(),))
                conn.commit()

                # Reassign IDs to form a continuous series
                cur.execute("SELECT cid FROM category ORDER BY cid")
                rows = cur.fetchall()

                for new_id, row in enumerate(rows, start=1):
                    cur.execute("UPDATE category SET cid = ? WHERE cid = ?", (new_id, row[0]))

                conn.commit()

                # Refresh the table view and clear inputs
                self.show()
                self.var_cat_id.set("")
                self.var_name.set("")
                messagebox.showinfo("Success", "Category deleted and IDs reassigned successfully.", parent=self.root)
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)
    def clear(self):
        self.var_name.set("")
        self.show()

if __name__ == "__main__":
# Initialize the root window
    root = Tk()
# Create an instance of the IMS class
    obj = category(root)
# Start the main loop
    root.mainloop()