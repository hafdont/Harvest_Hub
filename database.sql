-- Create database (replace 'ecommerce.db' with your desired filename)
CREATE TABLE IF NOT EXISTS Harvest_hub.db;

-- Use the created database
USE Harvest_hub;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL  -- Consider storing hashed password for security
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  location TEXT NOT NULL,
  price REAL NOT NULL,
  seller_id INTEGER NOT NULL,
  FOREIGN KEY (seller_id) REFERENCES users(id)
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  status TEXT NOT NULL,  -- Add options like 'pending', 'shipped', 'delivered'
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (product_id) REFERENCES products(id)
);
