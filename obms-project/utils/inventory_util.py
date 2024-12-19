def add_book_to_inventory_without_commit(mysql, book_id, total_stock):
    """
    Add book stock to the inventories without committing the transaction.

    Args:
    mysql: The Flask-MySQLDB object.
    book_id: The ID of the book.
    total_stock: The total stock of the book.

    Returns:
    None
    """
    cursor = mysql.connection.cursor()
    # Add book stock in inventories
    cursor.execute("INSERT INTO inventories (book_id, total_stock, sold_stock) VALUES(%s, %s, 0)", (book_id, total_stock))
    cursor.close()

def update_inventory_stock_without_commit(mysql, book_id, total_stock):
    """
    Update the inventory stock for a book without committing the transaction.

    Args:
    mysql: The Flask-MySQLDB object.
    book_id: The ID of the book to update the stock for.
    total_stock: The new total stock value for the book.

    Returns:
    None
    """
    cursor = mysql.connection.cursor()
    # Update the inventory stock
    cursor.execute("UPDATE inventories SET total_stock = %s WHERE book_id = %s", (book_data['stock'], book_id))
    cursor.close()

# Function to update the inventory for a specific book
def execute_inventory_stock_updates(cursor, book_id, quantity):
    # Update the soldStock for the specified book_id
    cursor.execute("UPDATE inventories set sold_stock = sold_stock + %s where book_id = %s", (quantity, book_id))
    
    # Update the totalStock for the specified book_id
    cursor.execute("UPDATE inventories set total_stock = total_stock - %s where book_id = %s", (quantity, book_id))