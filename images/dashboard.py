from tkinter import *
from PIL import Image, ImageTk
from employee import employee
from supplier import supplier
from category import category
from product import product
from sales import sales
import sqlite3
from tkinter import messagebox
import os,sys
import time
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import pandas as pd
import joblib
import pickle
import sklearn

class Visualizations:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x800")
        self.root.title("Sales Visualizations")
        
        # Frame for buttons
        btn_frame = Frame(self.root, bd=2, relief=RIDGE, bg="#d5821e")
        btn_frame.place(x=0, y=0, width=1200, height=50)
        
        # Buttons for different visualizations
        Button(btn_frame, text="Monthly Quantity", command=lambda: self.show_visualization(1), 
               font=("times new roman", 12), bg="#b48a58", fg="black").place(x=10, y=5, width=200)
        Button(btn_frame, text="Monthly Net Pay", command=lambda: self.show_visualization(2), 
               font=("times new roman", 12), bg="#b48a58", fg="black").place(x=220, y=5, width=200)
        Button(btn_frame, text="Product-wise Quantity", command=lambda: self.show_visualization(3), 
               font=("times new roman", 12), bg="#b48a58", fg="black").place(x=430, y=5, width=200)
        Button(btn_frame, text="Product-wise Net Pay", command=lambda: self.show_visualization(4), 
               font=("times new roman", 12), bg="#b48a58", fg="black").place(x=640, y=5, width=200)
        Button(btn_frame, text="Top 10 Products", command=lambda: self.show_visualization(5), 
               font=("times new roman", 12), bg="#b48a58", fg="black").place(x=850, y=5, width=200)

        # Frame for plot
        self.plot_frame = Frame(self.root, bd=2, relief=RIDGE, bg="#d5821e")
        self.plot_frame.place(x=0, y=50, width=1200, height=750)
        
        # Initialize data
        self.initialize_data()
        
    def initialize_data(self):
        try:
            # Load the CSV file
            df = pd.read_csv('images/sales_data.csv')
            print(df.columns)
            
            if 'Date' not in df.columns:
               raise ValueError("The 'Date' column is missing from the dataset.")
        
            # Parse the 'Date' column
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)
            
            # Drop rows with invalid or missing dates
            df = df.dropna(subset=['Date'])

            # Add Month and Year columns for grouping
            df['Month'] = df['Date'].dt.month
            df['Year'] = df['Date'].dt.year

            # Group data by month
            self.monthly_data = df.groupby('Month').agg({'Quantity': 'sum', 'Net Pay': 'sum'}).reset_index()

            # Group data by product and month
            self.product_monthly_data = df.groupby(['Month', 'Product Name']).agg({'Quantity': 'sum', 'Net Pay': 'sum'}).reset_index()

            # Top products by net pay
            self.top_products = df.groupby('Product Name').agg({'Quantity': 'sum', 'Net Pay': 'sum'}).sort_values('Net Pay', ascending=False).head(10).reset_index()

           

            # Load test data
            self.X_test = pd.read_csv('images/X_test.csv')  # Replace with the actual test data path
            self.y_test = pd.read_csv('images/y_test.csv')  # Replace with actual test labels

            # Load the regression model
            with open('images/regression_model.pkl', 'rb') as model_file:
                self.reg = pickle.load(model_file)

            # Make predictions
            self.y_pred = self.reg.predict(self.X_test)


        except FileNotFoundError:
            messagebox.showerror("Error", "The file 'sales_data.csv' was not found.")
            self.monthly_data = pd.DataFrame({'Month': [], 'Quantity': [], 'Net Pay': []})
            self.product_monthly_data = pd.DataFrame({'Month': [], 'Product Name': [], 'Quantity': [], 'Net Pay': []})
            self.top_products = pd.DataFrame({'Product Name': [], 'Net Pay': []})

        except ValueError as ve:
            messagebox.showerror("Error", f"Data issue: {str(ve)}")
            self.monthly_data = pd.DataFrame({'Month': [], 'Quantity': [], 'Net Pay': []})
            self.product_monthly_data = pd.DataFrame({'Month': [], 'Product Name': [], 'Quantity': [], 'Net Pay': []})
            self.top_products = pd.DataFrame({'Product Name': [], 'Net Pay': []})

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            self.monthly_data = pd.DataFrame({'Month': [], 'Quantity': [], 'Net Pay': []})
            self.product_monthly_data = pd.DataFrame({'Month': [], 'Product Name': [], 'Quantity': [], 'Net Pay': []})
            self.top_products = pd.DataFrame({'Product Name': [], 'Net Pay': []})

    def clear_plot_frame(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

    def show_regression_plot(self):
        self.clear_plot_frame()

        # Prepare predicted and actual values for plotting
        y_pred_df = pd.DataFrame(self.y_pred, columns=self.y_test.columns, index=self.y_test.index)

        fig = Figure(figsize=(12, 7))
        ax = fig.add_subplot(111)

        # Regression plot for 'Net Pay' and 'Quantity'
        ax.scatter(self.y_test['Net Pay'], y_pred_df['Net Pay'], color='red', label='Predicted Net Pay', alpha=0.7)
        ax.plot(self.y_test['Net Pay'], self.y_test['Net Pay'], color='green', label='Perfect Fit', linestyle='--')
        ax.scatter(self.y_test['Quantity'], y_pred_df['Quantity'], color='blue', label='Predicted Quantity', alpha=0.7)
        
        # Labels, legend, and title
        ax.set_xlabel('Actual Values')
        ax.set_ylabel('Predicted Values')
        ax.set_title('Regression Plot: Actual vs. Predicted Values')
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=0, y=0, relwidth=1, height=660)

    def show_visualization(self, viz_num):
        self.clear_plot_frame()
        self.show_regression_plot()
        
        fig = Figure(figsize=(12, 7))
        ax = fig.add_subplot(111)
        
        if viz_num == 1:
            sns.barplot(ax=ax, x='Month', y='Quantity', data=self.monthly_data, palette='viridis')
            ax.set_title('Total Quantity Sold Per Month')
            ax.set_xlabel('Month')
            ax.set_ylabel('Total Quantity')
            
        elif viz_num == 2:
            sns.lineplot(ax=ax, x='Month', y='Net Pay', data=self.monthly_data, marker='o', color='orange')
            ax.set_title('Total Net Pay Generated Per Month')
            ax.set_xlabel('Month')
            ax.set_ylabel('Net Pay')
            
        elif viz_num == 3:
            sns.barplot(ax=ax, x='Month', y='Quantity', hue='Product Name', data=self.product_monthly_data)
            ax.set_title('Product-wise Quantity Sold Per Month')
            ax.set_xlabel('Month')
            ax.set_ylabel('Quantity Sold')
            
        elif viz_num == 4:
            sns.barplot(ax=ax, x='Month', y='Net Pay', hue='Product Name', 
                       data=self.product_monthly_data, palette='coolwarm')
            ax.set_title('Product-wise Net Pay Per Month')
            ax.set_xlabel('Month')
            ax.set_ylabel('Net Pay Generated')
            
        elif viz_num == 5:
            sns.barplot(ax=ax, y='Product Name', x='Net Pay', data=self.top_products, palette='magma')
            ax.set_title('Top 10 Products by Total Net Pay')
            ax.set_xlabel('Total Net Pay')
            ax.set_ylabel('Product Name')

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=0,y=0,relwidth=1,height=650)

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Online Retail Store Database System | Developed By Arish")
        
        self.bg_img = Image.open("images/leftmenu.png")
        self.bg_img = self.bg_img.resize((1366, 768), Image.Resampling.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)

        self.bg_label = Label(self.root, image=self.bg_img)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        img = Image.open("images/logo1111.png")
        resized_img = img.resize((300, 150), Image.Resampling.LANCZOS)
        self.icon_title = ImageTk.PhotoImage(resized_img)
        
        title = Label(self.root, text="Online Retail Store Database System", image=self.icon_title, compound=LEFT,
                     font=("times new roman", 45, "bold"), bd=10, relief=GROOVE, bg="#d5821e", fg="black")
        title.place(x=0, y=0, relwidth=1, height=150)

        btn_logout = Button(self.root, text="LOGOUT", command=self.logout,
                          font=("times new roman", 20, "bold"), bg="#b48a58", fg="black",
                          bd=5, cursor="hand2", relief=GROOVE)
        btn_logout.place(x=1170, y=600, width=150, height=50)

        self.label_clock = Label(self.root, 
                               text="Effortless Retail, Unmatched Management – Your Store's Success Starts Here!",
                               font=("times new roman", 17), bg="#d5821e", fg="black", relief=GROOVE)
        self.label_clock.place(x=0, y=150, relwidth=1, height=50)

        self.leftmenu_pic = Image.open("images/h3.png")
        self.leftmenu_pic = self.leftmenu_pic.resize((300, 200), Image.Resampling.LANCZOS)
        self.leftmenu_pic = ImageTk.PhotoImage(self.leftmenu_pic)
        LEFT_menu = Frame(self.root, bd=2, relief=GROOVE, bg="#d5821e")
        LEFT_menu.place(x=0, y=200, width=300, height=500)

        lbl_left_menu_logo = Label(LEFT_menu, image=self.leftmenu_pic, bg="#d5821e")
        lbl_left_menu_logo.pack(side=TOP, fill=X)

        btn_menu = Label(LEFT_menu, text="MENU", font=("times new roman", 14, "bold"),
                        bg="#d5821e", fg="black", bd=5, cursor="hand2", relief=GROOVE)
        btn_menu.pack(side=TOP, fill=X)

        btn_employee = Button(LEFT_menu, text="EMPLOYEES", command=self.employee,
                            font=("times new roman", 12), bg="#b48a58", fg="black",
                            bd=5, cursor="hand2", relief=GROOVE)
        btn_employee.pack(side=TOP, fill=X)

        btn_supplier = Button(LEFT_menu, text="SUPPLIERS", command=self.supplier,
                            font=("times new roman", 12), bg="#b48a58", fg="black",
                            bd=5, cursor="hand2", relief=GROOVE)
        btn_supplier.pack(side=TOP, fill=X)

        btn_categories = Button(LEFT_menu, text="CATEGORIES", command=self.category,
                              font=("times new roman", 12), bg="#b48a58", fg="black",
                              bd=5, cursor="hand2", relief=GROOVE)
        btn_categories.pack(side=TOP, fill=X)

        btn_products = Button(LEFT_menu, text="PRODUCTS", command=self.product,
                            font=("times new roman", 12), bg="#b48a58", fg="black",
                            bd=5, cursor="hand2", relief=GROOVE)
        btn_products.pack(side=TOP, fill=X)

        btn_sales = Button(LEFT_menu, text="SALES", command=self.sales,
                          font=("times new roman", 12), bg="#b48a58", fg="black",
                          bd=5, cursor="hand2", relief=GROOVE)
        btn_sales.pack(side=TOP, fill=X)

        # Add visualization button
        btn_visualizations = Button(LEFT_menu, text="SALES GRAPHS", command=self.show_visualizations,
                                  font=("times new roman", 12), bg="#b48a58", fg="black",
                                  bd=5, cursor="hand2", relief=GROOVE)
        btn_visualizations.pack(side=TOP, fill=X)


        self.lbl_employee = Label(self.root, text="TOTAL EMPLOYEES \n [ 0 ]",
                                bg="#d5821e", fg="black", font=("goudy old style", 20, "bold"),
                                bd=5, relief=RIDGE)
        self.lbl_employee.place(x=330, y=220, width=300, height=150)

        self.lbl_suplier = Label(self.root, text="TOTAL SUPPLIERS \n [ 0 ]",
                                bg="#d5821e", fg="black", font=("goudy old style", 20, "bold"),
                                bd=5, relief=RIDGE)
        self.lbl_suplier.place(x=690, y=220, width=300, height=150)

        self.lbl_category = Label(self.root, text="TOTAL CATEGORIES \n [ 0 ]",
                                bg="#d5821e", fg="black", font=("goudy old style", 20, "bold"),
                                bd=5, relief=RIDGE)
        self.lbl_category.place(x=1050, y=220, width=300, height=150)

        self.lbl_products = Label(self.root, text="TOTAL PRODUCTS \n [ 0 ]",
                                bg="#d5821e", fg="black", font=("goudy old style", 20, "bold"),
                                bd=5, relief=RIDGE)
        self.lbl_products.place(x=330, y=400, width=300, height=150)

        self.lbl_sales = Label(self.root, text="TOTAL SALES \n [ 0 ]",
                              bg="#d5821e", fg="black", font=("goudy old style", 20, "bold"),
                              bd=5, relief=RIDGE)
        self.lbl_sales.place(x=690, y=400, width=300, height=150)

        label_footer = Label(self.root,
                           text="© 2024 Arish. All Rights Reserved. | Online Retail Management System | Privacy Policy | Terms of Service | Contact Us: Arish@retailsystem.com",
                           font=("times new roman", 11), bg="#d5821e", fg="black", relief=GROOVE)
        label_footer.pack(side=BOTTOM, fill=X)

        self.update_content()

    def employee(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = employee(self.new_window)

    def supplier(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = supplier(self.new_window)

    def category(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = category(self.new_window)

    def product(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = product(self.new_window)
    
    def sales(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = sales(self.new_window)

    def show_visualizations(self):
        self.viz_window = Toplevel(self.root)
        self.viz_obj = Visualizations(self.viz_window)

    def update_content(self):
        conn = sqlite3.connect(database=r'DB PROJECT.db')
        cur = conn.cursor()
        try:
            cur.execute("select * from product")
            product = cur.fetchall()
            self.lbl_products.config(text=f"TOTAL PRODUCTS \n [ {str(len(product))} ]")

            cur.execute("select * from supplier")
            supplier = cur.fetchall()
            self.lbl_suplier.config(text=f"TOTAL SUPPLIERS \n [ {str(len(supplier))} ]")

            cur.execute("select * from category")
            category = cur.fetchall()
            self.lbl_category.config(text=f"TOTAL CATEGORIES \n [ {str(len(category))} ]")

            cur.execute("select * from employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f"TOTAL EMPLOYEES \n [ {str(len(employee))} ]")

            self.lbl_sales.config(text=f"TOTAL SALES \n [ {str(len(os.listdir('images/bill')))} ]")

            conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)

    def logout(self):
        self.root.destroy()
        try:
            os.system(f"{sys.executable} images/login.py")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()