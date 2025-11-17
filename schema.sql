DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    favorite_food TEXT NOT NULL
);

DROP TABLE IF EXISTS posts;
CREATE TABLE posts
(
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    appliances_id INTEGER NOT NULL,
    title   TEXT    NOT NULL,
    content TEXT    NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (appliances_id) REFERENCES appliances(id)
);

DROP TABLE IF EXISTS appliances;
CREATE TABLE appliances
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    post_id INTEGER,
    stove BOOLEAN,
    oven BOOLEAN,
    microwave BOOLEAN,
    blender BOOLEAN,
    toaster BOOLEAN,
    air_fryer BOOLEAN,
    slow_cooker BOOLEAN,
    pressure_cooker BOOLEAN,
    grill BOOLEAN
);