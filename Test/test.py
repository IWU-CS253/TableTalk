import os
import tempfile
import pytest
from app import app, init_db, get_db

#Creating a temporary database to use for testing purposes
@pytest.fixture
def client():
    #First I'll create a temporary database
    temp = tempfile.mkstemp()
    db_fd = temp[0]
    temp_db_path = temp[1]
    app.config['DATABASE'] = temp_db_path
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client


#This Area is for route testing

def test_welcome_page(client):
    """Testing to make sure the page loads"""
    response = client.get('/')
    assert b"login" in response.data.lower()
    assert b"username" in response.data.lower()

def test_invalid_logins(client):
    """Testing what happens when invalid logins are submitted"""
    response = client.get("/")
    assert b"login" in response.data.lower()
    assert b"username" in response.data.lower()

# This is for sign-up test


def test_signup_users(client):
    """Test if new users make it to the database"""
    client.post("/sign_up", data={"username" : "testuser", "password" : "testpass"})

    #this should confirm the database change
    with app.app_context():
        db = get_db()
        user = db.execute("SELECT * FROM accounts WHERE username = ?", ("testuser",)).fetchone()
        assert user is not None

def test_duplicate_username(client):
    """Testing to see what happens when you have duplicate usernames"""
    client.post('/sign_up', data={"username":"repeat", "password":"a"})
    response = client.post('/sign_up', data={"username":"repeat", "password":"a"})

    assert b"already taken" in response.data.lower()

# This is for feed test


def test_if_feed_loads(client):
    """Test if the feed loads after loging in"""
    #creates account
    client.post('/sing_up', data={"username":"me", "password":"123"})

    response = client.post('/show_feed', data={"username":"me", "password":"123"})

    #should load feed text
    assert b"post" in response.data.lower() or b"feed" in response.data.lower()

# This test the post and comments


def test_insert_post(client):
    """This test verifies if the post properly inserts into the feed"""
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO posts (title,userid) VALUES (?,?)", ("Test Post", 1))
        db.commit()

        response = client.get("/show_feed")

        #Feed should have/contain certain post
        assert b"post" in response.data.lower()

def add_comment(client):
    """This test adding to comments to existing post"""

    #create post first
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO posts (title, userid) VALUES (?,?)", ("Another Post",1))
        db.commit()

        #adding a comment
        client.post('/add_comment/1', data= {"comment":"Nice recipe!"})

        with app.app_context():
            db = get_db()
            comment = db.execute("SELECT * FROM comments WHERE post_id = ?", (1,)).fetchone()

            assert comment is not None
            assert comment["comment_text"] == "Nice recipe!"

# This test everything with the ingredients


def add_ingredient(client):
    """Testing to see if the ingredients table exist and that the user can insert into it"""
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO ingredients (post_id, ingredient, measurement) VALUES (?,?,?)", (1,"Sugar", "1 cup"))
        db.commit()

        row = db.execute("SELECT * FROM ingredients WHERE post_id = ?", (1)).fetchone()

        assert row is not None
        assert row["ingredient"].lower() == "sugar"



