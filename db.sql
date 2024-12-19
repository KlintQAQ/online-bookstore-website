/* Name: Online Bookstore Management System Database */

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`obms_db` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `obms_db`;

/* Table structure for table `authors` */
CREATE TABLE `authors` (
    `author_id` INT PRIMARY KEY AUTO_INCREMENT,
    `author_first_name` VARCHAR(20),
    `author_last_name` VARCHAR(20), 
    `author_address` VARCHAR(255),
    `author_url` VARCHAR(255)
);

/* Table structure for table `publishers` */
CREATE TABLE `publishers` (
    `publisher_id` INT PRIMARY KEY AUTO_INCREMENT,
    `publisher_name` VARCHAR(100) UNIQUE NOT NULL,
    `publisher_country` VARCHAR(255),
    `publisher_founded` INT,
    `publisher_url` VARCHAR(255),
    `publisher_phone` VARCHAR(20)
);

/* Table structure for table `books` */
CREATE TABLE `books` (
    `book_id` INT PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL,
    `isbn` VARCHAR(20) UNIQUE NOT NULL,
    `genre` VARCHAR(15),
    `year_of_publication` INT,
    `price` DECIMAL(10, 2),
    `author_id` INT,
    `publisher_id` INT,
    CONSTRAINT `fk_author_id` FOREIGN KEY (`author_id`) REFERENCES `authors`(`author_id`) ON DELETE SET NULL;,
    CONSTRAINT `fk_publisher_id` FOREIGN KEY (`publisher_id`) REFERENCES `publishers`(`publisher_id`) ON DELETE SET NULL;
);

CREATE TABLE admins (
    `admin_id` INT PRIMARY KEY AUTO_INCREMENT,
    `admin_username` VARCHAR(30) UNIQUE NOT NULL,
    `admin_password` VARCHAR(255) NOT NULL,
    `admin_email` VARCHAR(100) UNIQUE NOT NULL,
    `admin_first_name` VARCHAR(20),
    `admin_last_name` VARCHAR(20)
);

/* Table structure for table `customers` */
CREATE TABLE `customers` (
    `customer_id` INT PRIMARY KEY AUTO_INCREMENT,
    `customer_username` VARCHAR(30) UNIQUE NOT NULL,
    `customer_password` VARCHAR(30),
    `customer_first_name` VARCHAR(20),
    `customer_last_name` VARCHAR(20), 
    `customer_email` VARCHAR(100),
    `customer_phone` VARCHAR(20),
    `customer_address` VARCHAR(255)
);

/* Table structure for table `shopping_carts` */
CREATE TABLE `shopping_carts` (
    `cart_id` INT PRIMARY KEY AUTO_INCREMENT,
    `customer_id` INT,
    `book_id` INT,
    `quantity` INT CHECK (quantity >= 1),  -- Check constraint to enforce minimum quantity of 1
    FOREIGN KEY (`customer_id`) REFERENCES `customers`(`customer_id`) ON DELETE CASCADE,
    FOREIGN KEY (`book_id`) REFERENCES `books`(`book_id`) ON DELETE CASCADE
);

/* Table structure for table `inventories` */
CREATE TABLE `inventories` (
    `book_id` INT,
    `total_stock` INT,
    `sold_stock` INT,
    CONSTRAINT `fk_book_id_inventory` FOREIGN KEY (`book_id`) REFERENCES `books`(`book_id`) ON DELETE CASCADE
);

/* Table structure for table `orders` */
CREATE TABLE `orders` (
    `order_id` INT PRIMARY KEY AUTO_INCREMENT,
    `customer_id` INT,
    `book_id` INT,
    `quantity` INT NOT NULL, 
    `total` DECIMAL(10, 2),
    `order_date` DATETIME,
    CONSTRAINT `fk_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customers`(`customer_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_book_id_order` FOREIGN KEY (`book_id`) REFERENCES `books`(`book_id`) ON DELETE CASCADE
);

/* Table structure for table `payments` */
CREATE TABLE `payments` (
    `payment_id` INT PRIMARY KEY AUTO_INCREMENT,
    `order_id` INT,
    `payment_date` DATE,
    `amount` DECIMAL(10, 2),
    CONSTRAINT `fk_order_id_payment` FOREIGN KEY (`order_id`) REFERENCES `orders`(`order_id`) ON DELETE CASCADE
);

-- Insert sample data into the authors table
INSERT INTO authors (author_first_name, author_last_name, author_address, author_url) 
VALUES 
('John', 'Smith', '123 Main St, USA', 'www.johnsmith.com'),
('Emily', 'Johnson', '456 Elm St, Canada', 'www.emilyjohnson.com');

-- Insert sample data into the publishers table
INSERT INTO publishers (publisher_name, publisher_country, publisher_founded, publisher_url, publisher_phone) 
VALUES 
('ABC Books', 'USA', 1995, 'www.abcbooks.com', '+1-123-456-7890'),
('XYZ Publications', 'UK', 2000, 'www.xyzpublications.com', '+44-1234567890');

-- Use the sample author and publisher data to create sample books
-- Assuming the author_id and publisher_id are auto-incremented values from the previous inserts
INSERT INTO books (title, isbn, genre, year_of_publication, price, author_id, publisher_id) 
VALUES 
('Book 1', 'ISBN001', 'Fiction', 2005, 25.00, 1, 1),
('Book 2', 'ISBN002', 'Science Fiction', 2010, 30.00, 2, 2);

INSERT INTO admins (admin_username, admin_password, admin_email, admin_first_name, admin_last_name)
VALUES 
('admin1', 'password1', 'admin1@example.com', 'Admin', 'One'),
('admin2', 'password2', 'admin2@example.com', 'Admin', 'Two');

-- Insert sample data into the customers table
INSERT INTO customers (customer_username, customer_password, customer_first_name, customer_last_name, customer_email, customer_phone, customer_address) 
VALUES 
('alice123', 'password123', 'Alice', 'Smith', 'alice@example.com', '+1-123-456-7890', '123 Oak St, USA'),
('bob456', 'password456', 'Bob', 'Johnson', 'bob@example.com', '+1-987-654-3210', '456 Pine St, USA');

-- Use the sample customer data to create sample shopping cart items
-- Assuming the customer_id and book_id are auto-incremented values from the previous inserts
INSERT INTO shopping_carts (customer_id, book_id, quantity) 
VALUES 
(1, 1, 2),
(2, 2, 1);

-- Insert sample inventory data
INSERT INTO inventories (book_id, total_stock, sold_stock) 
VALUES 
(1, 100, 20),  -- Assuming book_id 1 corresponds to 'Book 1'
(2, 150, 30);  -- Assuming book_id 2 corresponds to 'Book 2'

-- Insert sample data into the orders table
INSERT INTO orders (customer_id, book_id, quantity, total, order_date) 
VALUES 
(1, 1, 2, 50.00, '2023-01-15 10:00:00'),
(2, 2, 1, 30.00, '2023-02-20 11:30:00');
