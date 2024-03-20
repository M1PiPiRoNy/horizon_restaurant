import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('data2.db')
cursor = conn.cursor()

# Create a table to store image information
cursor.execute('''CREATE TABLE IF NOT EXISTS menu
                (id INTEGER PRIMARY KEY, 
                name TEXT NOT NULL,
                price REAL,
                description TEXT)''')

# Commit the changes and close the connection
conn.commit()
conn.close()

def add_image(name,  price, description):
    conn = sqlite3.connect('data2.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO menu (name, price, description) VALUES (?, ?, ?)''', (name, price, description))
    conn.commit()
    conn.close()

# def get_image_info(image_id):
#     conn = sqlite3.connect('image_data.db')
#     cursor = conn.cursor()
#     cursor.execute('''SELECT filename, path FROM images WHERE id = ?''', (image_id,))
#     image_info = cursor.fetchone()
#     conn.close()
#     return image_info

# Example usage
name = input('name?')
price = input('price?')
des = input()

add_image(name, price, des)
#image_info = get_image_info(1)
#print(image_info)

def all() : 
    conn = sqlite3.connect('data2.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM menu''')
    menu = cursor.fetchall()
    conn.close()
    return menu
print(all())