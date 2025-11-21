import os
import json
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, flash, get_flashed_messages, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# look to see if you can store multiple attributes in the session data or just the username
# need to figure out how to use this
app.secret_key = 'table_talk_secret_key'

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

@app.route('/sign_up')
def sign_up():
    return render_template('new_user_sign_up.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    if all(request.form.get(field) for field in ["username", "password", "first_name", "last_name", "favorite_food"]):
        db = get_db()

        # make easy access stored variable
        username = request.form.get('username')
        raw_password = request.form.get('password')
        hashed_password = generate_password_hash(raw_password)
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        favorite_food = request.form.get('favorite_food')

        cur = db.execute('SELECT id FROM users WHERE username = ?', [username])
        user = cur.fetchone()

        if user is None:
            # json.dumps() citation https://www.geeksforgeeks.org/python/json-loads-in-python/
            db.execute('INSERT INTO users (username, password, first_name, last_name, favorite_food, cart) VALUES (?, ?, ?, ?, ?, ?)',
                [username, hashed_password, first_name, last_name, favorite_food, json.dumps([])])
            db.commit()

            # store the username in a session variable
            session['username'] = username
            session['cart'] = []
            flash("New account successfully registered", "info")
            return redirect(url_for('show_feed'))
        else:
            flash("Username is already taken", "warning")
            return render_template('new_user_sign_up.html')
    else:
        flash("Form arguments missing", "error")
        return render_template('new_user_sign_up.html')

@app.route('/login', methods=['POST'])
def login():
    db = get_db()
    username = request.form['username']
    password_input = request.form['password']

    if "username" in request.form and "password" in request.form:
        # a more secure update to viewing hashed passwords
        user = db.execute('SELECT id, password FROM users WHERE username = ?',
                         [username]).fetchone()

        # check to see if the user has entered the correct information (hashed password)
        if user and check_password_hash(user['password'], password_input):
            session['username'] = username

            # set session cart to the values in the cart from when the user last logged out
            stored_row = db.execute('SELECT cart FROM users WHERE username = ?',
                                         [username]).fetchone()

            # assign the cart variable if it exists otherwise initialize with an empty cart
            # json.loads() citation https://www.geeksforgeeks.org/python/json-loads-in-python/
            session['cart'] = json.loads(stored_row['cart']) if stored_row and stored_row['cart'] else []

            # log them into their account
            flash("Successfully logged into account", "info")
            return redirect(url_for('show_feed'))

        # if username/password are not in the input (this should never happen bc fields are required but safe check)
        else:
            flash("Invalid username or password", "error")
            return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    username = session['username']
    db = get_db()

    # store the current cart in the users table to be fetched later when the user logs back in
    adding_cart = session['cart']
    # json.dumps() citation https://www.geeksforgeeks.org/python/json-loads-in-python/
    db.execute('UPDATE users SET cart=? WHERE username=?', [json.dumps(adding_cart), username])
    db.commit()

    # remove the current cart session variable so it does not carry over into the next logged-in user
    session['cart'] = []
    session['username'] = None
    return render_template('login.html')

@app.route('/show_feed', methods=['GET', 'POST'])
def show_feed():
    # make sure user is logged in
    if 'username' in session:
        db = get_db()
        username = session['username']

        # find user id using the session username
        user_row = db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        if not user_row:
            flash("User not found in database", "error")
            return redirect(url_for('login'))

        user_id = user_row['id']

        # get all posts for the feed
        feed = db.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()

        # get all users except the one logged into the current session
        friends = db.execute('SELECT first_name, last_name, username, favorite_food FROM users WHERE id != ? ORDER BY id DESC', (user_id,)).fetchall()

        return render_template('main_feed.html', posts=feed, suggested_friends=friends)

    # return user to login if session is empty
    else:
        flash("Please log in to view the feed", "error")
        return render_template('login.html')


@app.route('/filter_posts')
def filter_posts():
    if 'username' in session:
        db = get_db()
        username = session['username']

        selected_category = request.args.get('filter_category')
        db = get_db()
        categories = db.execute('SELECT DISTINCT category FROM posts').fetchall()

        # gets all the info to pass in the freinds for the aside
        user_row = db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        user_id = user_row['id']
        friends = db.execute('SELECT first_name, last_name, username, favorite_food FROM users WHERE id != ? ORDER BY id DESC', (user_id,)).fetchall()

        # if the user wants to filer posts
        if selected_category and selected_category != "FILTER POSTS":
            posts = db.execute('SELECT * FROM posts WHERE category=?',
                               (selected_category,)).fetchall()
        # default will be all posts
        else:
            posts = db.execute('SELECT * FROM posts').fetchall()

        # return the filtered main feed
        return render_template('main_feed.html', posts=posts, categories=categories,
                               selected_category=selected_category, suggested_friends=friends)

    # incase user is not logged in
    else:
        flash("Please log in to view the feed", "error")
        return render_template('login.html')


@app.route('/user_profile', methods=['POST'])
def show_profile():
    if "username" in request.form:
        db = get_db()
        cur = db.execute('SELECT id FROM users WHERE username = ?',
                         [request.form['username']])
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

@app.route('/my_profile')
def my_profile():
    if "username" in session:
        db = get_db()
        cur = db.execute('SELECT * FROM users WHERE username = ?',
                         [session['username']])
        user = cur.fetchone()
        if user is not None:
            appliances = db.execute('SELECT * FROM appliances WHERE user_id = ?', [user['id']]).fetchone()
            recipes = db.execute('SELECT * FROM posts WHERE user_id = ? ORDER BY id DESC', [user['id']]).fetchall()
            return render_template('user_profile.html', user=user,appliances=appliances,recipes=recipes)
        else:
            flash("User does not exist", "error")
            print_flashes()
            return redirect(url_for('show_feed'))
    else:
        flash("Your username is needed load your profile", "error")
        print_flashes()
        return redirect(url_for('show_feed'))


@app.route('/add_appliance', methods=['POST'])
def add_appliance():
    if 'username' not in session:
        flash("Login required")
        return redirect(url_for('show_feed'))
    
    db = get_db()
    cur = db.execute('SELECT id FROM users WHERE username = ?', [session['username']])
    user_id = cur.fetchone()['id']
    
    # Check if row exists
    appliance = db.execute('SELECT * FROM appliances WHERE user_id = ?', [user_id]).fetchone()
    

    stove = 0
    if request.form.get('stove'):
        stove = 1

    oven = 0
    if request.form.get('oven'):
        oven = 1

    microwave = 0
    if request.form.get('microwave'):
        microwave = 1

    blender = 0
    if request.form.get('blender'):
        blender = 1

    toaster = 0
    if request.form.get('toaster'):
        toaster = 1

    air_fryer = 0
    if request.form.get('air_fryer'):
        air_fryer = 1

    slow_cooker = 0
    if request.form.get('slow_cooker'):
        slow_cooker = 1

    pressure_cooker = 0
    if request.form.get('pressure_cooker'):
        pressure_cooker = 1

    grill = 0
    if request.form.get('grill'):
        grill = 1
    
    if appliance:
        db.execute('''UPDATE appliances SET stove=?, oven=?, microwave=?, blender=?, 
                      toaster=?, air_fryer=?, slow_cooker=?, pressure_cooker=?, grill=? 
                      WHERE user_id=?''',
                   [stove, oven, microwave, blender, toaster, air_fryer, slow_cooker, pressure_cooker, grill, user_id])
    else:
        db.execute('''INSERT INTO appliances (user_id, stove, oven, microwave, blender, 
                      toaster, air_fryer, slow_cooker, pressure_cooker, grill) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   [user_id, stove, oven, microwave, blender, toaster, air_fryer, slow_cooker, pressure_cooker, grill])
    
    db.commit()
    flash("Appliances updated!")
    return redirect(url_for('my_profile'))

@app.route('/tag_appliance', methods=['POST'])
def tag_appliance():
    if all(request.form.get(field) for field in ["id", 'appliance']):
        db = get_db()
        cur = db.execute('SELECT appliances_id FROM posts WHERE id = ?', [session['id']])
        id_num = cur.fetchone()
        db.execute('UPDATE appliances SET ? = TRUE WHERE post_id = ?', [request.form['appliance'], id_num])
        return redirect(url_for('edit_post'))
    else:
        flash("An appliance name is needed to tag it on your post")
        print_flashes()
        return redirect(url_for('edit_post'))
    

@app.route('/filter_by_appliances')
def filter_by_appliances():
    if 'username' not in session:
        return redirect(url_for('welcome_page'))
    
    db = get_db()
    user_row = db.execute('SELECT id FROM users WHERE username = ?', [session['username']]).fetchone()
    user_id = user_row['id']
    
    user_app = db.execute('SELECT * FROM appliances WHERE user_id = ?', [user_id]).fetchone()
    
    if not user_app:
        flash("Add your appliances first!")
        return redirect(url_for('my_profile'))
    
    all_posts = db.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
    filtered = []
    
    for post in all_posts:
        post_app = db.execute('SELECT * FROM appliances WHERE post_id = ?', [post['id']]).fetchone()
        
        if not post_app:
            filtered.append(post)
            continue
        
        can_make = True
        if post_app['stove'] and not user_app['stove']:
            can_make = False
        if post_app['oven'] and not user_app['oven']:
            can_make = False
        if post_app['microwave'] and not user_app['microwave']:
            can_make = False
        if post_app['blender'] and not user_app['blender']:
            can_make = False
        if post_app['toaster'] and not user_app['toaster']:
            can_make = False
        if post_app['air_fryer'] and not user_app['air_fryer']:
            can_make = False
        if post_app['slow_cooker'] and not user_app['slow_cooker']:
            can_make = False
        if post_app['pressure_cooker'] and not user_app['pressure_cooker']:
            can_make = False
        if post_app['grill'] and not user_app['grill']:
            can_make = False
        
        if can_make:
            filtered.append(post)
    
    friends = db.execute('SELECT first_name, last_name, username, favorite_food FROM users WHERE id != ?', [user_id]).fetchall()
    return render_template('main_feed.html', posts=filtered, suggested_friends=friends, filtered_by_appliances=True)


@app.route('/submit_recipe', methods=['POST'])
def submit_recipe():
    if 'username' in session:
        title = request.form['title']
        category = request.form['recipe_category']
        ingredients = request.form['ingredients']
        steps = request.form['steps']
        username = session['username']
        appliances = request.form.get('appliances', "No Appliances Listed")


        db = get_db()
        cur = db.execute('SELECT id FROM users WHERE username = ?', [username])
        user = cur.fetchone()

        if user:
            user_id = user['id']
            db.execute('INSERT INTO posts (title, category, ingredients, steps, username, user_id, appliances) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       [title, category,ingredients, steps, username, user_id, appliances])
            db.commit()

            flash("Recipe added successfully!", "info")
            return redirect(url_for('show_feed'))
        else:
            flash("User not found", "error")
            return redirect(url_for('login'))
    else:
        flash("Please log in to submit a recipe", "error")
        return redirect(url_for('login'))

@app.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    if 'username' in session:
        db = get_db()
        db.execute('DELETE FROM posts WHERE id = ? AND username = ?', [post_id, session['username']])
        db.commit()
        flash("Post deleted successfully", "info")
    return redirect(url_for('show_feed'))

@app.route('/edit_post', methods=['POST'])
def edit_post():
    post_id = request.form['id']
    title = request.form['title']
    category = request.form['category']
    ingredients = request.form['ingredients']
    steps = request.form['steps']

    db = get_db()

    # this has an un-needed (but helpful double-check) conditional to check the user owns the post before actually executing the edit on the post
    db.execute("""UPDATE posts SET title = ?, category = ?, ingredients = ?, steps = ? WHERE id = ? AND username = ?""",
               (title, category, ingredients, steps, post_id, session['username']))
    db.commit()
    return redirect(url_for('show_feed'))

@app.route('/view_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def view_recipe(recipe_id):
    db = get_db()
    recipe = db.execute('SELECT * FROM posts WHERE id = ?',
                        (recipe_id,)).fetchone()

    if recipe is None:
        flash("Recipe not found", "error")
        return redirect(url_for('show_feed'))

    ingredients = recipe['ingredients'].split('\n') if recipe['ingredients'] else []
    instructions = recipe['steps'].split('\n') if recipe['steps'] else []
    appliances = recipe['appliances'].split('\n') if recipe['steps'] else []
    # optional for now must look deeper into
    comments = []

    return render_template('recipe_card.html', recipe=recipe, ingredients=ingredients, instructions=instructions, appliances=appliances, comments=comments)



@app.route('/add_to_cart/<int:recipe_id>', methods=['POST'])
def add_to_cart(recipe_id):
    db = get_db()
    recipe = db.execute("SELECT title, ingredients FROM posts WHERE id = ?",
                        (recipe_id,)).fetchone()

    # if the recipe exists
    if recipe:
        # store title, all ingredients, and list seperated ingredients split by the return from the input
        # had to look up some help of how to structure it (restructuring to fix all same cart error)
        title = recipe['title'] if isinstance(recipe, dict) else recipe[0]
        ingredients_str = recipe['ingredients'] if isinstance(recipe, dict) else recipe[1]
        ingredients_list = [item.strip() for item in ingredients_str.splitlines() if item.strip()]

        # if there is nothing in the cart already add a dictionary with the desired information from the recipe within
        if not any(isinstance(r, dict) and r.get('id') == recipe_id for r in session['cart']):
            item_to_add = {'id': recipe_id, 'title': title, 'ingredients': ingredients_list}
            session['cart'].append(item_to_add)
            session.modified = True
            flash(f'{title} ingredients added to your cart!', 'success')

        # ensures the recipe can not be added a million times to the cart, only once
        else:
            flash(f'{title} is already in your cart.', 'info')

    # this is a warning if something were to go wrong- a simple catch-all
    else:
        flash('Recipe not found.', 'warning')

    return redirect(url_for('show_cart'))


@app.route('/show_cart')
def show_cart():
    return render_template('cart.html', cart=session.get("cart", []))


@app.route('/remove_recipe/<int:recipe_id>', methods=['POST'])
def remove_recipe(recipe_id):
    cart = session.get('cart', [])
    session['cart'] = [r for r in cart if r.get('id') != recipe_id]
    session.modified = True
    flash('Recipe removed from cart.', 'info')
    return redirect(url_for('show_cart'))


@app.route('/mark_item/<int:recipe_id>/<item>', methods=['POST'])
def mark_item(recipe_id, item):
    cart = session.get('cart', [])

    for recipe in cart:
        if recipe.get('id') == recipe_id:
            # Remove the ingredient if it exists
            if item in recipe['ingredients']:
                recipe['ingredients'].remove(item)
                flash(f"Marked off '{item}' from {recipe['title']}.", 'info')
            break

    session['cart'] = cart
    session.modified = True
    return redirect(url_for('show_cart'))


@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    flash('Cart cleared.', 'info')
    return redirect(url_for('show_cart'))


@app.route('/user/<username>')
def show_user_profile(username):
    if 'username' not in session:
        return redirect(url_for('welcome_page'))
    
    db = get_db()
    cur = db.execute('SELECT * FROM users WHERE username = ?', [username])
    user = cur.fetchone()
    
    if user is not None:
        appliances = db.execute('SELECT * FROM appliances WHERE user_id = ?', [user['id']]).fetchone()
        recipes = db.execute('SELECT * FROM posts WHERE user_id = ? ORDER BY id DESC', [user['id']]).fetchall()
        return render_template('user_profile.html', user=user, appliances=appliances, recipes=recipes)
    else:
        flash("User does not exist", "error")
        return redirect(url_for('show_feed'))

@app.route('/add_comment/<int:recipe_id>', methods=['POST'])
def add_comment(recipe_id):
    comment_text = request.form.get("comment")

    db = get_db()
    db.execute('INSERT INTO comments (recipe_id, comment_text) VALUES (?,?)', (recipe_id, comment_text))
    db.commit()

    return redirect(url_for('show_recipe_card', recipe_id = recipe_id))

@app.route('/follow_user', methods=['POST'])
def follow_user():
    if 'username' in session and 'username' in request.form:
        db = get_db()
        cur = db.execute("SELECT following FROM users WHERE username = ?",
                              session['username'])
        old_list = cur.fetchone()
        new_list = old_list.split('|').append(request.form['username'])
        new_text = new_list.join('|')
        db.execute('UPDATE users SET following = new_text WHERE username = ?', session['username'])
        return redirect(url_for('show_feed'))
    else:
        flash("Failed to follow user")
        print_flashes()
        return redirect(url_for('show_feed'))
    

if __name__ == '__main__':
        app.run(debug=True)