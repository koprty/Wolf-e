
GRANT ALL PRIVILEGES ON wolfieshop_db.* TO ''@'localhost';
#GRANT ALL PRIVILEGES ON wolfieshop_db.* TO 'root'@'localhost';#added this for me until i can figure out '' user
FLUSH PRIVILEGES;
DROP DATABASE wolfieshop_db;
DROP USER 'lal'@'localhost';
quit
