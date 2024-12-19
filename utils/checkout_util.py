def checkout_all_carts(mysql, customer_id):
    """
    Process the checkout for all carts belonging to a specific customer.

    Args:
    mysql: The Flask-MySQLDB object.
    customer_id (int): The ID of the customer whose carts are to be processed.

    Returns:
    list: A list of boolean values indicating the success or failure of the checkout for each cart.

    This method retrieves all carts for the specified customer and iterates through each cart to perform the checkout using the checkout_single_cart method.
    It returns a list of boolean values, where True represents a successful checkout and False represents a failed checkout for each cart.
    In case of an error during the checkout process, a list of False values is returned.
    """
    try:
        cur = mysql.connection.cursor()
        # Get all carts for the customer
        cur.execute("SELECT cart_id FROM shopping_carts WHERE customer_id = %s", (customer_id,))
        carts = cur.fetchall()
        results = []
        for cart in carts:
            result = checkout_single_cart(mysql, cart[0])
            results.append(result)
        return results
    except Exception as e:
        print(f"An error occurred checkout_all_carts: {e}")
        return [False] * len(carts)  # Return a list of False values if an error occurs
    finally:
        cur.close()

def checkout_single_cart(mysql, cart_id):
    """
    Process the checkout for a single cart.

    Args:
    mysql: The Flask-MySQLDB object.
    cart_id (int): The ID of the cart to be processed.

    Returns:
    bool: True if the transaction is successful, False otherwise.

    This method retrieves the details of the specified cart and processes the checkout by creating an order, updating the inventory, and creating a payment. 
    It uses a transaction to ensure the integrity of the database operations. 
    If the cart is not found or if there is not enough stock in the inventory, the transaction is rolled back, and False is returned.
    """
    try:
        # Start the transaction
        cur = mysql.connection.cursor()

        cur.execute("START TRANSACTION")

        # Get cart details
        cur.execute("SELECT customer_id, book_id, quantity FROM shopping_carts WHERE cart_id = %s", (cart_id,))
        cart = cur.fetchone()
        if cart:
            customer_id = cart[0]
            book_id = cart[1]
            quantity = cart[2]
            
            # Calculate total based on the book price and quantity
            cur.execute("SELECT price FROM books WHERE book_id = %s", (book_id,))
            book_price = cur.fetchone()[0]
            total = book_price * quantity
            
            # Delete cart
            cur.execute("DELETE FROM shopping_carts WHERE cart_id = %s", (cart_id,))

            # Create order
            cur.execute("INSERT INTO orders (customer_id, book_id, quantity, total, order_date) VALUES (%s, %s, %s, %s, NOW())", (customer_id, book_id, quantity, total))
            
            # Get the order_id of the newly created order
            order_id = cur.lastrowid

            # Check if inventories have enough stock
            cur.execute("SELECT total_stock FROM inventories WHERE book_id = %s", (book_id,))
            row = cur.fetchone()

            if row and row[0] >= int(quantity):
                # Update inventory
                cur.execute("UPDATE inventories SET sold_stock = sold_stock + %s, total_stock = total_stock - %s WHERE book_id = %s", (quantity, quantity, book_id))

                # Create payment using the obtained order_id
                cur.execute("INSERT INTO payments (order_id, amount, payment_date) VALUES (%s, %s, NOW())", (order_id, total))

                # Commit the transaction
                mysql.connection.commit()

                return True
            else:
                # Rollback the transaction and return False
                mysql.connection.rollback()
                return False
        else:
            return False
    except Exception as e:
        print(f"An error occurred in checkout_single_cart: {e}")
        # Rollback the transaction in case of any error and return False
        mysql.connection.rollback()
        return False
    finally:
        # Close the cursor
        cur.close()