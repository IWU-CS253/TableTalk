DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS posts;
CREATE TABLE posts
(
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title   TEXT    NOT NULL,
    content TEXT    NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);