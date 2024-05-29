-- Create database (replace 'ecommerce.db' with your desired filename)
CREATE DATABASE IF NOT EXISTS Harvest_hub.db;

-- Use the created database
USE Harvest_hub;

-- Create users table
CREATE TABLE users (
    user_id INT NOT NULL PRIMARY KEY,
    username CHAR(10) NOT NULL,
    firstname CHAR(10) NOT NULL,
    lastname CHAR(10) NOT NULL,
    password CHAR(10) NOT NULL,
    email CHAR(10) NOT NULL,
    role CHAR(10) NOT NULL,
    status CHAR(50) NOT NULL,
    profile_picture IMAGE NOT NULL
);


-- Create products table
CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  location TEXT NOT NULL,
  description CHAR(300) NOT NULL,
  available DATE NOT NULL,
  negotiation BOOLEAN NOT NULL,
  price REAL NOT NULL,
  seller_id INTEGER NOT NULL,
  image_gallery IMAGE,
  FOREIGN KEY (seller_id) REFERENCES user_(id)
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
  order_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  buyer_id INTEGER NOT NULL,
  seller_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  order_date TIMESTAMP NOT NULL,
  total_price INTEGER NOT NULL,
  
  status TEXT NOT NULL,  -- Add options like 'pending', 'shipped', 'delivered'
  FOREIGN KEY (buyer_id) REFERENCES users(id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
  FOREIGN KEY (seller_id) REFERENCES users(user_id)
  FOREIGN KEY (product_id) REFERENCES products(id)
);
