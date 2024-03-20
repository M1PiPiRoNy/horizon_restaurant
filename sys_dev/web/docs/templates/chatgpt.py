from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
DB_FILE = 'image_data.db'

# Route to serve the HTML file
@app.route('/')


def index():
    # Connect to SQLite database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Execute query to fetch menu items
    cursor.execute('SELECT * FROM menu')
    menu_items = cursor.fetchall()
    print(menu_items)

    # Close database connection
    conn.close()

    # Render the HTML file with menu items
    return render_template('chatgpt.html', menu_items=menu_items)

if __name__ == '__main__':
    app.run(debug=True)
