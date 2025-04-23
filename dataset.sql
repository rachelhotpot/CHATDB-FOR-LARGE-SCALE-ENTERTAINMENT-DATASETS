-- mysql --local-infile=1 -u root -p

CREATE TABLE `genome_scores` (
  `movieId` int DEFAULT NULL,
  `tagId` int DEFAULT NULL,
  `relevance` double DEFAULT NULL,
  PRIMARY KEY (`movieId`,`tagId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `genome_tags` (
  `tagId` int DEFAULT NULL,
  `tag` text,
  PRIMARY KEY (`tagId`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `link` (
  `movieId` int DEFAULT NULL,
  `imdbId` int DEFAULT NULL,
  `tmdbId` int DEFAULT NULL,
  PRIMARY KEY (`movieId`, `imdbId`, `tmdbId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `movie` (
  `movieId` int NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `genres` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`movieId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `rating` (
  `userId` int DEFAULT NULL,
  `movieId` int DEFAULT NULL,
  `rating` double DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`userId`, `movieId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `tag` (
  `userId` int DEFAULT NULL,
  `movieId` int DEFAULT NULL,
  `tag` varchar(255),
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SET GLOBAL local_infile = 1;
LOAD DATA LOCAL INFILE '/Users/kevinbui/Documents/DSCI 551 - Project/src/dataset1/genome_scores.csv' INTO TABLE genome_scores CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/Users/kevinbui/Documents/DSCI 551 - Project/src/dataset1/genome_tags.csv' INTO TABLE genome_tags CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/Users/kevinbui/Documents/DSCI 551 - Project/src/dataset1/link.csv' INTO TABLE link CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/Users/kevinbui/Documents/DSCI 551 - Project/src/dataset1/movie.csv' INTO TABLE movie CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/Users/kevinbui/Documents/DSCI 551 - Project/src/dataset1/rating.csv' INTO TABLE rating CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/Users/kevinbui/Documents/DSCI 551 - Project/src/dataset1/tag.csv' INTO TABLE tag CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;

ALTER TABLE `551project`.`genome_scores` 
ADD CONSTRAINT `fk_genomescores_movieid`
  FOREIGN KEY (`movieId`)
  REFERENCES `551project`.`movie` (`movieId`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `fk_genomescores_tagid`
  FOREIGN KEY (`tagId`)
  REFERENCES `551project`.`genome_tags` (`tagId`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
  
ALTER TABLE `551project`.`link` 
ADD INDEX `movieid_idx` (`movieId` ASC) VISIBLE;
ALTER TABLE `551project`.`link` 
ADD CONSTRAINT `fk_link_movieid`
  FOREIGN KEY (`movieId`)
  REFERENCES `551project`.`movie` (`movieId`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
  
ALTER TABLE `551project`.`rating` 
ADD INDEX `movieid_idx` (`movieId` ASC) VISIBLE;
ALTER TABLE `551project`.`rating` 
ADD CONSTRAINT `fk_rating_movieid`
  FOREIGN KEY (`movieId`)
  REFERENCES `551project`.`movie` (`movieId`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `551project`.`tag` 
ADD INDEX `movieid_idx` (`movieId` ASC) VISIBLE;
ALTER TABLE `551project`.`tag` 
ADD CONSTRAINT `fk_tag_movieid`
  FOREIGN KEY (`movieId`)
  REFERENCES `551project`.`movie` (`movieId`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;


  

