# shopkeeperapp
-
CREATE DATABASE shopkeeper;
USE shopkeeper;
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10, 2),
    quantity INT,
    description TEXT,
    image_path VARCHAR(255)
);
-