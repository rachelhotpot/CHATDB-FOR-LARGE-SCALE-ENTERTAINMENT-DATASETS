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

\copy genome_scores FROM '/dataset/genome_scores.csv' DELIMITER ',' CSV HEADER;
\copy genome_tags FROM '/dataset/genome_tags.csv' DELIMITER ',' CSV HEADER;
\copy link FROM '/dataset/link.csv' DELIMITER ',' CSV HEADER;
\copy movie FROM '/dataset/movie.csv' DELIMITER ',' CSV HEADER;
\copy rating FROM '/dataset/rating.csv' DELIMITER ',' CSV HEADER;
\copy tag FROM '/dataset/tag.csv' DELIMITER ',' CSV HEADER;

