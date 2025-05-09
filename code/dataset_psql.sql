-- psql database setup

CREATE TABLE genome_scores (
  movieId INTEGER,
  tagId INTEGER,
  relevance DOUBLE PRECISION,
  PRIMARY KEY (movieId, tagId)
);

CREATE TABLE genome_tags (
  tagId INTEGER,
  tag TEXT,
  PRIMARY KEY (tagId)
);

CREATE TABLE link (
  movieId INTEGER,
  imdbId INTEGER,
  tmdbId INTEGER,
  PRIMARY KEY (movieId, imdbId)
);

CREATE TABLE movie (
  movieId INTEGER NOT NULL,
  title VARCHAR(255),
  genres VARCHAR(255),
  PRIMARY KEY (movieId)
);

CREATE TABLE rating (
  userId INTEGER,
  movieId INTEGER,
  rating DOUBLE PRECISION,
  timestamp TIMESTAMP,
  PRIMARY KEY (userId, movieId)
);

CREATE TABLE tag (
  userId INTEGER,
  movieId INTEGER,
  tag VARCHAR(255),
  timestamp TIMESTAMP
);

\copy genome_scores FROM '/Users/kevinbui/Documents/DSCI 551 - Project/src/dataset1/genome_scores.csv' DELIMITER ',' CSV HEADER;
\copy genome_tags FROM '/Users/kevinbui/Documents/DSCI 551 - Project/src/dataset1/genome_tags.csv' DELIMITER ',' CSV HEADER;
\copy link FROM '/Users/kevinbui/Documents/DSCI 551 - Project/src/dataset1/link.csv' DELIMITER ',' CSV HEADER;
\copy movie FROM '/Users/kevinbui/Documents/DSCI 551 - Project/src/dataset1/movie.csv' DELIMITER ',' CSV HEADER;
\copy rating FROM '/Users/kevinbui/Documents/DSCI 551 - Project/src/dataset1/rating.csv' DELIMITER ',' CSV HEADER;
\copy tag FROM '/Users/kevinbui/Documents/DSCI 551 - Project/src/dataset1/tag.csv' DELIMITER ',' CSV HEADER;

