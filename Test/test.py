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

def test_invalid_logins(client):
    """Testing what happens when invalid logins are submitted"""


# This is for sign-up test


def test_signup_users(client):
    """Test if new users make it to the database"""

def test_duplicate_username(client):
    """Testing to see what happens when you have duplicate usernames"""


# This is for feed test


def test_if_feed_loads(client):
    """Test if the feed loads after loging in"""


# This test the post and comments


def test_insert_post(client):
    """This test verifies if the post properly inserts into the feed"""

def add_comment(client):
    """This test adding to comments to existing post"""


# This test everything with the ingredients


def add_ingredient(client):
    """Testing to see if the ingredients table exist and that the user can insert into it"""