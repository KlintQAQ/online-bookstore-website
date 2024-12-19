def register_customer(mysql, user_data):
    """
    Register a new customer with the provided user data.

    Args:
    mysql: The Flask-MySQLDB object.
    user_data: A dictionary containing the user data including username, password, first name, last name, email, phone, and address.

    Returns:
    If the registration is successful, the function returns True. If an error occurs during the registration process, it returns False.
    """
    try:
        # Create a cursor to execute the SQL query
        cursor = mysql.connection.cursor()
        
        # Unpack the user_data dictionary for readability and pass the values to the SQL query
        query = "INSERT INTO customers (customer_username, customer_password, customer_first_name, customer_last_name, customer_email, customer_phone, customer_address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (user_data['username'], user_data['password'], user_data['first_name'], user_data['last_name'], user_data['email'], user_data['phone'], user_data['address'])
        
        # Execute the SQL query to insert a new customer into the database using user_data
        cursor.execute(query, values)
        
        # Commit the transaction
        mysql.connection.commit()
        
        # Close the cursor
        cursor.close()
        
        return True  # Customer registered successfully
    except Exception as e:
        # Print the exception for debugging purposes
        print(f"An error occurred: {e}")
        return False  # Failed to register customer

def customer_login(mysql, user_data):
    """
    Authenticate a customer with the provided username or email and password.

    Args:
    mysql: The Flask-MySQLDB object.
    user_data: A dictionary containing the user data including identifier and password.

    Returns:
    If the login is successful, the function returns the customer_id. If an error occurs during the login process, it returns None.
    """
    try:
        # Create a cursor to execute the SQL query
        cursor = mysql.connection.cursor()

        identifier = user_data['identifier']
        password = user_data['password']

        # Using parameterized query to prevent SQL injection
        query = "SELECT customer_id FROM customers WHERE (customer_username = %s OR customer_email = %s) AND customer_password = %s"
        cursor.execute(query, (identifier, identifier, password))

        # Fetch the customer_id
        customer_id = cursor.fetchone()

        # Close the cursor
        cursor.close()

        if customer_id:
            # Return customer_id if login is successful
            return customer_id[0]
        else:
            return None  # Return None if login is not successful
    except Exception as e:
        # Print the exception for debugging purposes
        print(f"An error occurred: {e}")
        return None  # Return None if an error occurs during login
    
def admin_login(mysql, user_data):
    """
    Authenticate an admin with the provided username and password.

    Args:
    mysql: The Flask-MySQLDB object.
    user_data: A dictionary containing the user data including identifier and password.

    Returns:
    If the login is successful, the function returns the admin_id. If an error occurs during the login process, it returns None.
    """
    try:
        # Create a cursor to execute the SQL query
        cursor = mysql.connection.cursor()

        identifier = user_data['identifier']
        password = user_data['password']
        
        # Execute the SQL query to retrieve admin_id based on the provided username and password
        cursor.execute("SELECT admin_id FROM admins WHERE admin_username = %s AND admin_password = %s", (identifier, password))
        
        # Fetch the admin_id
        admin_id = cursor.fetchone()
        
        # Close the cursor
        cursor.close()
        
        if admin_id:
            # Return admin_id if login is successful
            return admin_id[0]
        else:
            return None  # Return None if login is not successful
    except Exception as e:
        # Print the exception for debugging purposes
        print(f"An error occurred: {e}")
        return None  # Return None if an error occurs during login