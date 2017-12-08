CREATE DATABASE wolfieshop_db;
use wolfieshop_db;

CREATE TABLE Item (
	ItemId INTEGER AUTO_INCREMENT,
	ItemName VARCHAR(100),
	Quantity INTEGER,
	Price DECIMAL(9,2),
	Category CHAR(25),
	Rating DECIMAL(3,2),
	NumReviews INTEGER DEFAULT 0,
	PRIMARY KEY(ItemId),
	CHECK (Quantity >= 0),
	CHECK (Price >= 0),
	CHECK (NumReviews >= 0),
	CHECK (Rating >= 0 AND Rating <= 5)
);

CREATE TABLE Customer (
	CustomerId INTEGER AUTO_INCREMENT,
	FirstName CHAR(20) NOT NULL,
	LastName CHAR(20) NOT NULL,
	Email CHAR(30) NOT NULL,
	PhoneNumber CHAR(15),
	PasswordHash CHAR(100) DEFAULT NULL,
	PRIMARY KEY(CustomerId)
);


CREATE TABLE Review (
	ReviewId INTEGER AUTO_INCREMENT,
	ItemId INTEGER,
	CustomerId INTEGER,
	Rating INTEGER NOT NULL,
	ReviewText VARCHAR(255),
	CHECK (Rating >= 0 AND Rating <= 5),
	UNIQUE (ItemId, CustomerId), -- A customer can review an item only once
	PRIMARY KEY (ReviewId),
	FOREIGN KEY(ItemId) REFERENCES Item(ItemId),
	FOREIGN KEY(CustomerId) REFERENCES Customer(CustomerId)
);

CREATE TABLE ShoppingCart (
	ShoppingCartId INTEGER AUTO_INCREMENT, -- added for primary key
	CustomerId INTEGER,
	ItemId INTEGER, -- set val
	Quantity INTEGER, -- set val
	PRIMARY KEY(ShoppingCartId), 
	FOREIGN KEY(CustomerId) REFERENCES Customer(CustomerId),
	FOREIGN KEY(ItemId) REFERENCES Item(ItemId),
	CHECK(Quantity > 0)
);

CREATE TABLE TransactionOrder ( -- can't be named transaction
	TransactionId INTEGER AUTO_INCREMENT,
	CustomerId INTEGER,
	TotalPrice INTEGER,
	DateProcessed DATETIME,
	PRIMARY KEY(TransactionId),
	CHECK (TotalPrice >= 0)  -- we may give free stuff 
    -- this is processed already, so the tables should never change
);

CREATE TABLE TransactionContents (
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


DELIMITER $$ 
CREATE TRIGGER update_item_review AFTER INSERT ON Review 
	FOR EACH ROW  
	BEGIN 
		UPDATE Item,Review 
		SET Item.Rating = ( 
				SELECT AVG(r.Rating) 
				FROM Review r 
				WHERE Item.ItemId = r.ItemId 
			), 
			NumReviews = NumReviews + 1 
		WHERE Item.ItemId = Review.ItemId; 
	END; 
	$$ 

CREATE TRIGGER decrement_quantity_transaction AFTER INSERT ON TransactionContents
	FOR EACH ROW
	BEGIN
		UPDATE Item, TransactionContents
		SET Item.Quantity = Item.Quantity - TransactionContents.Quantity
		WHERE Item.ItemId = TransactionContents.ItemId;
	END;
	$$
DELIMITER ; 

CREATE USER 'lal'@'localhost' IDENTIFIED BY 'ALLCSE305<3';
GRANT ALL PRIVILEGES ON wolfieshop_db.* TO 'lal'@'localhost';
FLUSH PRIVILEGES;

quit

