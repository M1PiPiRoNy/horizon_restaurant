from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('data2.db')
        cursor = conn.cursor()

        # Query to select menu items
        query = "SELECT name, price FROM menu"
        cursor.execute(query)
        menu_items = cursor.fetchall()

        # Print menu items to console for debugging
        print(menu_items)

        # Close database connection
        cursor.close()
        conn.close()

        return render_template('menu_flask.html', menu_items=menu_items)
    except Exception as e:
        print("An error occurred:", e)
        return "An error occurred while fetching menu items."

if __name__ == '__main__':
    app.run(debug=True)
