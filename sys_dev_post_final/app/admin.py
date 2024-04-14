import tkinter as tk
from tkinter import ttk, messagebox , simpledialog
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime
import time
from tkcalendar import DateEntry
import smtplib
from email.mime.text import MIMEText
from ttkthemes import ThemedStyle
import threading


localtime = time.asctime(time.localtime(time.time()))
current_datetime = datetime.now()
DB_FILE = 'data/data.db'
branches = {
    'London': ['South', 'Central'],
    'Bristol': ['Cabot', 'Cribbs Causeway'],
    
}
tables = {branch: [f"Table {i}" for i in range(1, 31)] for branch in sum(branches.values(), [])}

THRESHOLD = 100

#the functions: 
#update menu page functions :

def add_menu_item(name, price, category, description, allergy, availability):
    # Add item to the menu in the database
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS menu (name TEXT, price REAL, category TEXT, description TEXT, allergy TEXT , availability TEXT)")
    cursor.execute("INSERT INTO menu VALUES (?, ?, ?, ?, ?, ?)", (name, price, category, description, allergy, availability))

    connection.commit()
    connection.close()

def update_menu_item(name, price):
    # Update item in the menu in the database
    try: 
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
 
        cursor.execute("CREATE TABLE IF NOT EXISTS menu (name TEXT, price REAL, category TEXT, description TEXT, allergy TEXT, availability TEXT)")
        cursor.execute("UPDATE menu SET price=?  WHERE name=?", (price, name))

        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Error: {e}")

def update_menu_stat(name, availability):
    # Update item in the menu in the database
    try: 
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        
        if  availability == 'no':
            cursor.execute("CREATE TABLE IF NOT EXISTS menu (name TEXT, price REAL, category TEXT, description TEXT, allergy TEXT, availability TEXT)")
            cursor.execute("UPDATE menu SET availability = ? WHERE name = ?", ('no', name))
        elif  availability == 'yes':
            cursor.execute("CREATE TABLE IF NOT EXISTS menu (name TEXT, price REAL, category TEXT, description TEXT, allergy TEXT, availability TEXT)")
            cursor.execute("UPDATE menu SET availability = ? WHERE name = ?", ('yes', name))

        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Error: {e}")

def delete_menu_item(name):
    # Delete item from the menu in the database
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS menu (name TEXT, price REAL, category TEXT, description TEXT, allergy TEXT, availability TEXT)")
        cursor.execute("DELETE FROM menu WHERE name=?", (name))

        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Error: {e}")

#order page functions :
def get_menu_filtered():
    # Retrieve menu from the database
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS menu (name TEXT, price REAL, category TEXT, description TEXT, allergy TEXT, availability TEXT)")
        cursor.execute("SELECT * FROM menu")
        menu = cursor.fetchall()

        # Filter out items with availability 'not available'
        menu_without_not_available = [item for item in menu if item[5].lower() == 'yes']

        connection.close()
        return menu_without_not_available
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_menu():
    
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS menu (name TEXT, price REAL, category TEXT, description TEXT, allergy TEXT, availability TEXT)")
        cursor.execute("SELECT * FROM menu")
        menu = cursor.fetchall()

        connection.close()
        return menu
    except Exception as e:
        print(f"Error: {e}")
        return []

def save_payment(total, date , time):
    # Save payment to the database
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS payments ( date TEXT, time TEXT, total REAL )")
        cursor.execute("INSERT INTO payments VALUES (?, ?, ?)", (date, time, total))

        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Error: {e}")

def save_into_orders(self, order_date, order_time, total):
    
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    for item, details in self.selected_items.items():
            quantity = details["quantity_var"].get()
            if quantity > 0:
                print(f"Preparing to insert: Date: {order_date}, Time: {order_time}, Total: {total}, Item: {item}, Quantity: {quantity}")
                cursor.execute("CREATE TABLE IF NOT EXISTS orders ( order_id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, time TEXT, total REAL, item TEXT, quantity TEXT )")  # Debugging print
                cursor.execute("INSERT INTO payments VALUES (?, ?, ?, ?, ?)", (order_date, order_time, total, item, quantity))                        
    connection.commit()  
    connection.close()

#payments history functions :
def get_payment_history():
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS payments (date TEXT, time TEXT, total REAL)")
        cursor.execute("SELECT * FROM payments ORDER BY date DESC")
        payment_history = cursor.fetchall()

        connection.close()
        return payment_history
    except Exception as e:
        print(f"Error: {e}")
        return []
#check reservations functions :
def get_reservations():
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS reservations (name TEXT, city TEXT, branch TEXT, `table` TEXT, date TEXT, time TEXT)")
        cursor.execute("SELECT * FROM reservations")
        reservations = cursor.fetchall()
        connection.close()
        return reservations
    except Exception as e:
        print(f"Error: {e}")
        return []

def delete_reservation(reservation):
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM reservations WHERE name=? AND date=? AND time=?", reservation)

        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Error: {e}")

