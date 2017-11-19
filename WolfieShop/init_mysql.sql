CREATE DATABASE wolfieshop_db;

CREATE TABLE wolfieshop_db.Item (
	ItemId INTEGER AUTO_INCREMENT,
	ItemName VARCHAR(100),
	Quantity INTEGER,
	Price DECIMAL(9,2),
	Category CHAR(25), -- ex Household Appliances, Stationery, Books
	Rating DECIMAL(3,2),
	NumReviews INTEGER,
	PRIMARY KEY(ItemId),
	CHECK (Quantity >= 0),
	CHECK (Price >= 0),
	CHECK (NumReviews >= 0),
	CHECK (Rating >= 0 AND Rating <= 5)
);


CREATE USER 'lal'@'localhost' IDENTIFIED BY 'ALLCSE305<3';
GRANT ALL PRIVILEGES ON wolfieshop_db.* TO 'lal'@'localhost';
FLUSH PRIVILEGES;

quit
