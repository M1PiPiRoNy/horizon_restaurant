from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'data.db'  # path to your database file

@app.route('/')
def index():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'reservation.html')

@app.route('/update_reservation', methods=['POST'])
def update_reservation():
    reservation_id = request.json['reservationId']
    new_time = request.json['newTime']
    new_table = request.json['newTable']
    new_date = request.json['newDate']

    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("UPDATE reservations SET time=?, table=?, date=? WHERE id=?", (new_time, new_table, new_date, reservation_id))
        connection.commit()
        connection.close()
        return jsonify({"status": "success", "message": "Reservation updated successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/delete_reservation', methods=['POST'])
def delete_reservation():
    reservation_id = request.json['reservationId']

    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM reservations WHERE id=?", (reservation_id,))
        connection.commit()
        connection.close()
        return jsonify({"status": "success", "message": "Reservation deleted successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
