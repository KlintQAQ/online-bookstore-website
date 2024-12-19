def get_publisher_id_by_name(mysql, publisher_name):
    """
    Retrieve the publisher ID based on the publisher name.

    Args:
    mysql: The Flask-MySQLDB object.
    publisher_name: The name of the publisher.

    Returns:
    A tuple containing the publisher ID if found, or None if not found.
    """
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT publisher_id from publishers WHERE publisher_name = %s", (publisher_name,))
    publisher = cursor.fetchone()
    cursor.close()
    return publisher


def create_publisher_without_commit(mysql, publisher_data):
    """
    Create a new publisher in the database using the provided publisher data.

    Args:
    mysql: The Flask-MySQLDB object.
    publisher_data: A dictionary containing the publisher data including 'name', 'country', 'founded', 'url', and 'phone'.

    Returns:
    The ID of the newly created publisher.
    """
    cursor = mysql.connection.cursor()
    query = "INSERT INTO publishers(publisher_name, publisher_country, publisher_founded, publisher_url, publisher_phone) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (publisher_data['name'], publisher_data['country'], publisher_data['founded'], publisher_data['url'], publisher_data['phone']))
    publisher_id = cursor.lastrowid
    cursor.close()
    return publisher_id

def create_publisher_by_name_if_not_exists_without_commit(mysql, publisher_name):
    """
    Add a publisher to the database if it does not already exist, based on the publisher name.

    Args:
    mysql: The Flask-MySQLDB object.
    publisher_name: The name of the publisher to be added.

    Returns:
    If the publisher is added, returns the last inserted publisher_id. 
    If the publisher already exists, returns the existing publisher_id.
    """
    cursor = mysql.connection.cursor()
    publisher = get_publisher_id_by_name(cursor, publisher_name)
    if not publisher:
        publisher_id = create_publisher_without_commit(mysql, {'name': publisher_name, 'country': '', 'founded': 0, 'url': '', 'phone': ''})
        cursor.close()
        return publisher_id
    else:
        cursor.close()
        return publisher[0]  # Return the existing publisher_id if found