def update_reservation(name, date, old_time, new_time):
    # Update reservation in the database
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        # Check if the reservation exists
        cursor.execute("SELECT * FROM reservations WHERE name=? AND date=? AND time=?", (name, date, old_time))
        existing_reservation = cursor.fetchone()

        if existing_reservation:
            # Update the time for the existing reservation
            cursor.execute("UPDATE reservations SET time=? WHERE name=? AND date=? AND time=?", (new_time, name, date, old_time))
            connection.commit()
            messagebox.showinfo("Reservation Updated", f"Reservation for {name} on {date} updated to {new_time}.")
        else:
            messagebox.showwarning("Reservation Not Found", f"No reservation found for {name} on {date} at {old_time}.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        connection.close()

def order_stock(item_name, quantity):
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        # Check if the item already exists in the stock
        cursor.execute("CREATE TABLE IF NOT EXISTS stock (item_name TEXT, quantity REAL)")
        cursor.execute("SELECT * FROM stock WHERE item_name = ?", (item_name))
        existing_item = cursor.fetchone()

        if existing_item:
            # Update the quantity for the existing item
            new_quantity = existing_item[1] + quantity
            cursor.execute("UPDATE stock SET quantity = ? WHERE item_name = ?", (new_quantity, item_name))
        else:
            # Insert a new record for the item in the stock
            cursor.execute("INSERT INTO stock (item_name, quantity) VALUES (?, ?)", (item_name, quantity))

        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Error: {e}")

def check_entire_stock():
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM stock")
        entire_stock = cursor.fetchall()
        connection.close()
        return entire_stock
    except Exception as e:
        print(f"Error: {e}")
        return []
#ali
class MakeReservationPage:
    def __init__(self, master):
        self.master = master
        self.reservation_window = tk.Toplevel(master)
        self.reservation_window.title("Make Reservation Page")
        self.reservation_window.geometry("400x400")

        actions_frame = ttk.Frame(self.reservation_window, padding="20")
        actions_frame.pack()

        # Dropdown for City
        ttk.Label(actions_frame, text="City:").grid(row=0, column=0, sticky=tk.W)
        self.city_var = tk.StringVar()
        self.city_dropdown = ttk.Combobox(actions_frame, textvariable=self.city_var, values=list(branches.keys()))
        self.city_dropdown.grid(row=0, column=1, pady=5)
        self.city_dropdown.bind("<<ComboboxSelected>>", self.update_branch_dropdown)

        # Dropdown for Branch
        ttk.Label(actions_frame, text="Branch:").grid(row=1, column=0, sticky=tk.W)
        self.branch_var = tk.StringVar()
        self.branch_dropdown = ttk.Combobox(actions_frame, textvariable=self.branch_var)
        self.branch_dropdown.grid(row=1, column=1, pady=5)

        # Name Entry
        ttk.Label(actions_frame, text="Name:").grid(row=2, column=0, sticky=tk.W)
        self.name_entry = ttk.Entry(actions_frame)
        self.name_entry.grid(row=2, column=1, pady=5)

        # Calendar for Date Selection
        ttk.Label(actions_frame, text="Date:").grid(row=3, column=0, sticky=tk.W)
        self.calendar = DateEntry(actions_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.calendar.grid(row=3, column=1, pady=5)

        # Time Selection
        ttk.Label(actions_frame, text="Time:").grid(row=4, column=0, sticky=tk.W)
        self.time_entry = ttk.Combobox(actions_frame, values=["10:00 AM", "12:00 PM", "2:00 PM", "4:00 PM", "6:00 PM", "8:00 PM"])
        self.time_entry.grid(row=4, column=1, pady=5)
        #table
        ttk.Label(actions_frame, text="Table:").grid(row=5, column=0, sticky=tk.W)
        self.table_dropdown = ttk.Combobox(actions_frame, values=[i + 1 for i in range(15)])
        self.table_dropdown.grid(row=5, column=1, pady=5)
        #email input checkbox
        self.email_var = tk.BooleanVar()
        email_checkbox = ttk.Checkbutton(actions_frame, text="Send email confirmation", variable=self.email_var)
        email_checkbox.grid(row=6, column=0, columnspan=2, pady=5)

        # Button to make a reservation
        make_reservation_button = ttk.Button(actions_frame, text="Make Reservation", command=self.make_reservation)
        make_reservation_button.grid(row=7, column=0, columnspan=2, pady=10)

    

    def update_branch_dropdown(self, event):
        city = self.city_var.get()
        self.branch_dropdown['values'] = branches.get(city, [])
        self.branch_dropdown.set('')



    def make_reservation(self):
        name = self.name_entry.get().strip()
        city = self.city_var.get()
        branch = self.branch_var.get()
        date = self.calendar.get_date()
        time = self.time_entry.get().strip()
        table = self.table_dropdown.get().strip()

        if name and city and branch and date and time and table:
            # Save reservation to the database
            try:
                connection = sqlite3.connect(DB_FILE)
                cursor = connection.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS reservations (name TEXT, city TEXT, branch TEXT, `table` TEXT, date TEXT, time TEXT)")
                cursor.execute("SELECT * FROM reservations WHERE branch = ? AND date = ? AND time = ? AND `table` = ?", (branch, date, time, table))
                if cursor.fetchone():
                    messagebox.showwarning("Error", "This time slot at the selected table is already booked. Please select another time or table.")
                else:
                    cursor.execute("INSERT INTO reservations VALUES (?, ?, ?, ?, ?, ?)", (name, city, branch, table, date, time))
                    connection.commit()
                    messagebox.showinfo("Success", "Reservation made successfully.")
                connection.close()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            try:
                if self.email_var.get():
                    # Prompt user for the recipient's email address
                    recipient_email = simpledialog.askstring("Email Address", "Enter the recipient's email address:")
                    if recipient_email:
                        # Send email confirmation
                        self.send_email_confirmation(name, date, time, recipient_email)
                    else:
                        messagebox.showwarning("Warning", "Email address not provided. Email confirmation will not be sent.")

                messagebox.showinfo("Reservation Success", f"Reservation for {name} on {date} at {time} successfully made!")
                self.reservation_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Error", "Please enter valid name, date, and time for the reservation.")

    def send_email_confirmation(self, name, date, time, recipient_email):
        me = "blaqmerchandise@gmail.com"
        app_password = "hvlw holu bfci dzfq"

        try:
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpObj.starttls()
            smtpObj.login(me, app_password)

            msg = MIMEText(f"Reservation confirmation\n\nName: {name}\nDate: {date}\nTime: {time}")
            msg['Subject'] = "Reservation Confirmation"
            msg['From'] = me
            msg['To'] = recipient_email

            smtpObj.sendmail(me, [recipient_email], msg.as_string())

            print('Mail sent successfully!')

        except smtplib.SMTPException as e:
            print(f"An error occurred: {e}")

        finally:
            try:
                smtpObj.quit()
            except Exception as e:
                pass
#amgad & ibra
class ReservationPage:
    def __init__(self, master):
        self.master = master
        self.reservation_window = tk.Toplevel(master)
        self.reservation_window.title("Reservation Management")
        self.reservation_window.geometry("1000x1000")

        actions_frame = ttk.Frame(self.reservation_window, padding="20")
        actions_frame.pack()

        # Reservation ID for Update/Delete
        ttk.Label(actions_frame, text="Reservation ID:").grid(row=0, column=0, sticky=tk.W)
        self.reservation_id_entry = ttk.Entry(actions_frame)
        self.reservation_id_entry.grid(row=0, column=1, pady=5)

        # New Time for Update (as a Dropdown)
        ttk.Label(actions_frame, text="New Time:").grid(row=1, column=0, sticky=tk.W)
        self.new_time_dropdown = ttk.Combobox(actions_frame, values=["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"])
        self.new_time_dropdown.grid(row=1, column=1, pady=5)

        # New Table for Update
        ttk.Label(actions_frame, text="New Table:").grid(row=2, column=0, sticky=tk.W)
        table_values = [i+1 for i in range(15)]  # Generating values for 15 tables
        self.new_table_dropdown = ttk.Combobox(actions_frame, values=table_values)
        self.new_table_dropdown.grid(row=2, column=1, pady=5)

        # New Date for Update
        ttk.Label(actions_frame, text="New Date:").grid(row=3, column=0, sticky=tk.W)
        self.new_date_entry = DateEntry(actions_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.new_date_entry.grid(row=3, column=1, pady=5)

        # Update button
        update_button = ttk.Button(actions_frame, text="Update Reservation", command=self.update_reservation)
        update_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Delete button
        delete_button = ttk.Button(actions_frame, text="Delete Reservation", command=self.delete_reservation)
        delete_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Reservation display area
        self.reservation_display = tk.Text(self.reservation_window, height=150, width=100)
        self.reservation_display.pack(pady=50, padx=50)

        self.refresh_reservations_display()


        self.check_entire_reservations()
    
    def refresh_reservations_display(self):
        # Retrieve and display all reservations
        try:
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS reservations (name TEXT, date TEXT, time TEXT)")
            cursor.execute("SELECT * FROM reservations ORDER BY name")
            reservations = cursor.fetchall()
            connection.close()
            self.display_reservations(reservations)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def check_entire_reservations(self):
        # Check entire reservations in the database
        entire_reservations = self.get_entire_reservations()
        self.display_reservations(entire_reservations)

    def check_reservation(self):
        search_name = self.search_entry.get().strip().lower()

        if search_name:
            reservations = get_reservations()
            found = False

            for reservation in reservations:
                if search_name.lower() in reservation[0].lower():
                    found = True
                    break

            if found:
                messagebox.showinfo("Reservation Found", f"Reservation for {reservation[0]} on {reservation[1]} at {reservation[2]} found!")
                self.reservation_window.destroy()
            else:
                messagebox.showinfo("Reservation Not Found", f"No reservation found for {search_name}.")
        else:
            messagebox.showwarning("Error", "Please enter a valid name for searching reservations.")

    def delete_reservation(self):
        search_name = self.search_entry.get().strip().lower()

        if search_name:
            reservations = self.get_reservations()

            # Find the reservation to delete
            found_reservation = next((r for r in reservations if search_name.lower() == r[0].lower()), None)

            if found_reservation:
                self.display_reservations([found_reservation])
                delete_reservation(found_reservation)
                tk.messagebox.showinfo("Reservation Deleted", f"Reservation for {found_reservation[0]} on {found_reservation[1]} at {found_reservation[2]} deleted.")
            else:
                self.display_reservations([])
                tk.messagebox.showinfo("Reservation Not Found", f"No reservation found for {search_name}.")
        else:
            tk.messagebox.showwarning("Error", "Please enter a valid name for deleting reservations.")

    def update_reservation(self):
        search_name = self.search_entry.get().strip().lower()
        new_time = self.new_time_dropdown.get().strip()
        new_table = self.new_table_dropdown.get().strip()
        new_date = self.new_date_entry.get_date()

        try:
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()
            query = "UPDATE reservations SET `table`=?, date=?, time=? WHERE name=?"
            cursor.execute(query, (new_table, new_date, new_time, search_name))
            connection.commit()
            connection.close()
            messagebox.showinfo("Success", "Reservation updated successfully.")
            self.refresh_reservations_display()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_reservations(self, reservations):
        self.reservation_display.delete("1.0", tk.END)
        self.reservation_display.insert(tk.END, "Name\t\tCity\t\tBranch\t\t\tTable\t\tDate\t\tTime\n")
        self.reservation_display.insert(tk.END, "-" * 100 + "\n")
        for res in reservations:
            self.reservation_display.insert(tk.END, f"{res[0]}\t\t{res[1]}\t\t{res[2]}\t\t\t{res[3]}\t\t{res[4]}\t\t{res[5]}\n")

    def get_entire_reservations(self):
        try:
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS reservations (name TEXT, city TEXT, branch TEXT, `table` TEXT, date TEXT, time TEXT)")
            cursor.execute("SELECT * FROM reservations")
            entire_reservations = cursor.fetchall()
            connection.close()

            return entire_reservations
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))
            return []

    def get_reservations(self):
        search_name = self.search_entry.get().strip().lower()
        try:
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS reservations (name TEXT, date TEXT, time TEXT)")
            cursor.execute("SELECT * FROM reservations WHERE name=?", (search_name,))
            reservations = cursor.fetchall()
            connection.close()

            return reservations
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))
            return []
