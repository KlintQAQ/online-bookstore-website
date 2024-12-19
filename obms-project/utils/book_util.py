from utils.author_util import create_author_by_name_if_not_exists_without_commit
from utils.publisher_util import create_publisher_by_name_if_not_exists_without_commit
from utils.inventory_util import add_book_to_inventory_without_commit

def add_book_with_auto_author_publisher_registration(mysql, book_data):
    """
    Add a book to the database along with its author and publisher, and its stock to the Inventory if they do not already exist.
    Args:
    mysql: The Flask-MySQLDB object.
    book_data: A dictionary containing the book information including 'book_id', 'title', 'isbn', 'genre', 'publication_year', 'price', 'author_first_name', 'author_last_name', 'publisher_name', and 'stock'.
    Returns:
    True if the book is added successfully, False if the book failed to add.
    """
    cursor = mysql.connection.cursor()
    try:
        # Start a transaction
        cursor.execute("START TRANSACTION")

        author_id = create_author_by_name_if_not_exists_without_commit(mysql, book_data['author_first_name'], book_data['author_last_name'])
        publisher_id = create_publisher_by_name_if_not_exists_without_commit(mysql, book_data['publisher_name'])

        book_info = {
            'title': book_data['title'],
            'isbn': book_data['isbn'],
            'genre': book_data['genre'],
            'year_of_publication': book_data['year_of_publication'],
            'price': book_data['price'],
            'author_id': author_id,
            'publisher_id': publisher_id
        }

        book_id = create_book_without_commit(mysql, book_info)
        if book_id is not None:
            add_book_to_inventory_without_commit(mysql, book_id, book_data['stock'])
            mysql.connection.commit()
            return True  # Book added successfully to both Books and Inventory
        else:
            # Roll back the transaction if there's an issue with adding to Inventory
            mysql.connection.rollback()
            return False  # Book added to Books but failed to add to Inventory
    except Exception as e:
        print(f"An error occurred: {e}")
        # Roll back the transaction if there's an exception
        mysql.connection.rollback()
        return False  # Book failed to add
    finally:
        cursor.close()

def edit_book_with_auto_author_publisher_registration(mysql, book_id, book_data):
    """
    Edit a book in the database along with its author and publisher, and its stock in the Inventory if they do not already exist.

    Args:
    mysql: The Flask-MySQLDB object.
    book_id: The ID of the book to be edited.
    book_data: A dictionary containing the updated book information including 'title', 'isbn', 'genre', 'publication_year', 'price', 'author_first_name', 'author_last_name', 'publisher_name', and 'stock'.

    Returns:
    True if the book is edited successfully, False if the book failed to edit.
    """
    cursor = mysql.connection.cursor()
    try:
        # Start a transaction
        cursor.execute("START TRANSACTION")

        author_id = create_author_by_name_if_not_exists_without_commit(mysql, book_data['author_first_name'], book_data['author_last_name'])
        publisher_id = create_publisher_by_name_if_not_exists_without_commit(mysql, book_data['publisher_name'])

        book_info = {
            'title': book_data['title'],
            'isbn': book_data['isbn'],
            'genre': book_data['genre'],
            'year_of_publication': book_data['year_of_publication'],
            'price': book_data['price'],
            'author_id': author_id,
            'publisher_id': publisher_id
        }

        # Update the book information without committing
        update_book_without_commit(mysql, book_id, book_info)

        mysql.connection.commit()
        return True  # Book edited successfully
    except Exception as e:
        print(f"An error occurred: {e}")
        # Roll back the transaction if there's an exception
        try:
            mysql.connection.rollback()
        except Exception as rollback_error:
            print(f"An error occurred during rollback: {rollback_error}")
        return False  # Book failed to edit
    finally:
        cursor.close()

