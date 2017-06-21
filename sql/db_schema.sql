DROP TABLE IF EXISTS "planet-votes";
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(30) UNIQUE,
    password CHAR(93)
);

CREATE TABLE "planet-votes" (
    id SERIAL PRIMARY KEY,
    planet_id INTEGER,
    user_id INTEGER NOT NULL REFERENCES users(id),
    submission_time TIMESTAMP WITHOUT TIME ZONE
);