#nora
class OrderPage:
    menu_options = []  

    def __init__(self, master):
        self.master = master
        self.order_window = tk.Toplevel(master)
        self.order_window.title("Order Page")
        self.order_window.geometry("900x900")

        menu_frame = ttk.Frame(self.order_window, padding="40")
        menu_frame.pack()

        order_frame = ttk.Frame(self.order_window, padding="60")
        order_frame.pack()

        ttk.Label(order_frame, text="Discount Code:").grid(row=8, column=0, sticky=tk.W)
        self.discount_entry = ttk.Entry(order_frame)
        self.discount_entry.grid(row=8, column=1, pady=5)

        total_button = ttk.Button(self.order_window, text="Calculate Total", command=self.calculate_total)
        total_button.pack(pady=10)

        total_button = ttk.Button(self.order_window, text="Apply Discount", command=self.price_after_discount)
        total_button.pack(pady=10)

        self.total_label = ttk.Label(self.order_window, text="Total: $0.00", font=('Helvetica', 16))
        self.total_label.pack(pady=20)

        payment_frame = ttk.Frame(self.order_window, padding="20")
        payment_frame.pack()

        self.payment_var = tk.StringVar()
        cash_radio = ttk.Radiobutton(payment_frame, text="Cash", variable=self.payment_var, value="cash")
        cash_radio.grid(row=0, column=0, padx=10)
        card_radio = ttk.Radiobutton(payment_frame, text="Card", variable=self.payment_var, value="card")
        card_radio.grid(row=0, column=1, padx=10)

        payment_button = ttk.Button(self.order_window, text="Proceed to Payment", command=self.process_payment)
        payment_button.pack(pady=10)

        OrderPage.update_menu_options()
        self.selected_items = {}
        for item in OrderPage.menu_options:
            label = ttk.Label(menu_frame, text=f"{item[0]} - ${item[1]:.2f}")
            label.grid(row=len(self.selected_items), column=0, sticky=tk.W)

            quantity_var = tk.IntVar()
            quantity_combobox = ttk.Combobox(menu_frame, textvariable=quantity_var, values=[0, 1, 2, 3, 4, 5])
            quantity_combobox.grid(row=len(self.selected_items), column=1, padx=10)

            self.selected_items[item[0]] = {"label": label, "price": item[1], "quantity_var": quantity_var}

    @staticmethod
    def update_menu_options():
        # Update menu options separately
        OrderPage.menu_options = get_menu_filtered()

    def price_after_discount(self):
        username = self.discount_entry.get()
        conn = sqlite3.connect('user_credentials.db')
        cursor = conn.cursor()
        cursor.execute('SELECT role FROM credentials WHERE username=?', (username,))
        result = cursor.fetchone()
        conn.close()
        if result and result[0] == 'staff':
            discount_percentage = 20
            total_before_discount = sum(item["price"] * item["quantity_var"].get() for item in self.selected_items.values() if item["quantity_var"].get() > 0)
            discount_amount = (discount_percentage / 100) * total_before_discount
            total_after_discount = total_before_discount - discount_amount
            self.total_label.config(text=f"Total: ${total_after_discount:.2f}")
        else:
            total = sum(item["price"] * item["quantity_var"].get() for item in self.selected_items.values() if item["quantity_var"].get() > 0)
            self.total_label.config(text=f"Total: ${total:.2f}")

    def calculate_total(self):
        total = sum(item["price"] * item["quantity_var"].get() for item in self.selected_items.values() if item["quantity_var"].get() > 0)
        self.total_label.config(text=f"Total: ${total:.2f}")

    def process_payment(self):
        username = self.discount_entry.get()
        conn = sqlite3.connect('user_credentials.db')
        cursor = conn.cursor()
        cursor.execute('SELECT role FROM credentials WHERE username=?', (username,))
        result = cursor.fetchone()
        conn.close()

        if result and result[0] == 'staff':
            discount_percentage = 20 
            total_before_discount = sum(item["price"] * item["quantity_var"].get() for item in self.selected_items.values() if item["quantity_var"].get() > 0)
            discount_amount = (discount_percentage / 100) * total_before_discount
            total_after_discount = total_before_discount - discount_amount
            total = total_after_discount
        else:
            total = sum(item["price"] * item["quantity_var"].get() for item in self.selected_items.values() if item["quantity_var"].get() > 0)
            self.total_label.config(text=f"Total: ${total:.2f}")

        payment_method = self.payment_var.get()

        if not payment_method:
            messagebox.showwarning("Payment Method", "Please select a payment method (Cash or Card).")
            return

        if payment_method == "cash":
            messagebox.showinfo("Payment Success", f"Payment of ${total:.2f} processed successfully using Cash! Please proceed to the register.")
            self.order_window.destroy()
        elif payment_method == "card":
            self.open_card_payment_window(total)
            self.order_window.destroy()
        else:
            messagebox.showwarning("Payment Method", "Invalid payment method selected.")

        current_datetime = datetime.now()
        save_payment(total, current_datetime.strftime("%Y-%m-%d"), current_datetime.strftime("%H:%M:%S"))
        for item, details in self.selected_items.items():
            quantity = details["quantity_var"].get()
            if quantity > 0:
                self.save_into_orders(current_datetime.strftime("%Y-%m-%d"), current_datetime.strftime("%H:%M:%S"), total, item, quantity)

    def save_into_orders(self, date, time, total, item, quantity):
        try:
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS orders ( order_id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, time TEXT, total REAL, item TEXT, quantity TEXT)")
            cursor.execute("INSERT INTO orders (date, time, total, item, quantity) VALUES (?, ?, ?, ?, ?)", (date, time, total, item, quantity))
            connection.commit()
            connection.close()
        except Exception as e:
            print(f"Error: {e}")

    def open_card_payment_window(self, total):
        card_payment_window = tk.Toplevel(self.order_window)
        card_payment_window.title("Card Payment Details")

        # Create labels and entry widgets for card details
        ttk.Label(card_payment_window, text="Card Number:").grid(row=0, column=0, sticky=tk.W)
        card_number_entry = ttk.Entry(card_payment_window)
        card_number_entry.grid(row=0, column=1, pady=5)

        ttk.Label(card_payment_window, text="Expiry Date:").grid(row=1, column=0, sticky=tk.W)
        expiry_date_entry = ttk.Entry(card_payment_window)
        expiry_date_entry.grid(row=1, column=1, pady=5)

        ttk.Label(card_payment_window, text="CVV:").grid(row=2, column=0, sticky=tk.W)
        cvv_entry = ttk.Entry(card_payment_window, show="*")
        cvv_entry.grid(row=2, column=1, pady=5)

        # Create a button to save card details and process payment
        save_button = ttk.Button(card_payment_window, text="Save and Process Payment", command=lambda: self.save_card_details_and_process(total, card_number_entry.get(), expiry_date_entry.get(), cvv_entry.get(), card_payment_window))
        save_button.grid(row=3, column=0, columnspan=2, pady=10)
