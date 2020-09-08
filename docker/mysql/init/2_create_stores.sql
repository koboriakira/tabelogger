CREATE TABLE tabelogger.stores (
  `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `name` varchar(1000),
  `navigation` varchar(1000),
  `rate` decimal(3,2),
  `address` varchar(1000),
  `address_image_url` varchar(2083),
  `url` varchar(767) UNIQUE
);
commit;
