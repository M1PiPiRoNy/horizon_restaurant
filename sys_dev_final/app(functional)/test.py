import sqlite3

def get_payment_history():
    connection = sqlite3.connect("data/data.db")
    cursor = connection.cursor()

    #cursor.execute("CREATE TABLE IF NOT EXISTS menu (name TEXT, price REAL, category TEXT, description TEXT, allergy TEXT, availability TEXT)")
    cursor.execute("SELECT * FROM reservations ")
    history = cursor.fetchall()

    connection.close()
    return history

# Check if the payment history is empty
payment_history = get_payment_history()

if not payment_history:
    print("The payment history is empty.")
else:
    print(f"The payment history contains {payment_history} records.")
    
