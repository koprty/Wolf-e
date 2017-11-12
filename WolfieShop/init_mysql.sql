CREATE DATABASE wolfieshop_db;
CREATE USER 'lal'@'localhost' IDENTIFIED BY 'ALL305';
GRANT ALL PRIVILEGES ON wolfieshop_db.* TO 'lal'@'localhost';
FLUSH PRIVILEGES;
quit
