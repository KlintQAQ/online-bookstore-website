from flask import Flask, render_template, redirect, request, url_for, session, jsonify
from flask_mysqldb import MySQL

from utils import admin_util, authentication_util, book_util, checkout_util, customer_util, order_util, search_util, shopping_cart_util

app = Flask(__name__)

app.secret_key = '6b/{gr+b~2>7,Vx'

# MySQL configurations
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'obms_db'

mysql = MySQL(app)

@app.context_processor
def inject_user_info():
    if 'user_id' in session:  # Check if 'user_id' is in the session
        user_id = session['user_id']
        user_fullname = session.get('user_fullname', '')  # Get the user's full name from the session, default to empty string if not present
        account_type = session.get('account_type', '')  # Get the user's account type from the session, default to empty string if not present
    else:
        user_id = ''
        user_fullname = ''
        account_type = ''

    return dict(account_type=account_type, user_id=user_id, user_fullname=user_fullname)

@app.context_processor
def inject_cart_count():
    # Check if customer is logged in
    if 'user_id' in session and session['account_type'] == 'customer':    
        customer_id = session['user_id']
        cart_count = shopping_cart_util.get_cart_count_by_customer_id(mysql, customer_id)
    else:
        cart_count = 0
    
    return dict(cart_count=cart_count)

