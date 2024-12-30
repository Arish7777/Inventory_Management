from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox,END
import os
import sqlite3

class sales:
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

        self.bill_list=[]

        #variables
        self.invoice_no = StringVar()

        sales_frame1 = Frame(self.root, bd=4, relief=RIDGE, bg="#d5821e")
        sales_frame1.place(x=180, y=80, width=1000, height=600)

        sales_frame = Frame(self.root, bd=4, relief=RIDGE, bg="#d5821e")
        sales_frame.place(x=180, y=20, width=1000, height=50)
        
        #title
        product_title = Label(sales_frame, text="View Customer Bills", font=("goudy old style", 25, "bold"), bg="#d5821e")
        product_title.pack(side=TOP, fill=X)

        #Invoice
        lbl_invoice = Label(sales_frame1, text="Invoice No.", font=("times new roman", 20, "bold"), bg="#d5821e")
        lbl_invoice.place(x=10, y=20, width=200, height=50)

        txt_invoice = Entry(sales_frame1, textvariable=self.invoice_no, font=("times new roman", 20, "bold"),bg="white")
        txt_invoice.place(x=200, y=28,height=30, width=250)

        #Button
        search_btn = Button(sales_frame1, text="Search",command=self.search,font=("goudy old style", 15, "bold"), bg="#b48a58", fg="black", cursor="hand2")
        search_btn.place(x=480, y=28, width=100, height=30)

        clear_btn = Button(sales_frame1, text="Clear",command=self.clear,font=("goudy old style", 15, "bold"), bg="#b48a58", fg="black", cursor="hand2")
        clear_btn.place(x=600, y=28, width=100, height=30)

        #Frame
        s_frame=Frame(sales_frame1,bd=4,relief=RIDGE,bg="white")
        s_frame.place(x=40,y=80,width=270,height=500)

        scrolly=Scrollbar(s_frame,orient=VERTICAL)
        self.sales_list=Listbox(s_frame,font=("goudy old style", 15, "bold"),bg="white",fg="black",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.sales_list.yview)
        self.sales_list.pack(fill=BOTH,expand=1)
        self.sales_list.bind("<ButtonRelease-1>",self.get_data)

        #BillArea
        bill_frame=Frame(sales_frame1,bd=4,relief=RIDGE,bg="white")
        bill_frame.place(x=350,y=80,width=600,height=500)

        product_title2 = Label(bill_frame, text="Customer Bill Area", font=("goudy old style", 25, "bold"), bg="#d5821e")
        product_title2.pack(side=TOP, fill=X)

        scrolly2=Scrollbar(bill_frame,orient=VERTICAL)
        self.bill_area=Text(bill_frame,font=("goudy old style", 17, "bold"),bg="white",fg="black",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.sales_list.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

    
        self.show()

    def show(self):
        del self.bill_list[:]
        bill_path = r"C:\\Users\\Syscom\\OneDrive - FAST National University\\Desktop\\DB PROJECT\\images\\bill"
        self.sales_list.delete(0,END)
        if not os.path.exists(bill_path):
            os.makedirs(bill_path)
        for i in os.listdir(bill_path):
            if i.split(".")[-1]=="txt":
                self.sales_list.insert(END,i)
                self.bill_list.append(i.split(".")[0])

    def get_data(self,ev):
        index_=self.sales_list.curselection()
        file_name=self.sales_list.get(index_)
        file_path=f"C:\\Users\\Syscom\\OneDrive - FAST National University\\Desktop\\DB PROJECT\\images\\bill\\{file_name}"
        with open(file_path,"r") as f:
            self.bill_area.delete("1.0",END)
            for d in f.readlines():
                self.bill_area.insert(END,d)
            f.close()

    def search(self):
        if self.invoice_no.get()=="":
            messagebox.showerror("Error","Invoice No. should be required",parent=self.root)
        else:
            if self.invoice_no.get() in self.bill_list:
                file_path=f"C:\\Users\\Syscom\\OneDrive - FAST National University\\Desktop\\DB PROJECT\\images\\bill\\{self.invoice_no.get()}.txt"
                with open(file_path,"r") as f:
                    self.bill_area.delete("1.0",END)
                    for d in f.readlines():
                        self.bill_area.insert(END,d)
                    f.close()
            else:
                messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
    
    def clear(self):
        self.show()
        self.invoice_no.set("")
        self.bill_area.delete("1.0",END)

if __name__ == "__main__":
# Initialize the root window
    root = Tk()
# Create an instance of the IMS class
    obj = sales(root)
# Start the main loop
    root.mainloop()