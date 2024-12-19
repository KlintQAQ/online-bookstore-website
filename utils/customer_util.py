# Method to retrieve customer details
def get_customer_details(mysql, customer_id):
    """
    Retrieve customer details from the database.

    Args:
    mysql: The Flask-MySQLDB object.
    customer_id: ID of the customer

    Returns:
    dict: A dictionary containing the customer details with keys representing the column names
    """
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT customer_id, customer_username, customer_first_name, customer_last_name, customer_email, customer_phone, customer_address FROM customers WHERE customer_id = %s", (customer_id,))
    customer_data = cursor.fetchone()
    cursor.close()

    if customer_data:
        keys = ('customer_id', 'customer_username', 'customer_first_name', 'customer_last_name', 'customer_email', 'customer_phone', 'customer_address')
        return dict(zip(keys, customer_data))
    return None

def get_customer_name_by_id(mysql, customer_id):
    """
    Retrieve the full name of a customer by their ID.

    Args:
    mysql: The Flask-MySQLDB object.
    customer_id: The ID of the customer.

    Returns:
    The full name of the customer if found, or None if the customer is not found or an error occurs.
    """
    cursor = mysql.connection.cursor()

    try:
        # Execute the query to retrieve the customer's first name and last name by ID
        query = "SELECT customer_first_name, customer_last_name FROM customers WHERE customer_id = %s"
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()  # Fetch the first row

        if result:
            first_name, last_name = result
            name = first_name + " " + last_name
            return name  # Return the full name of the customer
        else:
            return None  # Return None if the customer is not found
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Return None if an error occurs
    finally:
        cursor.close()