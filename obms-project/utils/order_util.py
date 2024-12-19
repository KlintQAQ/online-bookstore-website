import datetime

from utils.inventory_util import execute_inventory_stock_updates

def create_order(mysql, customer_id, book_id, quantity, total):
    """
    Create an order for a specific user.

    Args:
    mysql: The Flask-MySQLDB object.
    customer_id: The ID of the customer placing the order.
    book_id: The ID of the book being ordered.
    quantity: The quantity of the book.
    total: The total price of the order.

    Returns:
    The ID of the created order if the order is created successfully, None if an error occurs during the process.
    """
    try:
        cursor = mysql.connection.cursor()
        timestamp = datetime.datetime.now()

        # Start a transaction
        cursor.execute("START TRANSACTION")

        order_id = insert_order_and_return_id(cursor, customer_id, book_id, quantity, total, timestamp)  # Insert the order and get the order ID
        if order_id:
            execute_inventory_stock_updates(cursor, book_id, quantity)  # Update the inventory stock
            mysql.connection.commit()  # Commit the transaction
        else:
            mysql.connection.rollback()  # Rollback the transaction if order creation fails

        cursor.close()
        return order_id  # Return the ID of the created order
    except Exception as e:
        # Print the exception for debugging purposes
        print(f"An error occurred: {e}")
        return None  # Return None if an error occurs during order creation
    
def all_orders_by_customer(mysql, customer_id):
    """
    Retrieve all orders for a specific customer from the database.

    Args:
    mysql: The Flask-MySQLDB object.
    customer_id: The ID of the customer whose orders are to be retrieved.

    Returns:
    On success, returns a list of orders for the customer.
    On failure or if no orders are found, returns an empty list.
    """
    try:
        # Create a cursor to execute the SQL query
        cursor = mysql.connection.cursor()

        # Execute the SQL query to retrieve all orders for the customer with additional book details
        cursor.execute("""
            SELECT 
                books.book_id,
                books.title, 
                books.price, 
                authors.author_first_name, 
                authors.author_last_name, 
                publishers.publisher_name,
                orders.quantity,
                orders.order_date
            FROM orders 
            INNER JOIN books ON orders.book_id = books.book_id 
            INNER JOIN authors ON books.author_id = authors.author_id 
            INNER JOIN publishers ON books.publisher_id = publishers.publisher_id 
            WHERE orders.customer_id = %s
        """, (customer_id,))

        # Fetch all the results
        orders_data = cursor.fetchall()

        # Convert the result to a list of dictionaries
        orders = []
        for row in orders_data:
            order = {
                'book_id': row[0],
                'title': row[1],
                'price': row[2],
                'author_first_name': row[3],
                'author_last_name': row[4],
                'publisher_name': row[5],
                'quantity': row[6],
                'order_date': row[7]
            }
            orders.append(order)

        cursor.close()
        return orders
    except Exception as e:
        # Handle any exceptions and return an empty list
        print(f"An error occurred: {e}")
        return []

# Function to insert a new order into the database and return the ID of the created order
def insert_order_and_return_id(cursor, customer_id, book_id, quantity, total, timestamp):
    """
    Insert a new order into the database and return the ID of the created order.

    Args:
    cursor: The MySQL cursor object.
    customer_id: The ID of the customer placing the order.
    book_id: The ID of the book being ordered.
    quantity: The quantity of the book.
    total: The total price of the order.
    timestamp: The timestamp of the order.

    Returns:
    The ID of the created order.
    """
    # Insert the order into the Orders table
    cursor.execute("INSERT into orders(customer_id, book_id, quantity, total, order_date) values(%s, %s, %s, %s, %s)",(customer_id, book_id, quantity, total, timestamp))
    return cursor.lastrowid  # Return the ID of the created order