#amgad 
class OrderManagementPage:
    def __init__(self, master):
        self.master = master
        self.management_window = tk.Toplevel(master)
        self.management_window.title("Order Management")
        self.management_window.geometry("800x600")

        self.orders_frame = tk.Frame(self.management_window)
        self.orders_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.load_orders()

    def load_orders(self):
        # Clear existing content in the frame
        for widget in self.orders_frame.winfo_children():
            widget.destroy()

        # Add header labels
        headers = ["Order ID", "Date", "Time", "Total", "Item", "Quantity", "Action"]
        for col, header in enumerate(headers):
            label = tk.Label(self.orders_frame, text=header, font=('bold', 12))
            label.grid(row=0, column=col, padx=10, pady=10)

        try:
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()
            cursor.execute("SELECT order_id, date, time, total, item, quantity FROM orders")
            orders = cursor.fetchall()
            connection.close()

            for row, order in enumerate(orders, start=1):
                order_id = order[0]  # The first element is the order_id

                for col, value in enumerate(order):
                    label = tk.Label(self.orders_frame, text=value)
                    label.grid(row=row, column=col, padx=10, pady=10)

                # "Done" button to delete the order
                done_button = tk.Button(self.orders_frame, text="Done", 
                                        command=lambda oid=order_id, rw=row: self.handle_order_completion(oid, rw))
                done_button.grid(row=row, column=len(headers)-1, padx=10, pady=10)

        except Exception as e:
            print(f"Error: {e}")

    def handle_order_completion(self, order_id, row):
        # Calculate and store the order completion time
        self.calculate_and_store_order_completion_time(order_id)

        # Then delete the order
        self.delete_order(order_id, row)

    def calculate_and_store_order_completion_time(self, order_id):
        try:
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()

            # Fetch the order time
            cursor.execute("SELECT date, time FROM orders WHERE order_id = ?", (order_id,))
            order_date_time = cursor.fetchone()

            if order_date_time:
                order_date, order_time = order_date_time

                # Ensuring that order_date is a date object and order_time is a time object
                if not isinstance(order_date, datetime.date) or not isinstance(order_time, datetime.time):
                    print(f"Invalid data types for order date and time for order ID: {order_id}")
                    return

                order_datetime = datetime.combine(order_date, order_time)
                current_datetime = datetime.now()
                time_taken = current_datetime - order_datetime
                time_taken_seconds = time_taken.total_seconds()

                print(f"Storing completion time for order ID {order_id}: {time_taken_seconds} seconds")  # Debugging print

                # Store the time taken in the order_completion table
                cursor.execute("INSERT INTO order_completion (order_id, time_taken) VALUES (?, ?)",
                            (order_id, time_taken_seconds))
                connection.commit()

                print("Order completion time stored successfully")  # Debugging print
            else:
                print(f"Order date and time not found for order ID: {order_id}")  # Debugging print

            connection.close()

        except Exception as e:
            print(f"Error while storing order completion time: {e}")

    def delete_order(self, order_id, row):
        try:
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
            connection.commit()
            connection.close()

            # Remove the widgets for this row
            for widget in self.orders_frame.grid_slaves(row=row):
                widget.destroy()

        except Exception as e:
            print(f"Error while deleting order: {e}")
