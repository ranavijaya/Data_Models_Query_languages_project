CREATE TABLE products(
	product_id SERIAL PRIMARY KEY,
	product_name VARCHAR(32),
	product_category VARCHAR(32),
	price REAL,
	quantity_in_stock INT, 
	seller_id INT
);

CREATE TABLE customers(
	customer_id INT PRIMARY KEY,
	customer_city VARCHAR(20),
	customer_state VARCHAR(3)
);

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE order_items(
	order_item_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	order_id INT,
	product_id INT,
	quantity INT,
	FOREIGN KEY (product_id) REFERENCES products(product_id)
	
);

CREATE TABLE orders(
	order_id INT PRIMARY KEY,
	customer_id INT,
	purchase_time DATE,
	payment_type VARCHAR(20),
	FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
	FOREIGN KEY (order_id)   REFERENCES orders(order_id)
);


CREATE TABLE distances(
	dist_id INT PRIMARY KEY,
	customer_city VARCHAR(20)A,
	seller_city VARCHAR(20),
	time_to_deliver INT,
	seller_id INT
	
);