@app.route('/test-db-connection')
def test_db_connection():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        cur.close()
        return jsonify({'status': 'success', 'message': 'MySQL connection is successful'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Define a home page route
@app.route('/')
def home_route(): 
    books = book_util.all_books(mysql)
    return render_template('home.html', books=books)

# Define the dashboard route
@app.route('/dashboard')
def dashboard_route():
    # If the user is logged in and has a customer account type
    if 'user_id' in session and session['account_type'] == 'customer':    
        customer_id = session['user_id']
        customer_details = customer_util.get_customer_details(mysql, customer_id)
        orders_details = order_util.all_orders_by_customer(mysql, customer_id)
        return render_template('dashboard.html', customer=customer_details, orders=orders_details)
    else:
        # If the user is not logged in or does not have the appropriate account type, redirect to the login page
        return redirect(url_for('login_route'))

# Define a register page route
@app.route('/register', methods=['POST', 'GET'])
def register_route():
    if request.method == 'POST':
        # Get user input from the registration form
        user_data = {
            'username': request.form.get('username'),
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'phone': request.form.get('phone'),
            'address': request.form.get('address')
        }

        # Call the registration function with user data
        response = authentication_util.register_customer(mysql, user_data)

        # Handle the registration response
        if response:  # Registration successful
            return render_template('login.html', response=response)
        else:  # Registration failed
            return render_template('register.html', response=response)

    # Render the registration form for GET requests
    return render_template('register.html')

# Define a login page route
@app.route('/login', methods=['POST', 'GET'])
def login_route():
    if request.method == 'POST':
        user_data = {
            'identifier': request.form.get('username'),
            'password': request.form.get('password'),
            'account_type': request.form.get('account_type')
        }
        
        account_type = request.form.get('account_type')
        if account_type == 'customer':
            customer_id = authentication_util.customer_login(mysql, user_data)
            if customer_id is not None:  # Customer login successful
                # Get customer full name
                user_fullname = customer_util.get_customer_name_by_id(mysql, customer_id)

                # Create sessions for user data
                session['user_id'] = customer_id
                session['user_fullname'] = user_fullname
                session['account_type'] = user_data['account_type']
                
                return redirect(url_for('home_route'))
            else:  # Customer login failed
                return render_template('login.html')
        elif account_type == 'admin':
            admin_id = authentication_util.admin_login(mysql, user_data)
            if admin_id is not None:  # Admin login successful
                # Get admin full name
                user_fullname = admin_util.get_admin_name_by_id(mysql, admin_id)

                # Create sessions for user data
                session['user_id'] = admin_id
                session['user_fullname'] = user_fullname
                session['account_type'] = user_data['account_type']
                
                return redirect(url_for('home_route'))
            else:  # Admin login failed
                return render_template('login.html') 

        return redirect(url_for('login_route'))

    return render_template('login.html')

# Define a logout route
@app.route('/logout', methods=['GET', 'POST'])
def logout_route():
    # Clear the user's session data
    session.pop('user_id', None)  # Remove user_id from the session
    session.pop('user_fullname', None)  # Remove user_fullname from the session
    session.pop('account_type', None)  # Remove account_type from the session

    return redirect(url_for('login_route'))  # Redirect to the login page

# Define a cart route
@app.route('/cart', methods=['GET', 'POST'])
def cart_route():
    if 'user_id' in session and 'account_type' in session and session['account_type'] == 'customer':
        # User is logged in and has a customer account type
        customer_id = session['user_id']
        cart_items = shopping_cart_util.all_cart_items_for_cart(mysql, customer_id)
        total_price = sum(item['price'] * item['quantity'] for item in cart_items)
        print(cart_items, total_price)
        return render_template('cart.html', cart_items=cart_items, total_price=total_price)
    else:
        # User is not logged in or does not have a customer account type
        return redirect(url_for('login_route'))  # Redirect to the login page

# Define a home page route for admin
@app.route('/admin', methods=['POST','GET'])
def admin_index_route():
    books = book_util.all_books(mysql)
    return render_template('admin_index.html', books=books)

# Define Add/Delete/Update book page route for admin
@app.route('/books', methods=['POST', 'GET'])
def books_route():
    books = book_util.all_books(mysql)
    return render_template('books.html', books=books)

# Route to display a specific book
@app.route('/books/<int:book_id>', methods=['GET'])
def display_book_route(book_id):
    book = book_util.get_book(mysql, book_id)
    return render_template('book_details.html', book=book)

# Route to display the admin book management page
@app.route('/admin/books', methods=['GET'])
def admin_books_route():
    books = book_util.all_books(mysql)
    return render_template('admin_books.html', books=books)

# Route to add a new book
@app.route('/admin/books/add', methods=['GET', 'POST'])
def admin_add_book_route():
    if request.method == 'GET':        
        return render_template('admin_add_book_form.html')
    elif request.method == 'POST':
        book_util.add_book_with_auto_author_publisher_registration(mysql, request.form)
        return redirect(url_for('admin_books_route'))
    
# Route to edit a book
@app.route('/admin/books/edit/<int:book_id>', methods=['GET', 'POST'])
def admin_edit_book_route(book_id):
    if request.method == 'GET':
        book = book_util.get_book(mysql, book_id)
        print(book)
        return render_template('admin_edit_book_form.html', book=book)
    elif request.method == 'POST':
        book_util.edit_book_with_auto_author_publisher_registration(mysql, book_id, request.form)
        return redirect(url_for('admin_books_route'))
    
# Define the admin_remove_book route to handle book removal
@app.route('/admin/books/remove/<int:book_id>', methods=['POST'])
def admin_remove_book_route(book_id):
    book_util.remove_book(mysql, book_id)
    return redirect(url_for('admin_books_route'))

# Define add to the shopping cart route
@app.route('/add_to_cart/<int:book_id>/<int:quantity>', methods=['POST'])
def add_to_cart(book_id, quantity):
    if 'user_id' in session and 'account_type' in session and session['account_type'] == 'customer':
        # User is logged in and has a customer account type
        customer_id = session['user_id']
        # Check if the book already exists in the shopping cart for the customer
        existing_quantity = shopping_cart_util.get_book_quantity_in_cart(mysql, customer_id, book_id)
        if existing_quantity:
            # Book already exists in the cart, increase the quantity
            new_quantity = existing_quantity + quantity
            success = shopping_cart_util.update_cart_item_quantity(mysql, customer_id, book_id, new_quantity)
        else:
            # Book doesn't exist in the cart, add the book
            success = shopping_cart_util.add_to_cart(mysql, customer_id, book_id, quantity)
        if success:
            cart_count = shopping_cart_util.get_cart_count_by_customer_id(mysql, customer_id)
            return jsonify({
                'success': True, 
                'message': 'Book added to cart',
                'cart_count': cart_count
            })
        else:
            return jsonify({'success': False, 'message': 'Failed to add book to cart'})
    else:
        return jsonify({'success': False, 'message': 'Please login to continue'})

# Define remove from the shopping cart route
@app.route('/remove_from_cart/<int:book_id>', methods=['POST'])
def remove_from_cart_route(book_id):
    if 'user_id' in session and 'account_type':
        # User is logged in and has a customer account type
        customer_id = session['user_id'] 
        # Call the remove_from_cart function
        if shopping_cart_util.remove_from_cart(mysql, customer_id, book_id):
            return jsonify({"success": True, "message": "Book successfully removed from the cart."})
        else:
            return jsonify({"success": False, "message": "Failed to remove the book from the cart."})
    else:
        return jsonify({'success': False, 'message': 'User is not logged in as a customer'})

@app.route('/search', methods=['GET'])
def search_route():
    search_keyword = request.args.get('search_keyword')  # Get the search keyword from the query parameters
    if search_keyword:
        # Perform the search based on the book title
        books = search_util.search_books_by_title(mysql, search_keyword)
        return render_template('books.html', books=books, search_keyword=search_keyword)
    else:
        return render_template('books.html', books=[], search_keyword=None)
    
@app.route('/checkout_route', methods=['GET'])
def checkout_route():
    if 'user_id' in session and session['account_type'] == 'customer':    
        customer_id = session['user_id']
        checkout_util.checkout_all_carts(mysql, customer_id)
        
    return redirect(url_for('dashboard_route'))

if __name__ == '__main__':
    app.run(port=8000, debug=True)