#ibra & amgad
class PaymentHistoryPage:
    def __init__(self, master):
        self.master = master
        self.history_window = tk.Toplevel(master)
        self.history_window.title("Payment History Page")

        # Set a larger default size for the Payment History Page
        self.history_window.geometry("800x600")

        # Display payment history
        history_label = ttk.Label(self.history_window, text="Payment History", font=('Helvetica', 18, 'bold'))
        history_label.pack(pady=20)

        # Create a text widget to display payment history
        self.history_text = tk.Text(self.history_window, wrap=tk.WORD, font=('Helvetica', 12), height=20, width=70)
        self.history_text.pack(pady=20, padx=20)

        # Load and display payment history
        self.load_payment_history()

    def load_payment_history(self):
        # Load payment history from the database
        history = get_payment_history()

        # Display payment history in the text widget
        self.history_text.insert(tk.END, "Date\t\tTime\t\tTotal\n")
        self.history_text.insert(tk.END, "-" * 90 + "\n")
        print(f"The payment history contains {len(history)} records.")
        for payment in history:
            self.history_text.insert(tk.END, f"{payment[0]}\t\t{payment[1]}\t\t${payment[2]:.2f}\n")
#nour
class UpdateMenuPage:
    def __init__(self, master):
        self.master = master
        self.update_menu_window = tk.Toplevel(master)
        self.update_menu_window.title("Update Menu Page")

        self.update_menu_window.geometry("1000x1000")

        # Create a frame for menu updates
        update_frame = ttk.Frame(self.update_menu_window, padding="80")
        update_frame.pack()

        # Create labels and entry widgets for menu updates
        ttk.Label(update_frame, text="Item Name:").grid(row=0, column=0, sticky=tk.W)
        self.item_name_entry = ttk.Entry(update_frame)
        self.item_name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(update_frame, text="Item Price:").grid(row=1, column=0, sticky=tk.W)
        self.item_price_entry = ttk.Entry(update_frame)
        self.item_price_entry.grid(row=1, column=1, pady=5)

        ttk.Label(update_frame, text="Category:").grid(row=2, column=0, sticky=tk.W)
        self.item_category_entry = ttk.Entry(update_frame)
        self.item_category_entry.grid(row=2, column=1, pady=5)

        ttk.Label(update_frame, text="Description:").grid(row=3, column=0, sticky=tk.W)
        self.item_description_entry = ttk.Entry(update_frame)
        self.item_description_entry.grid(row=3, column=1, pady=5)

        ttk.Label(update_frame, text="Allergies:").grid(row=4, column=0, sticky=tk.W)
        self.item_allergy_entry = ttk.Entry(update_frame)
        self.item_allergy_entry.grid(row=4, column=1, pady=5)

        ttk.Label(update_frame, text="availability: ").grid(row=5, column=0, sticky=tk.W)
        self.item_availb_entry = ttk.Entry(update_frame)
        self.item_availb_entry.grid(row=5, column=1, pady=5)

        # Create buttons for menu updates
        add_button = ttk.Button(update_frame, text="Add Item", command=self.add_menu_item)
        add_button.grid(row=6, column=0, pady=10)

        update_button = ttk.Button(update_frame, text="Update Item", command=self.update_menu_item)
        update_button.grid(row=6, column=1, pady=10)

        update_button = ttk.Button(update_frame, text="Update Stat", command=self.update_menu_stat)
        update_button.grid(row=6, column=2, pady=10)

        delete_button = ttk.Button(update_frame, text="delete Item", command=self.delete_menu_item)
        delete_button.grid(row=6, column=3, pady=10)

        self.display_menu()

    def add_menu_item(self):

        item_name = self.item_name_entry.get()
        item_price = float(self.item_price_entry.get()) if self.item_price_entry.get() else 0.0
        item_category = self.item_category_entry.get()
        item_description = self.item_description_entry.get()  
        item_allergy = self.item_allergy_entry.get()
        item_availb = self.item_availb_entry.get()

        if item_name and item_price and item_category and item_description and item_allergy:
            # Add item to the menu in the database
            add_menu_item(item_name, item_price, item_category, item_description, item_allergy, item_availb)
            tk.messagebox.showinfo("Success", f"Item '{item_name}' added to the menu.")
            self.display_menu()
            self.update_menu_window.destroy()
        else:
            tk.messagebox.showwarning("Error", "Please enter all required fields.")

    def update_menu_item (self):
        item_name = self.item_name_entry.get()
        item_price = float(self.item_price_entry.get()) if self.item_price_entry.get() else 0.0

        if item_name and item_price  :
            # Update item in the menu in the database
            update_menu_item(item_name, item_price)
            tk.messagebox.showinfo("Success", f"Item '{item_name}' updated in the menu.")
            self.display_menu()
            self.update_menu_window.destroy()
        else:
            tk.messagebox.showwarning("Error", "Please enter valid item name.")

    def update_menu_stat (self):
        item_name = self.item_name_entry.get()
        item_availb = self.item_availb_entry.get()

        if item_name and item_availb :
            # Update item in the menu in the database
            update_menu_stat(item_name, item_availb)
            tk.messagebox.showinfo("Success", f"Item '{item_name}' updated in the menu.")
            self.display_menu()
            self.update_menu_window.destroy()
        else:
            tk.messagebox.showwarning("Error", "Please enter valid item name.")

    def delete_menu_item(self):
        item_name = self.item_name_entry.get()
        
        if item_name:
            # Delete item from the menu in the database
            delete_menu_item(item_name)
            tk.messagebox.showinfo("Success", f"Item '{item_name}' deleted from the menu.")
            self.display_menu()
            self.update_menu_window.destroy()
        else:
            tk.messagebox.showwarning("Error", "Please enter a valid item name.")

    def display_menu(self):
    # Create a frame to display the current menu
        menu_frame = ttk.Frame(self.update_menu_window, padding="100")
        menu_frame.pack(fill=tk.BOTH, expand=True)

        # Display the current menu in the frame
        menu_text = tk.Text(menu_frame, wrap=tk.WORD, font=('Helvetica', 12), height=40, width=1000, bg="white")
        menu_text.pack(pady=80, padx=80)

        current_menu = get_menu()
        menu_text.insert(tk.END, "Item\t\tPrice\t\tCategory\t\tStatus\n")
        menu_text.insert(tk.END, "-" * 100 + "\n")
        for item in current_menu:
            menu_text.insert(tk.END, f"{item[0]}\t\t${item[1]:.2f}\t\t{item[2]}\t\t{item[5]}\n")
