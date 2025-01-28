import pyodbc
from werkzeug.security import generate_password_hash

class DatabaseHandler:
    def __init__(self, db_path='database.accdb'):
        self.db_path = db_path
        self.connection_string = (
            f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};"
            f"DBQ={self.db_path};"
        )

    def connect(self):
        """Connect to the Access database"""
        try:
            return pyodbc.connect(self.connection_string)
        except pyodbc.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def execute_query(self, query, params=()):
        try:
            conn = self.connect()
            if conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                conn.close()
        except Exception as e:
            print(f"Error executing query: {e}")
            if conn:
                conn.close()

    def fetch_query(self, query, params=()):
        try:
            conn = self.connect()
            if conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                result = cursor.fetchall()
                conn.close()
                return result
        except Exception as e:
            print(f"Error fetching query: {e}")
            if conn:
                conn.close()
            return []

    def init_db(self):
        """Initialize the database and create tables."""
        try:
            conn = self.connect()
            if conn:
                cursor = conn.cursor()

                 # בדוק אם הטבלה 'users' קיימת
            cursor.execute("SELECT name FROM MSysObjects WHERE type=1 AND name='users'")
            if not cursor.fetchall():
                # יצירת טבלת users אם לא קיימת
                cursor.execute('''CREATE TABLE users (
                                    id AUTOINCREMENT PRIMARY KEY,
                                    username TEXT UNIQUE NOT NULL,
                                    email TEXT UNIQUE NOT NULL,
                                    password TEXT NOT NULL,
                                    is_admin YESNO DEFAULT FALSE)''')

            # בדוק אם הטבלה 'products' קיימת
            cursor.execute("SELECT name FROM MSysObjects WHERE type=1 AND name='products'")
            if not cursor.fetchall():
                # יצירת טבלת products אם לא קיימת
                cursor.execute('''CREATE TABLE products (
                                    id AUTOINCREMENT PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    description TEXT,
                                    price DOUBLE NOT NULL,
                                    image TEXT,
                                    size_s INTEGER DEFAULT 0,
                                    size_m INTEGER DEFAULT 0,
                                    size_l INTEGER DEFAULT 0,
                                    size_xl INTEGER DEFAULT 0)''')

            # בדוק אם הטבלה 'orders' קיימת
            cursor.execute("SELECT name FROM MSysObjects WHERE type=1 AND name='orders'")
            if not cursor.fetchall():
                # יצירת טבלת orders אם לא קיימת
                cursor.execute('''CREATE TABLE orders (
                                    id AUTOINCREMENT PRIMARY KEY,
                                    user_id INTEGER NOT NULL,
                                    product_id INTEGER NOT NULL,
                                    quantity INTEGER NOT NULL,
                                    total_price DOUBLE NOT NULL,
                                    status TEXT DEFAULT 'pending',
                                    order_date DATETIME DEFAULT NOW(),
                                    delivery_address TEXT,
                                    delivery_date DATE,
                                    FOREIGN KEY(user_id) REFERENCES users(id),
                                    FOREIGN KEY(product_id) REFERENCES products(id))''')

            # בדוק אם הטבלה 'cart_items' קיימת
            cursor.execute("SELECT name FROM MSysObjects WHERE type=1 AND name='cart_items'")
            if not cursor.fetchall():
                # יצירת טבלת cart_items אם לא קיימת
                cursor.execute('''CREATE TABLE cart_items (
                                   id AUTOINCREMENT PRIMARY KEY,
                                   user_id INTEGER NOT NULL,
                                   product_id INTEGER NOT NULL,
                                   quantity INTEGER NOT NULL,
                                   FOREIGN KEY(user_id) REFERENCES users(id),
                                   FOREIGN KEY(product_id) REFERENCES products(id))''')

                conn.commit()
                conn.close()
                print("Database initialized.")
        except Exception as e:
            print(f"Error initializing database: {e}")
            
    def create_admin(self):
     """Create a default admin user if not exists."""
     # Check if an admin user already exists
     query = "SELECT * FROM users WHERE is_admin = ?"
     result = self.fetch_query(query, ('-1',))  # Query for admin with is_admin = '-1'

     if not result:
        # Create a default admin if not exists
        admin_username = "admin"
        admin_email = "admin@example.com"
        admin_password = 'password123'  # Default admin password
        hashed_password = generate_password_hash(admin_password, method='scrypt')

        # Insert the admin user into the database
        query = '''
            INSERT INTO users (username, email, password, is_admin) 
            VALUES (?, ?, ?, ?)
        '''
        params = (admin_username, admin_email, hashed_password, '-1')
        self.execute_query(query, params)

        print("Admin user created successfully.")
     else:
        print("Admin user already exists.")