def search_books_by_title(mysql, query):
    """
    Search for books by title matching a specific query and retrieve their details including author and publisher information.

    Args:
    mysql: The Flask-MySQLDB object.
    query: The search query for the book title.

    Returns:
    A list of dictionaries, where each dictionary represents a book and its details.
    """
    try:
        cursor = mysql.connection.cursor()
        
        # Search for books by title matching the query and retrieve book details along with author and publisher information
        cursor.execute("""
            SELECT b.book_id, a.author_id, b.publisher_id, p.publisher_name, b.title, b.isbn, b.genre, b.year_of_publication, b.price, a.author_first_name, a.author_last_name
            FROM books AS b
            JOIN authors AS a ON b.author_id = a.author_id
            JOIN publishers AS p ON b.publisher_id = p.publisher_id
            WHERE  b.title LIKE %s
        """, ('%' + query + '%',))

        # Fetch all the results and get the column names
        books_data = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

        # Convert the result to a list of dictionaries and return
        books_list = []
        for row in books_data:
            book_dict = dict(zip(columns, row))
            books_list.append(book_dict)

        # Close the cursor
        cursor.close()

        return books_list
    except Exception as e:
        # Print the exception for debugging purposes
        print(f"An error occurred: {e}")
        return []  # Return an empty list if an error occurs