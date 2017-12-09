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
	TotalPrice DECIMAL(9,2),
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
	PricePerItem DECIMAL(9,2),   -- This is dependent on ItemId
	PRIMARY KEY(TransactionContentsId),
	CHECK(PricePerItem >= 0), 
	CHECK(Quantity > 0)
);

CREATE TABLE Payment (
	PaymentId INTEGER AUTO_INCREMENT,
	TransactionId	   INTEGER,
	Type		   CHAR(10), -- Credit or Debit
	BillingAddress	   VARCHAR(255),
	CardNumber	   CHAR(16),	-- We are not performing operations, therefore its CHAR not INTEGER
	CardExpiryDate CHAR(5),	-- In format "XX/XX"
	PRIMARY KEY(PaymentId)
);

CREATE TABLE Shipment (
	ShipmentId INTEGER AUTO_INCREMENT,
	TransactionId	INTEGER,
	Provider	CHAR(20),
	Type		CHAR(50), -- Types: Standard, Priority, 2-Day, etc
	Address	CHAR(50) NOT NULL,
	Fee		DECIMAL(9,2), -- Used in calculating total price in a transaction
	PRIMARY KEY(ShipmentId)
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
		UPDATE Item
		SET Item.Quantity = Item.Quantity - NEW.Quantity
		WHERE Item.ItemId = NEW.ItemId;
	END;
	$$
DELIMITER ; 

CREATE USER 'lal'@'localhost' IDENTIFIED BY 'ALLCSE305<3';
GRANT ALL PRIVILEGES ON wolfieshop_db.* TO 'lal'@'localhost';
FLUSH PRIVILEGES;

quit

