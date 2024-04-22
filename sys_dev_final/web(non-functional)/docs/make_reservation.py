from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'shush'

DB_FILE = 'data/data.db'  

@app.route('/')
def index():
    return render_template('booking.html')  

@app.route('/make_reservation', methods=['POST'])
def make_reservation():
    name = request.form['name'].strip()
    email = request.form['email'].strip()
    table = request.form['table'].strip()
    date = request.form['date'].strip()
    
    if name and email and table and date:
        try:
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS reservations (name TEXT, email TEXT, `table` TEXT, date TEXT)")
            cursor.execute("SELECT * FROM reservations WHERE `table` = ? AND date = ?", (table, date))
            if cursor.fetchone():
                flash("This table is already booked for the selected date.", 'error')
            else:
                cursor.execute("INSERT INTO reservations VALUES (?, ?, ?, ?)", (name, email, table, date))
                connection.commit()
                flash("Reservation made successfully.", 'success')
            connection.close()
        except Exception as e:
            flash(str(e), 'error')
    else:
        flash("Please make sure all fields are filled in correctly.", 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
