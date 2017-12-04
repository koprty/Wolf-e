CREATE DATABASE wolfieshop_db;

CREATE TABLE wolfieshop_db.Item (
	ItemId INTEGER AUTO_INCREMENT,
	ItemName VARCHAR(100),
	Quantity INTEGER,
	Price DECIMAL(9,2),
	Category CHAR(25),
	Rating DECIMAL(3,2),
	NumReviews INTEGER,
	PRIMARY KEY(ItemId),
	CHECK (Quantity >= 0),
	CHECK (Price >= 0),
	CHECK (NumReviews >= 0),
	CHECK (Rating >= 0 AND Rating <= 5)
);

CREATE TABLE wolfieshop_db.Customer (
	CustomerId INTEGER AUTO_INCREMENT,
	FirstName CHAR(20) NOT NULL,
	LastName CHAR(20) NOT NULL,
	Email CHAR(30) NOT NULL,
	PhoneNumber CHAR(15),
	PRIMARY KEY(CustomerId)
);


CREATE TABLE wolfieshop_db.Review (
	ReviewId INTEGER AUTO_INCREMENT,
	ItemId INTEGER,
	CustomerId INTEGER,
	Rating INTEGER NOT NULL,
	ReviewText VARCHAR(255),
	CHECK (Rating >= 0 AND Rating <= 5),
	PRIMARY KEY (ReviewId),
	FOREIGN KEY(ItemId) REFERENCES Item(ItemId),
	FOREIGN KEY(CustomerId) REFERENCES Customer(CustomerId)
);


CREATE TABLE wolfieshop_db.ShoppingCart (
	ShoppingCartId INTEGER, -- added for primary key
	CustomerId INTEGER,
	ItemId INTEGER, -- set val
	Quantity INTEGER, -- set val
	PRIMARY KEY(ShoppingCartId), 
	FOREIGN KEY(CustomerId) REFERENCES Customer(CustomerId),
	FOREIGN KEY(ItemId) REFERENCES Item(ItemId),
	CHECK(Quantity > 0)
);


CREATE USER 'lal'@'localhost' IDENTIFIED BY 'ALLCSE305<3';
GRANT ALL PRIVILEGES ON wolfieshop_db.* TO 'lal'@'localhost';
FLUSH PRIVILEGES;

quit

