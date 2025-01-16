import os
import sqlite3
from werkzeug.security import generate_password_hash

class DatabaseHandler:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.db_path = db_name  # Ensure consistent usage

    def connect(self):
        return sqlite3.connect(self.db_name)

    def execute_query(self, query, params=()):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error executing query: {e}")

    def fetch_query(self, query, params=()):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            conn.close()
            return result
        except Exception as e:
            print(f"Error fetching query: {e}")
            return []

    def delete_db(self):
        """Delete the existing database file"""
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
            print(f"Database {self.db_name} deleted.")
        else:
            print(f"Database {self.db_name} does not exist.")

    def init_db(self):
        """Initialize the database and create tables."""
        conn = self.connect()
        cursor = conn.cursor()

        # Create users table with the 'is_admin' column
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            email TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            is_admin BOOLEAN DEFAULT FALSE)''')

        # Create products table
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            description TEXT,
                            price REAL NOT NULL,
                            image TEXT,
                            size_s INTEGER DEFAULT 0,
                            size_m INTEGER DEFAULT 0,
                            size_l INTEGER DEFAULT 0,
                            size_xl INTEGER DEFAULT 0)''')

        # Create orders table
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            product_id INTEGER NOT NULL,
                            quantity INTEGER NOT NULL,
                            total_price REAL NOT NULL,
                            status TEXT DEFAULT 'pending',
                            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            delivery_address TEXT,
                            delivery_date DATE,
                            FOREIGN KEY(user_id) REFERENCES users(id),
                            FOREIGN KEY(product_id) REFERENCES products(id))''')

        conn.commit()
        conn.close()
        print("Database initialized.")

    def create_admin(self):
        """
        Insert a default admin user if it doesn't already exist.
        """
        try:
            hashed_password = generate_password_hash("password123")  # Securely hash the default password
            query = """
                INSERT OR IGNORE INTO users (username, email, password, is_admin) 
                VALUES (?, ?, ?, ?)
            """
            self.execute_query(query, ("admin", "admin@example.com", hashed_password, True))
            print("Admin user created.")
        except Exception as e:
            print(f"Error creating admin user: {e}")