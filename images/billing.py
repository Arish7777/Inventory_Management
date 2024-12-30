from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import sys
import tempfile
import csv
from datetime import datetime
from tkinter import messagebox
class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Online Retail Store Database System | Developed By Arish")
        self.cart_list=[]
        
        self.bg_img = Image.open("images/leftmenu.png")  # Replace with the correct image path
        self.bg_img = self.bg_img.resize((1366, 768), Image.Resampling.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)

        self.bg_label = Label(self.root, image=self.bg_img)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # -- Title with Image (Resize the logo)
        img = Image.open("images/logo1111.png")
        resized_img = img.resize((300, 150), Image.Resampling.LANCZOS)  # Resize image to 100x100 pixels
        self.icon_title = ImageTk.PhotoImage(resized_img)  # Use resized image # Place the title at the top

        #--clock
        self.label_clock=Label(self.root, text="Effortless Retail, Unmatched Management – Your Store's Success Starts Here!", font=("times new roman", 17), bg="#d5821e", fg="black",relief=GROOVE)
        self.label_clock.place(x=0, y=0, relwidth=1, height=80) 

         # --logout button
        btn_logout = Button(self.root, text="LOGOUT",command=self.logout, font=("times new roman", 20, "bold",),bg="#b48a58",fg="black", bd=5,cursor="hand2", relief=GROOVE).place(x=1100, y=14, width=150, height=50)

        #===Product Frame====
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="#d5821e")
        ProductFrame1.place(x=6,y=110,width=410,height=530)

        pTitle=Label(ProductFrame1,text="All Products",font=("goudy old style",20,"bold"),bg="#d5821e",fg="black").pack(side=TOP,fill=X)

        #===Product Search Frame=============
        self.var_search=StringVar()
        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="#d5821e")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(ProductFrame2,text="Search Product | By Name ",font=("times new roman",15,"bold"),bg="#d5821e",fg="black").place(x=2,y=5)
        
        lbl_search=Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="#d5821e",fg="black").place(x=5,y=45)
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=130,y=47,width=150,height=22)
        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("goudy old style",15),bg="#b48a58",fg="black",cursor="hand2").place(x=285,y=45,width=100,height=25)
        btn_show_all=Button(ProductFrame2,text="Show All",command=self.show,font=("goudy old style",15),bg="#b48a58",fg="black",cursor="hand2").place(x=285,y=10,width=100,height=25)

        #===Product Details Frame==============
        ProductFrame3=Frame(ProductFrame1,bd=2,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=355)

        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)

        self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        self.product_Table.heading("pid",text="PID")
        self.product_Table.heading("name",text="Name")
        self.product_Table.heading("price",text="Price")
        self.product_Table.heading("qty",text="QTY")
        self.product_Table.heading("status",text="Status")
        self.product_Table["show"]="headings"
        self.product_Table.column("pid",width=40)
        self.product_Table.column("name",width=100)
        self.product_Table.column("price",width=90)
        self.product_Table.column("qty",width=40)
        self.product_Table.column("status",width=90)
        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)

        lbl_note=Label(ProductFrame1,text="Note: Enter 0 quantity to remove product from the cart",font=("goudy old style",12,"bold"),anchor='w',bg="#d5821e",fg="black",).pack(side=BOTTOM,fill=X)


        #=====Customer Frame================
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="#d5821e")
        CustomerFrame.place(x=420,y=110,width=530,height=70)

        cTitle=Label(CustomerFrame,text="Customer Details",font=("goudy old style",20,"bold"),bg="#d5821e").pack(side=TOP,fill=X)
        lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15),bg="#d5821e").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg="lightyellow").place(x=80,y=35,width=180)

        lbl_contact=Label(CustomerFrame,text="Contact No.",font=("times new roman",15),bg="#d5821e").place(x=270,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="lightyellow").place(x=380,y=35,width=140)

        #===Cal Cart Frame============
        Cal_Cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="#d5821e")
        Cal_Cart_Frame.place(x=420,y=190,width=530,height=400)

        #===Calculator Frame============
        self.var_cal_input=StringVar()

        Cal_Frame=Frame(Cal_Cart_Frame,bd=9,relief=RIDGE,bg="#d5821e")
        Cal_Frame.place(x=5,y=10,width=268,height=340)

        txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=('arial',15,'bold'),width=22,bd=5,relief=GROOVE,state='readonly',justify=RIGHT)
        txt_cal_input.grid(row=0,columnspan=4)

        btn_7=Button(Cal_Frame,text='7',font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text='8',font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text='9',font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=3)

        btn_4=Button(Cal_Frame,text='4',font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text='5',font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text='6',font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=3)

        btn_1=Button(Cal_Frame,text='1',font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=0)
        btn_2=Button(Cal_Frame,text='2',font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text='3',font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text='*',font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=3)

        btn_0=Button(Cal_Frame,text='0',font=('arial',15,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=0)
        btn_c=Button(Cal_Frame,text='c',font=('arial',15,'bold'),command=self.clear_cal,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,text='=',font=('arial',15,'bold'),command=self.perform_cal,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text='/',font=('arial',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=3)


        #===Cart Frame============
        cart_Frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        cart_Frame.place(x=280,y=8,width=245,height=342)
        self.cartTitle=Label(cart_Frame,text="Cart \t Total Product:[0]",font=("goudy old style",15,"bold"),bg="#d5821e")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly=Scrollbar(cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(cart_Frame,orient=HORIZONTAL)

        self.CartTable=ttk.Treeview(cart_Frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("pid",text="PID")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price",text="Price")
        self.CartTable.heading("qty",text="QTY")
        self.CartTable["show"]="headings"
        self.CartTable.column("pid",width=40)
        self.CartTable.column("name",width=90)
        self.CartTable.column("price",width=90)
        self.CartTable.column("qty",width=40)
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        #===Add Cart Widgets Frame============
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()

        Add_CartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="#d5821e")
        Add_CartWidgetsFrame.place(x=420,y=550,width=530,height=90)

        lbl_p_name=Label(Add_CartWidgetsFrame,text="Product Name",font=("times new roman",15),bg="#d5821e").place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=5,y=30,width=190,height=22)

        lbl_p_price=Label(Add_CartWidgetsFrame,text="Price Per Qty",font=("times new roman",15),bg="#d5821e").place(x=230,y=5)
        txt_p_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=230,y=30,width=150,height=22)

        lbl_p_qty=Label(Add_CartWidgetsFrame,text="Quantity",font=("times new roman",15),bg="#d5821e").place(x=390,y=5)
        txt_p_qty=Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow",).place(x=390,y=30,width=120,height=22)


        self.lbl_inStock=Label(Add_CartWidgetsFrame,text="In Stock",font=("times new roman",13),bg="#d5821e")
        self.lbl_inStock.place(x=5,y=60)

        btn_clear_cart=Button(Add_CartWidgetsFrame,text="Clear",command=self.clear_cart,font=("times new roman",15,"bold"),bg="#b48a58",cursor="hand2").place(x=180,y=60,width=150,height=23)
        btn_add_cart=Button(Add_CartWidgetsFrame,text="Add | Update Cart",command=self.add_update_cart,font=("times new roman",15,"bold"),bg="#b48a58",cursor="hand2").place(x=340,y=60,width=180,height=23)


        #===============billing area======================
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billFrame.place(x=953,y=110,width=400,height=410)

        BTitle=Label(billFrame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="#d5821e",fg="black").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #===============billing buttons==================
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg='#d5821e')
        billMenuFrame.place(x=953,y=520,width=400,height=120)

        self.lbl_amnt=Label(billMenuFrame,text="Bill Amount\n[0]",font=("goudy old style",13,"bold"),bg="#b48a58",fg="black")
        self.lbl_amnt.place(x=2,y=5,width=120,height=60)

        self.lbl_discount=Label(billMenuFrame,text="Discount\n[5%]",font=("goudy old style",13,"bold"),bg="#b48a58",fg="black")
        self.lbl_discount.place(x=130,y=5,width=120,height=60)

        self.lbl_net_pay=Label(billMenuFrame,text="Net Pay\n[0]",font=("goudy old style",13,"bold"),bg="#b48a58",fg="black")
        self.lbl_net_pay.place(x=258,y=5,width=130,height=60)

        btn_print=Button(billMenuFrame,text="Print",command=self.print_bill,cursor="hand2",font=("goudy old style",13,"bold"),bg="#b48a58",fg="black")
        btn_print.place(x=2,y=70,width=120,height=40)

        btn_clear_all=Button(billMenuFrame,text="Clear All",command=self.clear_all,cursor="hand2",font=("goudy old style",13,"bold"),bg="#b48a58",fg="black")
        btn_clear_all.place(x=130,y=70,width=120,height=40)

        btn_generate=Button(billMenuFrame,text="Generate Bill",command=self.generate_bill,cursor="hand2",font=("goudy old style",13,"bold"),bg="#b48a58",fg="black")
        btn_generate.place(x=258,y=70,width=130,height=40)

        #Footer
        footer=Label(self.root,text="Online Retail Store Database System | Developed By Arish",font=("goudy old style",12),bg="#d5821e",fg="black").pack(side=BOTTOM,fill=X)
        self.show()
        # self.bill_top()
        
