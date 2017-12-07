use wolfieshop_db;

LOCK TABLES `Customer` WRITE;
/*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
INSERT INTO `Customer` VALUES (1,'Lisa','Guo','lisa.guo@stonybrook.edu',NULL,NULL);
/*!40000 ALTER TABLE `Customer` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `Item` WRITE;
/*!40000 ALTER TABLE `Item` DISABLE KEYS */;
INSERT INTO `Item` VALUES (1,'Google Pixel',10,758.95,'ELECTRONICS',0.00,0),(2,'iPhone X',15,756.56,'ELECTRONICS',0.00,0),(3,'Logitech Mouse',2,14.95,'ELECTRONICS',0.00,0),(4,'Naruto Vol. 1',4,14.95,'BOOKS',0.00,0),(5,'Bleach Vol. 5',45,13.96,'BOOKS',0.00,0),(6,'Looseleaf Paper x150',50,9.96,'STATIONERY',0.00,0);
/*!40000 ALTER TABLE `Item` ENABLE KEYS */;
UNLOCK TABLES;