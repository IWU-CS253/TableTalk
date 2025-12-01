DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appliances_id INTEGER,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    favorite_food TEXT NOT NULL,
    cart TEXT,
    following TEXT,
    FOREIGN KEY (appliances_id) REFERENCES appliances(id)
);

DROP TABLE IF EXISTS posts;
CREATE TABLE posts
(
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    appliance_id INTEGER NOT NULL,
    title   TEXT    NOT NULL,
    content TEXT    NOT NULL,
    category TEXT NOT NULL,
    username TEXT NOT NULL,
    ingredients,
    steps,
    appliances,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (appliance_id) REFERENCES appliances(id)
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

Create Table comments
(   
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    comment_text TEXT NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES posts(id)
);