# ================All Functions==========================
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)
    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))


    def show(self):
        conn = sqlite3.connect(database=r'DB PROJECT.db')
        cur=conn.cursor()
        try:
            cur.execute("select pid,name,price,quantity,status from product where status='Active'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def search(self):
        conn = sqlite3.connect(database=r'DB PROJECT.db')
        cur=conn.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select pid,name,price,quantity,status from product where name LIKE '%"+self.var_search.get()+"%' and status='Active'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values'] #pid,name,price,qty,status
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values'] #pid,name,price,qty,status
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])
        

    def add_update_cart(self):
    # Check if the product is selected
            if self.var_pid.get() == '':
                messagebox.showerror('Error', "Please select a product from the list", parent=self.root)
            elif self.var_qty.get() == '':
                messagebox.showerror('Error', "Quantity is required", parent=self.root)
            elif int(self.var_qty.get()) > int(self.var_stock.get()):
                messagebox.showerror('Error', "Invalid quantity. Quantity exceeds stock.", parent=self.root)
            else:
                # Calculate the total price for the quantity
                price_cal = float(self.var_qty.get()) * float(self.var_price.get())
                cart_data = [
                    self.var_pid.get(),    # Product ID
                    self.var_pname.get(),  # Product Name
                    price_cal,             # Total Price
                    self.var_qty.get(),    # Quantity
                    self.var_stock.get()   # Stock
                ]

                # Check if the product is already in the cart
                present = False
                index_ = None
                for idx, row in enumerate(self.cart_list):
                    if self.var_pid.get() == row[0]:  # If Product ID matches
                        present = True
                        index_ = idx
                        break

                if present:
                    # Ask user to confirm update or removal
                    op = messagebox.askyesno('Confirm', 
                                              "Product already present.\nDo you want to Update/Remove from the cart?",
                                              parent=self.root)
                    if op:
                        # If quantity is 0, remove the product from the cart
                        if self.var_qty.get() == "0":
                            self.cart_list.pop(index_)
                            messagebox.showinfo('Removed', 'Product removed from the cart.', parent=self.root)
                        else:
                            # Update quantity and price
                            #self.cart_list[index_][2] = price_cal  # Update price
                            self.cart_list[index_][3] = self.var_qty.get()  # Update quantity
                            messagebox.showinfo('Updated', 'Product updated in the cart.', parent=self.root)
                else:
                    # Add new product to the cart
                    self.cart_list.append(cart_data)
                    messagebox.showinfo('Added', 'Product added to the cart.', parent=self.root)

                # Refresh the cart display
                self.show_cart()

                self.bill_updates()


    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f'Bill Amnt\n{str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'Net Pay\n{str(self.net_pay)}')
        self.cartTitle.config(text=f"Cart \t Total Product:[{str(len(self.cart_list))}]")


    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def generate_bill(self): 
        if self.var_cname.get() == '' or self.var_contact.get() == '':
            messagebox.showerror("Error", f"Customer details are required", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", f"Please add product to the cart!!!", parent=self.root)
        else:
            # ===Bill Top====
            self.bill_top()
            # ===Bill Middle====
            self.bill_middle()
            # ===Bill Bottom====
            self.bill_bottom()


            # Save bill data to sales_data.csv
            try:
                with open(f'images/bill/{str(self.invoice)}.txt', 'w') as fp:
                    fp.write(self.txt_bill_area.get('1.0', END))
                messagebox.showinfo('Saved', "Bill has been generated/Saved in Backend", parent=self.root)
                self.chk_print = 1

                # Save bill data to sales_data.csv
                with open('sales_data.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)

                    # Write rows for each product in the cart
                    for item in self.cart_list:
                        # Extract data: Assuming structure is [PID, Product Name, Price, Quantity, Stock]
                        product_name = item[1]  # Product Name
                        quantity = int(item[3])  # Quantity
                        net_pay = float(item[2]) * quantity  # Net Pay = Price * Quantity
                        date = datetime.now().strftime('%d/%m/%Y')  # Current Date

                        # Write to CSV
                        writer.writerow([product_name, date, quantity, net_pay])

            except Exception as e:
                messagebox.showerror("Error", f"Error saving to CSV: {str(e)}", parent=self.root)


            
    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
            TRADER'S CART
Phone No. +92355******* , Karachi-750760
{str("="*46)}
Customer Name: {self.var_cname.get()}
Ph no. :{self.var_contact.get()}
Bill No. {str(self.invoice)}  Date: {str(time.strftime("%d/%m/%Y"))}
{str("="*46)}
Product Name         QTY          Price
{str("="*46)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)
        
    def bill_bottom(self):
        bill_bottom_temp = f'''
{str("="*46)}
 Bill Amount     Rs.{self.bill_amnt:,.2f}
 Discount        Rs.{self.discount:,.2f}
 Net Pay         Rs.{self.net_pay:,.2f}
 Bill Amount     Rs.{self.bill_amnt:.2f}
 Discount        Rs.{self.discount:.2f}
 Net Pay         Rs.{self.net_pay:.2f}
{str("="*46)}\n
    '''
        self.txt_bill_area.insert(END, bill_bottom_temp)


    def bill_middle(self):
        conn = sqlite3.connect(database=r'DB PROJECT.db')
        cur = conn.cursor()
        try:
            for row in self.cart_list:
                pid = row[0]
                name = row[1]
                qty = int(row[4]) - int(row[3])  # Calculate updated quantity

            # Update status based on stock
                status = "Inactive" if qty == 0 else "Active"

            # Calculate price
                price = float(row[2]) * int(row[3])
                price_str = f"{price:.2f}"  # Format price to two decimal places

            # Insert product details into the bill area
                self.txt_bill_area.insert(END, f"\n{name:<20}{row[3]:<5}Rs.{price_str}")

            # Update quantity and status in the database
                cur.execute(
                "UPDATE product SET quantity=?, status=? WHERE pid=?",
                (qty, status, pid)
                )
                conn.commit()

            conn.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    
    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set('')
        
    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart \t Total Product:[0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()

    def print_bill(self):
        if  self.chk_print==1:
            messagebox.showinfo('Print',"Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('Print',"Please generate bill to pint the receipt",parent=self.root)
            
    def logout(self):
        self.root.destroy()  # Destroy the current window
        try:
            os.system(f"{sys.executable} images/login.py")  # Use the same Python interpreter
        except Exception as e:
            print(f"Error: {e}")

if __name__=="__main__":
    root=Tk()
    obj=BillClass(root)
    root.mainloop()