CREATE DATABASE IF NOT EXISTS furniture_reservation_system;

USE furniture_reservation_system;

-- Create a table for customers
CREATE TABLE IF NOT EXISTS customers (
                                         customer_id INT AUTO_INCREMENT PRIMARY KEY,
                                         first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL
    );

-- Create a table for furniture products
CREATE TABLE IF NOT EXISTS furniture (
                                         product_id INT AUTO_INCREMENT PRIMARY KEY,
                                         product_name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL
    );

-- Create a table for orders
CREATE TABLE IF NOT EXISTS orders (
                                      order_id INT AUTO_INCREMENT PRIMARY KEY,
                                      customer_id INT NOT NULL,
                                      order_date DATE NOT NULL,
                                      total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );

-- Create a table for order items (to represent products in each order)
CREATE TABLE IF NOT EXISTS order_items (
                                           item_id INT AUTO_INCREMENT PRIMARY KEY,
                                           order_id INT NOT NULL,
                                           product_id INT NOT NULL,
                                           quantity INT NOT NULL,
                                           FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES furniture(product_id)
    );



-- Insert sample data into the customers table
INSERT INTO customers (first_name, last_name, email, phone_number)
VALUES
    ('John', 'Doe', 'john@example.com', '123-456-7890'),
    ('Jane', 'Smith', 'jane@example.com', '987-654-3210');


INSERT INTO furniture (product_name, description, price)
VALUES
    ('Sofa', 'Comfortable three-seater sofa', 499.99),
    ('Dining Table', 'Wooden dining table with 4 chairs', 299.99),
    ('Bed', 'Queen-sized bed with memory foam mattress', 699.99),
    ('Coffee Table', 'Modern glass coffee table', 149.99),
    ('Bookshelf', 'Wooden bookshelf with adjustable shelves', 179.99),
    ('Office Chair', 'Ergonomic office chair with lumbar support', 249.99),
    ('Wardrobe', 'Large wardrobe with sliding doors', 599.99),
    ('TV Stand', 'TV stand with storage shelves', 199.99),
    ('Recliner Sofa', 'Reclining sofa with leather upholstery', 799.99),
    ('Kitchen Table', 'Round kitchen table with 4 chairs', 399.99),
    ('Nightstand', 'Bedside nightstand with drawer', 69.99),
    ('Dresser', 'Dresser with mirror and multiple drawers', 349.99),
    ('Computer Desk', 'Corner computer desk with keyboard tray', 159.99);


-- Insert sample data into the orders table
INSERT INTO orders (customer_id, order_date, total_amount)
VALUES
    (1, '2023-01-10', 499.99),
    (2, '2023-02-05', 999.98),
    (1, '2023-03-20', 749.98), -- John's second order
    (2, '2023-03-22', 899.97), -- Jane's second order
    (1, '2023-04-05', 949.96), -- John's third order
    (2, '2023-04-10', 1249.95); -- Jane's third order


-- Insert sample data into the order_items table
INSERT INTO order_items (order_id, product_id, quantity)
VALUES
    (1, 1, 1),
    (2, 2, 1),
    (2, 3, 2),
    (3, 4, 1),  -- John's second order - Wardrobe
    (3, 8, 2),  -- John's second order - Nightstand
    (4, 5, 1),  -- Jane's second order - TV Stand
    (4, 6, 1),  -- Jane's second order - Recliner Sofa
    (5, 2, 1),  -- John's third order - Bookshelf
    (5, 9, 2),  -- John's third order - Dresser
    (6, 3, 1),  -- Jane's third order - Office Chair
    (6, 7, 1);  -- Jane's third order - Kitchen Table

