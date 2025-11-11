import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, flash

app = Flask(__name__)

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


def check_username_exists(username):
    db = get_db()
    cursor = db.execute('SELECT id FROM accounts WHERE username = ?', (username,))
    user = cursor.fetchone()
    return user is not None

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

@app.route('/login', methods=['post'])
def login():
    if "username" in request.args and "password" in request.args:
        db = get_db()
        cur = db.execute('SELECT id FROM accounts WHERE username = ? AND password = ?',
                         [request.form['username'], request.form['password']])
        user = cur.fetchone()
        if user is not None:
            flash('Successfully logged into account')
            return redirect(url_for('show_feed'))
        else:
            flash('Username does not exist')
            return render_template('login.html')
    else:
        flash('Invalid username or password')
        return render_template('login.html')

@app.route('/sign_up', methods=['post'])
def sign_up():
    if "username" in request.args and "password" in request.args:
        db = get_db()
        cur = db.execute('SELECT id FROM accounts WHERE username = ?',
                            [request.form['username']])
        user = cur.fetchone()
        if user is None:
            db.execute('INSERT INTO accounts (username, password) VALUES (?, ?)',
                       [request.form['username'], request.form['password']])
            db.commit()
            flash('New account successfully registered')
            return redirect(url_for('show_feed'))
        else:
            flash('Username is already taken')
            return render_template('new_user_sign_up.html')
    else:
        return render_template('new_user_sign_up.html')

@app.route('/show_feed', methods=['post'])
def show_feed():
    db = get_db()
    if "username" in request.args and "password" in request.args:
        cur = db.execute('SELECT id, title FROM posts ORDER BY id DESC')
        feed = cur.fetchall()
        return render_template('main_feed', feed=feed)
    else:
        flash('Invalid username or password')
        return render_template('login.html')

@app.route('/cart', methods=['post'])
def show_cart():
    return render_template('cart.html')

@app.route('/user_profile', methods=['post'])
def show_profile():
    if "username" in request.args:
        db = get_db()
        cur = db.execute('SELECT id FROM accounts WHERE username = ?',
                         [request.form['username']])
        user = cur.fetchone()
        if user is not None:
            return render_template('user_profile.html', user=user)
        else:
            flash('User does not exist')
            return redirect(url_for('show_feed'))
    else:
        flash('Their username is needed load their profile')
        return redirect(url_for('show_feed'))
