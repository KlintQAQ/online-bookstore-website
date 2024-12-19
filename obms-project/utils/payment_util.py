# Method to process a payment
def process_payment(mysql, order_id, amount, payment_date):
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Payments (order_id, amount, payment_date) VALUES (%s, %s, %s)", (order_id, amount, payment_date))
        mysql.connection.commit()
        cur.close()
        return 1  # Payment processed successfully
    except:
        return 0  # Failed to process payment

# Method to retrieve payments for an order
def get_payments_by_order(mysql, order_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Payments WHERE order_id = %s", (order_id,))
    payments = cur.fetchall()
    cur.close()
    return payments
