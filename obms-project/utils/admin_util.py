# Method to retrieve admin details
def get_admin_details(mysql, admin_id):
    """
    Retrieve admin details from the database.

    Args:
    mysql: The Flask-MySQLDB object.
    admin_id: ID of the admin

    Returns:
    dict: A dictionary containing the admin details with keys representing the column names
    """
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT admin_id, admin_username, admin_first_name, admin_last_name, admin_email FROM admins WHERE admin_id = %s", (admin_id,))
    admin_data = cursor.fetchone()
    cursor.close()

    if admin_data:
        keys = ('admin_id', 'admin_username', 'admin_first_name', 'admin_last_name', 'admin_email')
        return dict(zip(keys, admin_data))
    return None

def get_admin_name_by_id(mysql, admin_id):
    """
    Retrieve the full name of a admin by their ID.

    Args:
    mysql: The Flask-MySQLDB object.
    admin_id: The ID of the admin.

    Returns:
    The full name of the admin if found, or None if the admin is not found or an error occurs.
    """
    cursor = mysql.connection.cursor()

    try:
        # Execute the query to retrieve the admin's first name and last name by ID
        query = "SELECT admin_first_name, admin_last_name FROM admins WHERE admin_id = %s"
        cursor.execute(query, (admin_id,))
        result = cursor.fetchone()  # Fetch the first row

        if result:
            first_name, last_name = result
            name = first_name + " " + last_name
            return name  # Return the full name of the admin
        else:
            return None  # Return None if the admin is not found
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Return None if an error occurs
    finally:
        cursor.close()