def add_book(mysql, book_data):
    """
    Add a book to the database along with its author and publisher, and its stock to the Inventory if they do not already exist.

    Args:
    mysql: The Flask-MySQLDB object.
    book_data: A dictionary containing the book information including 'title', 'isbn', 'genre', 'year_of_publication', 'price', 'author_id', and 'publisher_id'.

    Returns:
    True if the book is added successfully, False if the book failed to add.
    """
    cursor = mysql.connection.cursor()
    try:
        # Add book in Books table
        cursor.execute("INSERT INTO books(title, isbn, genre, year_of_publication, price, author_id, publisher_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (book_data['title'], book_data['isbn'], book_data['genre'], book_data['year_of_publication'], book_data['price'], book_data['author_id'], book_data['publisher_id']))

        mysql.connection.commit()
        cursor.close()
        return True  # Book added successfully
    except Exception as e:
        print(f"An error occurred: {e}")
        cursor.close()
        return False  # Book failed to add
    
def create_book_without_commit(mysql, book_data):
    """
    Add a book to the database along with its author and publisher, and return the book_id of the newly added book.

    Args:
    mysql: The Flask-MySQLDB object.
    book_data: A dictionary containing the book information including 'title', 'isbn', 'genre', 'year_of_publication', 'price', 'author_id', and 'publisher_id'.

    Returns:
    The book_id of the newly added book if the addition is successful, None if the addition failed.
    """
    cursor = mysql.connection.cursor()
    
    # Add book in Books table
    cursor.execute("INSERT INTO books(title, isbn, genre, year_of_publication, price, author_id, publisher_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (book_data['title'], book_data['isbn'], book_data['genre'], book_data['year_of_publication'], book_data['price'], book_data['author_id'], book_data['publisher_id']))

    book_id = cursor.lastrowid  # Retrieve the book_id of the newly added book
    cursor.close()
    return book_id  # Return the book_id of the newly added book

def update_book_without_commit(mysql, book_id, book_data):
    """
    Update the book information in the database without committing the transaction.

    Args:
    mysql: The Flask-MySQLDB object.
    book_id: The ID of the book to be updated.
    book_data: A dictionary containing the updated book information including 'title', 'isbn', 'genre', 'year_of_publication', 'price', 'author_id', 'publisher_id'.

    Returns:
    None
    """
    cursor = mysql.connection.cursor()
    # Update the book information
    cursor.execute("UPDATE books SET title = %s, isbn = %s, genre = %s, year_of_publication = %s, price = %s, author_id = %s, publisher_id = %s WHERE book_id = %s", 
                    (book_data['title'], book_data['isbn'], book_data['genre'], book_data['year_of_publication'], book_data['price'], book_data['author_id'], book_data['publisher_id'], book_id))
    cursor.close()

def all_books(mysql):
    """
    Fetches all book data including author and publisher details from the database.

    Args:
    mysql: The Flask-MySQLDB object.

    Returns:
    list: A list of dictionaries containing the fetched book data including publisher name.
    """

    # Get a cursor to interact with the database
    cur = mysql.connection.cursor()

    # Execute the SQL query to fetch all book data including author, publisher details
    cur.execute("""
        SELECT b.book_id, a.author_id, b.publisher_id, p.publisher_name, b.title, b.isbn, b.genre, b.year_of_publication, b.price, a.author_first_name, a.author_last_name
        FROM books as b
        INNER JOIN authors as a ON b.author_id = a.author_id
        INNER JOIN publishers as p ON b.publisher_id = p.publisher_id
        ORDER BY book_id
    """)

    # Fetch all the results and get the column names
    books_data = cur.fetchall()
    columns = [col[0] for col in cur.description]

    # Convert the result to a list of dictionaries and return
    books_list = []
    for row in books_data:
        book_dict = dict(zip(columns, row))
        books_list.append(book_dict)

    # Close the cursor
    cur.close()

    return books_list

def get_book(mysql, book_id):
    """
    Retrieve book details from the database for a specific book ID.

    Args:
    mysql: The Flask-MySQLDB object.
    book_id: The ID of the book to retrieve.

    Returns:
    If the book is found, returns a dictionary containing the book details.
    If the book is not found, returns None.
    """
    cursor = mysql.connection.cursor()
    try:
        # Retrieve book details from the Books, Authors, and Publishers tables
        cursor.execute("""
            SELECT b.book_id, a.author_id, b.publisher_id, p.publisher_name, b.title, b.isbn, b.genre, b.year_of_publication, b.price, a.author_first_name, a.author_last_name
            FROM books b
            INNER JOIN authors a ON b.author_id = a.author_id
            INNER JOIN publishers p ON b.publisher_id = p.publisher_id
            WHERE b.book_id = %s
        """, (book_id,))
        book_data = cursor.fetchone()

        cursor.close()

        if book_data:
            book_details = {
                'book_id': book_data[0],
                'author_id': book_data[1],
                'publisher_id': book_data[2],
                'publisher_name': book_data[3],
                'title': book_data[4],
                'isbn': book_data[5],
                'genre': book_data[6],
                'year_of_publication': book_data[7],
                'price': book_data[8],
                'author_first_name': book_data[9],
                'author_last_name': book_data[10]
            }
            return book_details  # Return book details as a dictionary if found
        else:
            return None  # Return None if the book is not found
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Return None if an error occurs
    
def remove_book(mysql, book_id):
    """
    Remove a book from the database, triggering cascading deletion of related records in child tables.

    Args:
    mysql: The Flask-MySQLDB object.
    book_id: The ID of the book to be removed.

    Returns:
    True if the book is removed successfully, False if the removal failed.
    """
    cursor = mysql.connection.cursor()
    try:
        # Remove book from Books table, triggering cascading deletion of related records in child tables
        cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))

        mysql.connection.commit()
        cursor.close()
        return True  # Book removed successfully, along with related records in child tables
    except Exception as e:
        print(f"An error occurred: {e}")
        cursor.close()
        return False  # Removal failed