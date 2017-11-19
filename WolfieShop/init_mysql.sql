CREATE DATABASE wolfieshop_db;

CREATE TABLE wolfieshop_db.shop_item (
	ItemId INTEGER AUTO_INCREMENT,
	ItemName VARCHAR(100),
	Quantity INTEGER,
	Price INTEGER,
	Category CHAR(25), -- ex Household Appliances, Stationery, Books
	Rating INTEGER,
	NumReviews INTEGER DEFAULT 0,
	PRIMARY KEY(ItemId),
	CHECK (Quantity >= 0),
	CHECK (Price >= 0),
	CHECK (NumReviews >= 0)
);


CREATE USER 'lal'@'localhost' IDENTIFIED BY 'ALLCSE305<3';
GRANT ALL PRIVILEGES ON wolfieshop_db.* TO 'lal'@'localhost';
FLUSH PRIVILEGES;

quit
