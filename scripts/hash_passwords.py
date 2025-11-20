from app import app, get_db  # adjust import based on your app structure
from werkzeug.security import generate_password_hash

def hash_existing_passwords():
    with app.app_context():  # ensures Flask's `g` and config are available
        db = get_db()
        users = db.execute('SELECT id, password FROM users').fetchall()

        for user in users:
            user_id = user['id']
            raw_password = user['password']

            # Skip if already hashed (basic check for Werkzeug hash format)
            if not raw_password.startswith('pbkdf2:sha256:'):
                hashed = generate_password_hash(raw_password)
                db.execute(
                    'UPDATE users SET password = ? WHERE id = ?',
                    [hashed, user_id]
                )

        db.commit()
        print("✅ All plaintext passwords have been hashed.")

if __name__ == "__main__":
    hash_existing_passwords()
