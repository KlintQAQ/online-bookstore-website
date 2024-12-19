def add_to_cart(mysql, customer_id, book_id, quantity):
    """
    Add a book to the shopping cart for a specific customer.

    Args:
    mysql: The Flask-MySQLDB object.
    customer_id: The ID of the customer adding the book to the cart.
    book_id: The ID of the book to be added to the cart.
    quantity: The quantity of the book to be added to the cart.

    Returns:
    True if the book is added to the cart successfully, False if an error occurs during the process.
    """
    try:
        # Create a cursor to execute the SQL query
        cursor = mysql.connection.cursor()
        
        # Execute the SQL query to insert the book into the shopping cart
        cursor.execute("INSERT INTO shopping_carts (customer_id, book_id, quantity) VALUES (%s, %s, %s)", (customer_id, book_id, quantity))
        
        # Commit the transaction
        mysql.connection.commit()
        
        # Close the cursor
        cursor.close()
        
        return True  # Book added to the cart successfully
    except Exception as e:
        # Print the exception for debugging purposes
        print(f"An error occurred: {e}")
        return False  # Failed to add the book to the cart

def update_cart_item_quantity(mysql, customer_id, book_id, quantity):
    """
    Update the quantity of a specific item in the shopping cart.

    Args:
    mysql: The Flask-MySQLDB object.
    customer_id: The ID of the customer.
    book_id: The ID of the book in the shopping cart.
    quantity: The new quantity of the item.

    Returns:
    True if the item quantity is updated successfully, False if an error occurs during the process.
    """
    try:
        # Create a cursor to execute the SQL query
        cursor = mysql.connection.cursor()
        
        # Execute the SQL query to update the quantity of the item in the shopping cart
        cursor.execute("UPDATE shopping_carts SET quantity = %s WHERE customer_id = %s AND book_id = %s", (quantity, customer_id, book_id))
        
        # Commit the transaction
        mysql.connection.commit()
        
        # Close the cursor
        cursor.close()
        
        return True  # Cart item quantity updated successfully
    except Exception as e:
        # Print the exception for debugging purposes
        print(f"An error occurred: {e}")
        return False  # Failed to update cart item quantity

def remove_from_cart(mysql, customer_id, book_id):
    """
    Remove a book from the customer's shopping cart.

    Args:
    mysql: The Flask-MySQLDB object.
    customer_id: The ID of the customer whose cart is being modified.
    book_id: The ID of the book to be removed from the cart.

    Returns:
    True if the book is successfully removed from the cart, False otherwise.
    """
    try:
        # Create a cursor to execute the SQL query
        cursor = mysql.connection.cursor()

        # Execute the SQL query to remove the book from the customer's cart
        cursor.execute("DELETE FROM shopping_carts WHERE customer_id = %s AND book_id = %s", (customer_id, book_id))

        # Commit the transaction
        mysql.connection.commit()

        # Close the cursor
        cursor.close()

        return True  # Return True indicating successful removal from the cart
    except Exception as e:
        # Print the exception for debugging purposes
        print(f"An error occurred: {e}a")
        return False  # Return False if an error occurs during removal

def all_cart_items(mysql, customer_id):
    """
    Retrieve the items in the shopping cart for a specific customer.

    Args:
    mysql: The Flask-MySQLDB object.
    customer_id: The ID of the customer whose shopping carts are to be retrieved.

    Returns:
    On success, returns a list of shopping carts. On failure, returns an empty list.
    """
    try:
        # Create a cursor to execute the SQL query
        cursor = mysql.connection.cursor()
        
        # Execute the SQL query to retrieve the shopping carts for the customer
        cursor.execute("SELECT * FROM shopping_carts WHERE customer_id = %s", (customer_id,))
        
        # Fetch the shopping carts
        cart_items = cursor.fetchall()
        
        # Close the cursor
        cursor.close()
        
        return cart_items
    except Exception as e:
        # Print the exception for debugging purposes
        print(f"An error occurred: {e}")
        return []  # Return an empty list if an error occurs during retrieval
    
def all_cart_items_for_cart(mysql, customer_id):
    """
    Retrieve the items in the shopping cart for a specific customer intended for the cart process.

    Args:
    mysql: The Flask-MySQLDB object.
    customer_id: The ID of the customer whose shopping carts are to be retrieved for cart.

    Returns:
    On success, returns a list of shopping carts specifically for the cart process.
    On failure, returns an empty list.
    """
    try:
        # Create a cursor to execute the SQL query
        cursor = mysql.connection.cursor()

        # Execute the SQL query to retrieve shopping carts with book details
        cursor.execute("""
            SELECT 
                books.book_id,
                books.title, 
                books.price, 
                authors.author_first_name, 
                authors.author_last_name, 
                publishers.publisher_name,
                shopping_carts.quantity
            FROM shopping_carts 
            INNER JOIN books ON shopping_carts.book_id = books.book_id 
            INNER JOIN authors ON books.author_id = authors.author_id 
            INNER JOIN publishers ON books.publisher_id = publishers.publisher_id 
            WHERE shopping_carts.customer_id = %s
        """, (customer_id,))

        # Fetch all the results and get the column names
        cart_items_data = cursor.fetchall()
        columns = [col[0] for col in cursor.description]  # Get the column names

        # Convert the result to a list of dictionaries
        cart_items = []
        for row in cart_items_data:
            cart_item_dict = dict(zip(columns, row))
            cart_items.append(cart_item_dict)

        cursor.close()
        return cart_items
    except Exception as e:
        # Handle any exceptions and return an empty list
        print(f"An error occurred: {e}")
        return []
    
def get_cart_count_by_customer_id(mysql, customer_id):
    """
    This method retrieves the length of the shopping carts for a specific customer from a MySQL database.

    Parameters:
    mysql: The Flask-MySQLDB object.
    customer_id: The ID of the customer for whom the cart length is to be retrieved.

    Returns:
    The length of the shopping carts for the specific customer, or None if an error occurs.
    """
    try:
        # Establish a connection cursor to the MySQL database
        cursor = mysql.connection.cursor()

        # Execute the query to retrieve the length of the shopping carts for the specific customer
        query = "SELECT COUNT(*) FROM shopping_carts WHERE customer_id = %s"
        cursor.execute(query, (customer_id,))
        cart_count = cursor.fetchone()[0]  # Fetch the count from the first row

        # Return the length of the shopping carts for the specific customer
        return cart_count
    except Exception as e:
        # Print the error message if an exception occurs
        print(f"An error occurred: {e}")
        return None
    finally:
        # Close the cursor and the database connection
        cursor.close()

def get_book_quantity_in_cart(mysql, customer_id, book_id):
    """
    Retrieve the quantity of a specific book in the customer's shopping cart from a MySQL database.

    Args:
    mysql: The Flask-MySQLDB object.
    customer_id: The ID of the customer.
    book_id: The ID of the book.

    Returns:
    The quantity of the specified book in the customer's shopping cart if it exists; otherwise, returns None.
    """
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT quantity FROM shopping_carts WHERE customer_id = %s AND book_id = %s", (customer_id, book_id))
    quantity = cursor.fetchone()
    cursor.close()
    if quantity:
        return quantity[0]  # Return the quantity if the book exists in the cart
    else:
        return None  # Return None if the book does not exist in the cart