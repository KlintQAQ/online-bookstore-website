def get_author_id_by_name(cur, first_name, last_name):
    """
    Retrieve the author ID from the authors table based on the first name and last name.

    Args:
    cur: The database cursor object.
    first_name: The first name of the author.
    last_name: The last name of the author.

    Returns:
    The author ID if found, or None if not found.
    """
    cur.execute("SELECT author_id from authors WHERE author_first_name = %s AND author_last_name = %s", (first_name, last_name,))
    author_id = cur.fetchone()
    return author_id[0] if author_id else None

def create_author_without_commit(mysql, author_data):
    """
    Create a new author in the database using the provided author data.

    Args:
    mysql: The Flask-MySQLDB object.
    author_data: A dictionary containing the author data including 'first_name', 'last_name', 'address', and 'url'.

    Returns:
    The ID of the newly created author.
    """
    cursor = mysql.connection.cursor()
    query = "INSERT INTO authors(author_first_name, author_last_name, author_address, author_url) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (author_data['author_first_name'], author_data['author_last_name'], author_data['author_address'], author_data['author_url']))
    author_id = cursor.lastrowid
    cursor.close()
    return author_id

def create_author_by_name_if_not_exists_without_commit(mysql, first_name, last_name):
    """
    Add an author to the database if they do not already exist, based on the author's first name and last name.

    Args:
    mysql: The Flask-MySQLDB object.
    first_name: The first name of the author to be added.
    last_name: The last name of the author to be added.

    Returns:
    If the author is added, returns the last inserted author_id.
    If the author already exists, returns the existing author_id.
    """
    cursor = mysql.connection.cursor()
    author_id = get_author_id_by_name(cursor, first_name, last_name)
    
    if not author_id:
        author_data = {'author_first_name': first_name, 'author_last_name': last_name, 'author_address': '', 'author_url': ''}
        author_id = create_author_without_commit(mysql, author_data)
        cursor.close()
        return author_id
    else:
        cursor.close()
        return author_id  # Return the existing author_id if found