#nora & ali
class OrderStock:
    def __init__(self, master):
        self.master = master
        self.order_stock_window = tk.Toplevel(master)
        self.order_stock_window.title("Order Stock Page")

        # Set a larger default size for the Order Stock Page
        self.order_stock_window.geometry("600x400")

        # Create a frame for stock ordering
        order_frame = ttk.Frame(self.order_stock_window, padding="20")
        order_frame.pack()

        # Create labels and entry widgets for stock ordering
        ttk.Label(order_frame, text="Item Name:").grid(row=0, column=0, sticky=tk.W)
        self.order_item_name_entry = ttk.Entry(order_frame)
        self.order_item_name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(order_frame, text="Quantity:").grid(row=1, column=0, sticky=tk.W)
        self.order_quantity_entry = ttk.Entry(order_frame)
        self.order_quantity_entry.grid(row=1, column=1, pady=5)

        # Create a button to order stock
        order_stock_button = ttk.Button(order_frame, text="Order Stock", command=self.order_stock)
        order_stock_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Create a text widget to display stock information
        self.stock_text = tk.Text(self.order_stock_window, wrap=tk.WORD, font=('Helvetica', 12), height=20, width=70, bg="white")
        self.stock_text.pack(pady=20, padx=20)

        self.check_entire_stock()
        self.start_automatic_ordering()

    def start_automatic_ordering(self):
        # Start a separate thread for automatic ordering
        self.automatic_ordering_thread = threading.Thread(target=self.monitor_stock_level)
        self.automatic_ordering_thread.daemon = True  # Daemonize the thread so it automatically exits when the main program exits
        self.automatic_ordering_thread.start()

    def monitor_stock_level(self):
        # Function to continuously monitor stock levels and place orders if necessary
        while True:
            entire_stock = self.get_entire_stock()
            for item in entire_stock:
                if item[1] < THRESHOLD:
                    self.place_order(item[0], THRESHOLD - item[1])  # Order enough quantity to reach the threshold
            # Wait for a certain interval before checking again (e.g., every hour)
            time.sleep(3600)  # Wait for 1 hour

    def place_order(self, item_name, quantity):
        # Function to place an order for a specific item and quantity
        try:
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO stock_orders (item_name, quantity) VALUES (?, ?)", (item_name, quantity))
            connection.commit()
            connection.close()
            # Optionally, you can notify the user that an order has been placed
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

    def order_stock(self):
        item_name = self.order_item_name_entry.get()
        quantity = self.order_quantity_entry.get()

        if item_name and quantity.isdigit():
            # Order stock in the database
            self.save_stock_order(item_name, int(quantity))
            tk.messagebox.showinfo("Success", f"Stock order for {quantity} units of {item_name} placed successfully.")
            self.check_entire_stock() # Update displayed stock after ordering
            self.order_stock_window.destroy() 
        else:
            tk.messagebox.showwarning("Error", "Please enter valid item name and quantity for stock ordering.")

    def check_entire_stock(self):
        # Check entire stock in the database
        entire_stock = self.get_entire_stock()
        self.display_stock(entire_stock)

    def display_stock(self, stock_info):
        # Display stock information in the text widget
        self.stock_text.delete("1.0", tk.END)  # Clear previous content
        self.stock_text.insert(tk.END, "Item Name\t\tQuantity\n")
        self.stock_text.insert(tk.END, "-" * 40 + "\n")
        for item in stock_info:
            self.stock_text.insert(tk.END, f"{item[0]}\t\t{item[1]}\n")

    def save_stock_order(self, item_name, quantity):
        try:
            connection = sqlite3.connect(DB_FILE)  # Update with the actual path to your stock orders database
            cursor = connection.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS stock_orders (item_name TEXT, quantity INTEGER)")
            cursor.execute("INSERT INTO stock_orders VALUES (?, ?)", (item_name, quantity))

            connection.commit()
            connection.close()
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

    def get_entire_stock(self):
        try:
            connection = sqlite3.connect(DB_FILE)  # Update with the actual path to your stock orders database
            cursor = connection.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS stock_orders (item_name TEXT, quantity INTEGER)")
            cursor.execute("SELECT item_name, SUM(quantity) FROM stock_orders GROUP BY item_name")
            entire_stock = cursor.fetchall()

            connection.close()

            return entire_stock
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))
            return []

