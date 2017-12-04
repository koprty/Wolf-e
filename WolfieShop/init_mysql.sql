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
	PasswordHash CHAR(100) DEFAULT NULL,
	PRIMARY KEY(CustomerId)
);

USE wolfieshop_db;

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

USE wolfieshop_db;

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

USE wolfieshop_db;

CREATE TABLE wolfieshop_db.TransactionOrder ( -- can't be named transaction
	TransactionId INTEGER AUTO_INCREMENT,
	CustomerId INTEGER,
	TotalPrice INTEGER,
	DateProcessed DATETIME,
	PRIMARY KEY(TransactionId),
	CHECK (TotalPrice >= 0)  -- we may give free stuff 
    -- this is processed already, so the tables should never change
);

USE wolfieshop_db;

CREATE TABLE wolfieshop_db.TransactionContents (
	TransactionContentsId INTEGER AUTO_INCREMENT, -- added for primary key. Only TransactionId will really be needed for lookup though
	TransactionId INTEGER,
	CustomerId	INTEGER,
	ItemId INTEGER,   -- Set value - points to to an item in the item table
	Quantity INTEGER,   -- This is dependent on ItemId
	PricePerItem INTEGER,   -- This is dependent on ItemId
	PRIMARY KEY(TransactionContentsId),
	CHECK(PricePerItem >= 0), 
	CHECK(Quantity > 0)
);




CREATE USER 'lal'@'localhost' IDENTIFIED BY 'ALLCSE305<3';
GRANT ALL PRIVILEGES ON wolfieshop_db.* TO 'lal'@'localhost';
FLUSH PRIVILEGES;

quit

