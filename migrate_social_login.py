"""
Migration script: adds facebook_id and apple_sub to users.
Run once: python migrate_social_login.py
"""
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance", "personal.db")


def migrate():
    if not os.path.exists(DB_PATH):
        print("No database found — nothing to migrate. Run the app to create it.")
        return

    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA foreign_keys = ON")

    user_cols = [row[1] for row in db.execute("PRAGMA table_info(users)").fetchall()]
    if "facebook_id" not in user_cols:
        db.execute("ALTER TABLE users ADD COLUMN facebook_id TEXT")
        db.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_facebook_id ON users(facebook_id)")
        print("Added 'facebook_id' column to users.")
    else:
        print("'facebook_id' column already exists in users.")

    if "apple_sub" not in user_cols:
        db.execute("ALTER TABLE users ADD COLUMN apple_sub TEXT")
        db.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_apple_sub ON users(apple_sub)")
        print("Added 'apple_sub' column to users.")
    else:
        print("'apple_sub' column already exists in users.")

    db.commit()
    db.close()
    print("Migration complete.")


if __name__ == "__main__":
    migrate()
