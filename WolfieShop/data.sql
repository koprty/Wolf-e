use wolfieshop_db;

LOCK TABLES `Customer` WRITE;
/*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
INSERT INTO `Customer` VALUES (1,'Wolfie','Seawolf','wolfie@stonybrook.edu',1234567890,"wolfie");
/*!40000 ALTER TABLE `Customer` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `Customer` WRITE;
/*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
INSERT INTO `Customer` VALUES (2,'Selina','Wolf','s@stonybrook.edu',1234567890,"123");
/*!40000 ALTER TABLE `Customer` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `Customer` WRITE;
/*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
INSERT INTO `Customer` VALUES (3,'Ichigo','Kurosaki','bleach@stonybrook.edu',1234567890,"123");
/*!40000 ALTER TABLE `Customer` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `Customer` WRITE;
/*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
INSERT INTO `Customer` VALUES (4,'Matt','Wolfie Stuart','h@stonybrook.edu',1234567890,"123");
/*!40000 ALTER TABLE `Customer` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `Item` WRITE;
/*!40000 ALTER TABLE `Item` DISABLE KEYS */;
INSERT INTO `Item` VALUES (1,'Google Pixel',10,758.95,'ELECTRONICS',0.00,0),(2,'iPhone X',15,756.56,'ELECTRONICS',0.00,0),(3,'Logitech Mouse',2,14.95,'ELECTRONICS',0.00,0),(4,'Naruto Vol. 1',4,14.95,'BOOKS',0.00,0),(5,'Bleach Vol. 5',45,13.96,'BOOKS',0.00,0),(6,'Looseleaf Paper x150',50,9.96,'STATIONERY',0.00,0);
/*!40000 ALTER TABLE `Item` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `Review` WRITE;
/* Item Id before customer id */
INSERT INTO `Review` VALUES (1,4, 2, 5, 'Naruto is one of the best mangas written in this universe. If you ever need to take a break from studying from finals, this is absolutely the best book for you.');
UNLOCK TABLES;

LOCK TABLES `Review` WRITE;
/* Item Id before customer id */
INSERT INTO `Review` VALUES (2,6, 3, 3, 'This is an amazing product, but is way overpriced.');
UNLOCK TABLES;


LOCK TABLES `Review` WRITE;
/* Item Id before customer id */
INSERT INTO `Review` VALUES (3,5, 3, 5, 'The BEST MANGA of all time.');
UNLOCK TABLES;

LOCK TABLES `Review` WRITE;
/* Item Id before customer id */
INSERT INTO `Review` VALUES (4,6, 4, 5, 'Very useful thing to have around finals time.');
UNLOCK TABLES;
