DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    favorite_food TEXT NOT NULL,
    cart TEXT,
    following TEXT,
);

DROP TABLE IF EXISTS posts;
CREATE TABLE posts
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    category TEXT,
    steps TEXT,
    ingredients TEXT,
    appliances TEXT,
    username TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

DROP TABLE IF EXISTS appliances;
CREATE TABLE appliances
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
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

Create Table comments
(   
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    comment_text TEXT NOT NULL,
    username TEXT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id)
);
