import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
from cryptography.fernet import Fernet

class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login form")
        self.geometry('340x440')
        self.configure(bg='#333333')

        self.frame = tk.Frame(self, bg='#333333')

        self.login_label = tk.Label(
            self.frame, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))
        self.username_label = tk.Label(
            self.frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
        self.username_entry = tk.Entry(self.frame, font=("Arial", 16))
        self.password_entry = tk.Entry(self.frame, show="*", font=("Arial", 16))
        self.password_label = tk.Label(
            self.frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
        self.login_button = tk.Button(
            self.frame, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=self.authenticate)

        # Placing widgets on the screen
        self.login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
        self.username_label.grid(row=1, column=0)
        self.username_entry.grid(row=1, column=1, pady=20)
        self.password_label.grid(row=2, column=0)
        self.password_entry.grid(row=2, column=1, pady=20)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=30)

        self.frame.pack()

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check the entered username and password against the database
        role = self.check_credentials(username, password)
        if role == 'manager':
            os.system('python3 manager.py')
            self.destroy
        elif role == 'staff':
            os.system('python3 staff.py')
            self.destroy
        elif role == 'admin':
            os.system('python3 admin.py')
            self.destroy
        elif role == 'chef':
            os.system('python3 chef.py')
            self.destroy
        
        
    def check_credentials(self, username, password):
        conn = sqlite3.connect('user_credentials.db')
        cursor = conn.cursor()

        # Query to check if the username and password match in the database
        cursor.execute('SELECT role FROM credentials WHERE username=? AND password=?', (username, password))
        result = cursor.fetchone()

        conn.close()

        if result:
            return result[0]  # Return the role (admin or staff)
        else:
            return None

    def decrypt_file(self, file_path, key):
        try:
            with open(file_path, 'rb') as file:
                data = file.read()

            cipher_suite = Fernet(key)
            decrypted_data = cipher_suite.decrypt(data)

            decrypted_file_path = file_path[:-10]
            with open(decrypted_file_path, 'wb') as file:
                file.write(decrypted_data)

            return decrypted_file_path
        except Exception as e:
            print(f"Decryption error: {e}")
            return None

if __name__ == "__main__":
    app = LoginForm()
    app.mainloop()