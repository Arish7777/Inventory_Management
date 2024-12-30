from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
from tkinter import Spinbox
import sqlite3

class product:
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
        self.search_by = StringVar()
        self.search_txt = StringVar()

        self.var_cat=StringVar(value="Select")
        self.var_sup=StringVar(value="Select")
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()
        self.var_pid=StringVar()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar(value="Active")

        #--All Frame

        product_frame1 = Frame(self.root, bd=4, relief=RIDGE, bg="#d5821e")
        product_frame1.place(x=20, y=80, width=505, height=600)

        product_frame = Frame(self.root, bd=4, relief=RIDGE, bg="#d5821e")
        product_frame.place(x=20, y=20, width=505, height=50)

        product_title = Label(product_frame, text="Products Details", font=("goudy old style", 25, "bold"), bg="#d5821e")
        product_title.pack(side=TOP, fill=X)

        lbl_category = Label(product_frame1, text="Category", font=("goudy old style", 20, "bold"), bg="#d5821e")
        lbl_category.place(x=10, y=20,height=40)

        lbl_supplier = Label(product_frame1, text="Supplier", font=("goudy old style", 20, "bold"), bg="#d5821e")
        lbl_supplier.place(x=10, y=100,height=40)

        lbl_product = Label(product_frame1, text="Product", font=("goudy old style", 20, "bold"), bg="#d5821e")
        lbl_product.place(x=10, y=180,height=40)

        lbl_price = Label(product_frame1, text="Price", font=("goudy old style", 20, "bold"), bg="#d5821e")
        lbl_price.place(x=10, y=260,height=40)

        lbl_quantity = Label(product_frame1, text="Quantity", font=("goudy old style", 20, "bold"), bg="#d5821e")
        lbl_quantity.place(x=10, y=340,height=40)

        lbl_status = Label(product_frame1, text="Status", font=("goudy old style", 20, "bold"), bg="#d5821e")
        lbl_status.place(x=10, y=420,height=40)

        #Entry
        cmd_cat = ttk.Combobox(product_frame1, textvariable=self.var_cat,values=self.cat_list, justify="center",font=("goudy old style", 20), state="readonly")
        cmd_cat.place(x=130, y=20,height=35,width=260)
        cmd_cat.current(0)

        cmd_sup = ttk.Combobox(product_frame1, textvariable=self.var_sup,values=self.sup_list, justify="center",font=("goudy old style", 20), state="readonly")
        cmd_sup.place(x=130, y=100,height=35,width=260)
        cmd_sup.current(0)

        txt_name = Entry(product_frame1, textvariable=self.var_name, font=("goudy old style", 20, "bold"), bg="white")
        txt_name.place(x=130, y=180, height=35, width=260)

        txt_price = Entry(product_frame1, textvariable=self.var_price, font=("goudy old style", 20, "bold"), bg="white")
        txt_price.place(x=130, y=260, height=35, width=260)

        txt_qty = Spinbox(
            product_frame1,
            from_=0,
            to=1000000,
            increment=1,
            font=("goudy old style", 20, "bold"),
            textvariable=self.var_qty,  # Ensure this is bound to self.var_qty
            bg="white",
            fg="black",
            width=15,
        )
        txt_qty.place(x=130, y=340, height=35, width=260)


        # Set default value (optional)
        txt_qty.delete(0, "end")  # Clear the initial value
        txt_qty.insert(0, 1)  # Default to 1

        cmd_status = ttk.Combobox(product_frame1, textvariable=self.var_status,values=("Active","Inactive"), justify="center",font=("goudy old style", 20), state="readonly")
        cmd_status.place(x=130, y=420,height=35,width=260)
        cmd_status.current(0)

        #--buttons
        btn_add = Button(product_frame1, text="Save", command=self.add,font=("times new roman", 12, "bold"), bg="#b48a58", fg="black", cursor="hand2").place(x=10, y=500, width=110, height=40)
        btn_update = Button(product_frame1, text="Update",command=self.update, font=("times new roman", 12, "bold"), bg="#b48a58", fg="black", cursor="hand2").place(x=130, y=500, width=110, height=40)
        btn_delete = Button(product_frame1, text="Delete",command=self.delete, font=("times new roman", 12, "bold"), bg="#b48a58", fg="black", cursor="hand2").place(x=250, y=500, width=110, height=40)
        btn_clear = Button(product_frame1, text="Clear",command=self.clear ,font=("times new roman", 12, "bold"), bg="#b48a58", fg="black", cursor="hand2").place(x=370, y=500, width=110, height=40)

        #--SearchFrame
        SearchFrame = LabelFrame(self.root,text="Search Employee", font=("times new roman", 12, "bold"), bg="#d5821e" ,bd=2, relief=RIDGE)
        SearchFrame.place(x=540,y=10,width=800,height=80)

        #--options
        cmd_search=ttk.Combobox(SearchFrame,textvariable=self.search_by,values=("Select","Category","Supplier","Name"),font=("goudy old style", 12, "bold"), state="readonly", justify=CENTER)
        cmd_search.place(x=10, y=10, width=150, height=30)
        cmd_search.current(0)

        #--search
        txt_search = Entry(SearchFrame,textvariable=self.search_txt, font=("goudy old style", 15), bg="lightyellow")
        txt_search.place(x=170, y=10, width=500, height=30)

        #--search button
        search_btn = Button(SearchFrame, text="Search",command=self.search,font=("goudy old style", 12, "bold"), bg="#b48a58", fg="black", cursor="hand2")
        search_btn.place(x=680, y=10, width=100, height=30)

        #--Products Details
        p_frame = Frame(self.root, bd=3, relief=RIDGE,bg="lightyellow")
        p_frame.place(x=540, y=100, width=800, height=580)

        scrolly = Scrollbar(p_frame, orient=VERTICAL)
        scrollx = Scrollbar(p_frame, orient=HORIZONTAL)
        self.product_Table = ttk.Treeview(p_frame, columns=("pid", "Category", "Supplier", "name", "price", "quantity", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)
        self.product_Table.heading("pid", text="Product ID")
        self.product_Table.heading("Category", text="Category")
        self.product_Table.heading("Supplier", text="Supplier")
        self.product_Table.heading("name", text="Product")
        self.product_Table.heading("price", text="Price")
        self.product_Table.heading("quantity", text="Quantity")
        self.product_Table.heading("status", text="Status")
        self.product_Table["show"] = "headings"
        
        self.product_Table.column("pid", width=100)
        self.product_Table.column("Category", width=100)
        self.product_Table.column("Supplier", width=100)
        self.product_Table.column("name", width=100)
        self.product_Table.column("price", width=100)
        self.product_Table.column("quantity", width=100)
        self.product_Table.column("status", width=100)
        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        conn = sqlite3.connect(database=r'DB PROJECT.db')
        cur=conn.cursor()
        try:
            cur.execute("select name from category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            cur.execute("select name from supplier")
            sup=cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)

    def add(self):
        conn = sqlite3.connect(database=r'DB PROJECT.db')
        cur = conn.cursor()
        try:
            # Validation
            if self.var_cat.get().strip() in ["Select", ""] or self.var_sup.get().strip() in ["Select", ""] or self.var_name.get().strip() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("Select * from product where name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Product already present, try a different name", parent=self.root)
                else:
                    cur.execute(
                        "Insert into product (Category, Supplier, name, price, quantity, status) values(?,?,?,?,?,?)",
                        (
                            self.var_cat.get(),
                            self.var_sup.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get(),
                        ),
                    )
                    cur.execute("SELECT pid FROM product ORDER BY pid")
                    rows = cur.fetchall()

                    for new_id, row in enumerate(rows, start=1):
                        cur.execute("UPDATE product SET pid = ? WHERE pid = ?", (new_id, row[0]))
                    conn.commit()
                    messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
                    self.show()
                    conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)

    
    def show(self):
        conn = sqlite3.connect(database=r'DB PROJECT.db')
        cur=conn.cursor()
        try:
            cur.execute("select * from product")
            rows = cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows: 
                self.product_Table.insert('', END, values=row)
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)
    
    def get_data(self, ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])

    def update(self):
        conn=sqlite3.connect(database=r'DB PROJECT.db')
        cur=conn.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please select product from the list", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Product ID", parent=self.root)
                else:
                    cur.execute("Update product set Category=?, Supplier=?, name=?, price=?, quantity=?, status=? where pid=?",(
                            self.var_cat.get(),
                            self.var_sup.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get(),
                            self.var_pid.get(),
                    ))
                    conn.commit()
                    messagebox.showinfo('Success', 'Product Details Updated Successfully', parent=self.root)
                    self.show()
                    conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)
    
    def delete(self):
        if self.var_pid.get() == "":
            messagebox.showerror("Error", "Select product from the list", parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Delete", "Do you really want to delete?", parent=self.root)
                if delete>0:
                    conn=sqlite3.connect(database=r'DB PROJECT.db')
                    cur=conn.cursor()
                    sql="delete from product where pid=?"
                    cur.execute(sql, (self.var_pid.get(),))
                
                    cur.execute("SELECT pid FROM product ORDER BY pid")
                    rows = cur.fetchall()

                    for new_id, row in enumerate(rows, start=1):
                        cur.execute("UPDATE product SET pid = ? WHERE pid = ?", (new_id, row[0]))
                conn.commit()
                messagebox.showinfo("Success", "Product Deleted Successfully", parent=self.root)
                self.show()
                self.clear()
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)
   

    def clear(self):
        self.var_pid.set("")
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        
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
                cur.execute("select * from product where "+self.search_by.get()+" LIKE '%"+self.search_txt.get()+"%'")
                rows = cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No Data Found !!!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)


if __name__ == "__main__":
# Initialize the root window
    root = Tk()
# Create an instance of the IMS class
    obj = product(root)
# Start the main loop
    root.mainloop()