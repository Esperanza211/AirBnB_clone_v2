-- creates the database hbnb_test_db and the user hbnb_test  if not exists
-- give all privileges on the database hbnb_test_db to hbnb_test 
-- give SELECT privilege on the database performance_schema to hbnb_test 
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