#nour
class UserDatabase:
    
    def __init__(self, master):
        self.master = master
        self.users_window = tk.Toplevel(master)
        self.users_window.title("User Management System")
        # self.users_window.geometry("400x400")

        self.create_table()

        self.frame = ttk.Frame(self.users_window, padding="10")
        # actions_frame = ttk.Frame(self.users_window, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.frame, text="User Management System", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(self.frame, text="Add User", command=self.add_user).grid(row=1, column=0, pady=5)
        ttk.Button(self.frame, text="Show Users", command=self.show_users).grid(row=1, column=1, pady=5)
        ttk.Button(self.frame, text="Delete User", command=self.delete_user).grid(row=2, column=1, pady=5)
        ttk.Button(self.frame, text="Exit", command=self.users_window.destroy).grid(row=2, column=0, pady=5)
        
    
    def create_table(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT , 
                username TEXT UNIQUE,
                password TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def add_user(self):
        add_user_window = tk.Toplevel(self.master)
        add_user_window.title("Add User")

        role_label = ttk.Label(add_user_window, text="User's Role:")
        role_label.grid(row=0, column=0, padx=5, pady=5)

        role_entry = ttk.Entry(add_user_window)
        role_entry.grid(row=0, column=1, padx=5, pady=5)

        username_label = ttk.Label(add_user_window, text="Username:")
        username_label.grid(row=1, column=0, padx=5, pady=5)

        username_entry = ttk.Entry(add_user_window)
        username_entry.grid(row=1, column=1, padx=5, pady=5)

        password_label = ttk.Label(add_user_window, text="Password:")
        password_label.grid(row=2, column=0, padx=5, pady=5)

        password_entry = ttk.Entry(add_user_window, show="*")
        password_entry.grid(row=2, column=1, padx=5, pady=5)

        add_button = ttk.Button(add_user_window, text="Add User", command=lambda: self.save_user(role_entry.get(), username_entry.get(), password_entry.get(), add_user_window))
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

    def save_user(self, role, username, password, window):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('INSERT INTO credentials (role, username, password) VALUES (?, ?, ?)', (role, username, password))

        conn.commit()
        conn.close()

        window.destroy()

        print("User added successfully!")

    def show_users(self):
        show_users_window = tk.Toplevel(self.master)
        show_users_window.title("Show Users")

        tree = ttk.Treeview(show_users_window, columns=("ID", "Role", "Username", "Password"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Role", text="Role")
        tree.heading("Username", text="Username")
        tree.heading("Password", text="Password")

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM credentials')
        users = cursor.fetchall()

        for user in users:
            tree.insert("", "end", values=user)

        conn.close()

        tree.grid(row=0, column=0, pady=10, padx=10)

    def delete_user(self):
        username = simpledialog.askstring("Delete User", "Enter the username to delete:")
        if username:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM credentials WHERE username = ?", (username))
            if cursor.rowcount:
                messagebox.showinfo("Success", f"User '{username}' deleted successfully.")
                conn.commit()
            else:
                messagebox.showwarning("Warning", f"No user found with username '{username}'.")

            cursor.close()
            conn.close()
        else:
            messagebox.showinfo("Info", "No username entered.")

class RestaurantAdminPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Restaurant Management System")

        # Get the screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Load the background image5
        image = Image.open("shape-5.png")  
        self.photo = ImageTk.PhotoImage(image)

        # Create a label to display the background image
        background_label = ttk.Label(master, image=self.photo)
        background_label.place(relwidth=1, relheight=1)

        # Create a ThemedStyle for a more modern look
        style = ThemedStyle(master)
        style.set_theme("arc")

        # Create a frame to organize the buttons with a rounded border and subtle shadow
        button_frame = ttk.Frame(master, style="TFrame", padding=(10, 10, 10, 10))
        button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Title label with a larger font, bold style, and custom color
        self.Label1 = tk.Label(master=master, text='Restaurant Management System', font=('Arial', 36, 'bold'),
                               fg="#2E4053")  # Dark Blue
        self.Label1.place(relx=0.35, rely=0.1)

        # Date and time label with a larger font, custom color, and shadow effect
        self.localtime_label = tk.Label(master=master, text="", font=('Helvetica', 18), fg="#717D7E", bd=2,
                                        relief=tk.SUNKEN)
        self.localtime_label.place(relx=0.44, rely=0.17)

        # Buttons for different options with a modern style, custom font, and color
        options = ["Make an Order", "Make Reservation", "Check Reservation", "Order Stock",
                   "Update Menu", "Payment History", "Order Management", "Edit Users", "Exit"]

        # Define the custom sorting order
        custom_order = {
            "Make an Order": 0,
            "Make Reservation": 1,
            "Check Reservation": 2,
            "Order Stock": 3,
            "Update Menu": 4,
            "Payment History": 5,
            "Order Management": 6,
            "Edit Users": 7,
            "Exit": 8
        }

        # Sort the buttons based on the custom order
        sorted_options = sorted(options, key=lambda x: custom_order[x])

        # Initialize counters for each row
        row1_count = 0
        row2_count = 0

        for option in sorted_options:
            button = ttk.Button(button_frame, text=option, command=lambda o=option: self.open_option_window(o),
                                style="TButton")

            if row1_count < 5:
                button.grid(row=0, column=row1_count, pady=20, padx=40, ipadx=40, ipady=20)
                row1_count += 1
            elif row2_count < 3:
                button.grid(row=1, column=row2_count, pady=20, padx=40, ipadx=40, ipady=20)
                row2_count += 1
            else:
                button.grid(row=2, pady=20, padx=40, ipadx=40, ipady=20)

        # Set the window size to full screen
        self.master.geometry(f"{screen_width}x{screen_height}")

        # Initialize the date and time display
        self.update_time()

    def open_option_window(self, option):
        # You can implement the logic to open different windows based on the selected option
        print(f"Opening window for {option}")

    def update_time(self):
        # Update the date and time in the label
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        self.localtime_label.config(text=formatted_datetime)
        # Schedule the update_time function to run again after 1000 milliseconds (1 second)
        self.master.after(1000, self.update_time)

    def open_option_window(self, option):
        if option == "Make an Order":
            OrderPage(self.master)
        elif option == "Make Reservation":
            MakeReservationPage(self.master)
        elif option == "Check Reservation":
            ReservationPage(self.master)
        elif option == "Update Menu":
            UpdateMenuPage(self.master)
        elif option == "Order Stock": 
            OrderStock(self.master)
        elif option == "Payment History":
            PaymentHistoryPage(self.master)
        elif option == "Edit Users":
            UserDatabase(self.master)
        elif option == "Order Management":
            OrderManagementPage(self.master)
        elif option == "Exit" : 
            self.master.destroy()
        else:
            # Create a new window for the selected option
            option_window = tk.Toplevel(self.master)
            option_window.title(option + " Page")

            
            content_label = tk.Label(option_window, text=f"This is the {option} page.", font=('Helvetica', 14))
            content_label.pack(pady=20)

root = tk.Tk()
root.resizable(True, True)

# Create an instance of the RestaurantHomePage class
restaurant_home_page = RestaurantAdminPage(root)

# Run the Tkinter event loop
root.mainloop()