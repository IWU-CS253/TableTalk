import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, flash, get_flashed_messages, session

app = Flask(__name__)

# look to see if you can store multiple attributes in the session data or just the username
# need to figure out how to use this
app.secret_key = 'your_secret_key'  # Required for session and flash

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'tabletalk.db'),
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def print_flashes():
    for message in get_flashed_messages():
        print(message)

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def welcome_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if "username" in request.form and "password" in request.form:
        db = get_db()
        cur = db.execute('SELECT id FROM users WHERE username = ? AND password = ?',
                         [request.form['username'], request.form['password']])
        user = cur.fetchone()
        if user is not None:
            # update session
            session['username'] = request.form['username']

            flash("Successfully logged into account", "info")
            print_flashes()
            return redirect(url_for('show_feed'))
        else:
            flash("Username does not exist", "error")
            print_flashes()
            # this needs to return a flash to users so they know as well not just a flash to the terminal
            return render_template('login.html')
    else:
        flash("Invalid username or password", "error")
        print_flashes()
        return render_template('login.html')


@app.route('/sign_up')
def sign_up():
    return render_template('new_user_sign_up.html')


@app.route('/register_user', methods=['POST'])
def register_user():
    if all(request.form.get(field) for field in ["username", "password", "first_name", "last_name", "favorite_food"]):
        db = get_db()

        # make easy access stored variable
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        favorite_food = request.form.get('favorite_food')

        cur = db.execute('SELECT id FROM users WHERE username = ?', [username])
        user = cur.fetchone()

        if user is None:
            db.execute('INSERT INTO users (username, password, first_name, last_name, favorite_food) VALUES (?, ?, ?, ?, ?)',
                       [username, password, first_name, last_name, favorite_food])
            db.commit()
            session['username'] = username  # Store user in session
            flash("New account successfully registered", "info")
            return redirect(url_for('show_feed'))
        else:
            flash("Username is already taken", "warning")
            return render_template('new_user_sign_up.html')
    else:
        flash("Form arguments missing", "error")
        return render_template('new_user_sign_up.html')

@app.route('/show_feed', methods=['GET', 'POST'])
def show_feed():
    if 'username' in session:
        db = get_db()
        cur = db.execute('SELECT id, title FROM posts ORDER BY id DESC')
        feed = cur.fetchall()
        return render_template('main_feed.html', feed=feed)
    else:
        flash("Please log in to view the feed", "error")
        return render_template('login.html')

@app.route('/cart')
def show_cart():
    return render_template('cart.html')

@app.route('/user_profile', methods=['POST'])
def show_profile():
    if "username" in session:
        db = get_db()
        cur = db.execute('SELECT id FROM users WHERE username = ?',
                         [session['username']])
        user = cur.fetchone()
        if user is not None:
            return render_template('user_profile.html', user=user)
        else:
            flash("User does not exist", "error")
            print_flashes()
            return redirect(url_for('show_feed'))
    else:
        flash("Their username is needed load their profile", "error")
        print_flashes()
        return redirect(url_for('show_feed'))

@app.route('/recipe', methods=['POST'])
def show_recipe_card():
    return render_template('recipe_card.html')


@app.route('/submit_recipe', methods=['POST'])
def submit_recipe():
    if 'username' in session:
        title = request.form['title']
        category = request.form['category']
        content = request.form['content']
        username = session['username']

        db = get_db()
        cur = db.execute('SELECT id FROM users WHERE username = ?', [username])
        user = cur.fetchone()

        if user:
            user_id = user['id']
            db.execute('INSERT INTO posts (title, category, content, author, user_id) VALUES (?, ?, ?, ?, ?)',
                       [title, category, content, username, user_id])
            db.commit()

            flash("Recipe added successfully!", "info")
            return redirect(url_for('show_feed'))
        else:
            flash("User not found", "error")
            return redirect(url_for('login'))
    else:
        flash("Please log in to submit a recipe", "error")
        return redirect(url_for('login'))

@app.route('/add_appliance', methods=['POST'])
def add_appliance():
    if 'username' in session:
        if 'appliance' in request.form:
            db = get_db()
            cur = db.execute('SELECT id FROM users WHERE username = ?', [session['username']])
            id_num = cur.fetchone()
            db.execute('UPDATE appliances SET ? = TRUE WHERE user_id = ?', [request.form['appliance'], id_num])
            return redirect(url_for('user_profile'))
        else:
            flash("An appliance name is needed to add it to your profile")
            print_flashes()
            return redirect(url_for('user_profile'))
    else:
        flash("You need to be logged in to add an appliance to your profile")
        print_flashes()
        return redirect(url_for('user_profile'))
