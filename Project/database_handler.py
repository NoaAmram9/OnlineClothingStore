import pyodbc
from werkzeug.security import generate_password_hash
# Import the generate_password_hash function from the werkzeug.security module
class DatabaseHandler:
    def __init__(self, db_path='database.accdb'):
        """
        Initializes the DatabaseHandler class with a connection string to an 
        Access database file.
        
        :param db_path: Path to the Access database file (.accdb)
        """
        self.db_path = db_path
        self.connection_string = (
            f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};"
            f"DBQ={self.db_path};"
        )

    def connect(self):
        """
        Establishes a connection to the Access database.

        :return: Database connection object or None if connection fails.
        """
        try:
            return pyodbc.connect(self.connection_string)
        except pyodbc.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def execute_query(self, query, params=()):
        """
        Executes an SQL query that modifies the database (INSERT, UPDATE, DELETE).

        :param query: SQL query to execute.
        :param params: Parameters to be passed to the query (to prevent SQL injection).
        """
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
        """
        Executes a SELECT query and fetches results.

        :param query: SQL SELECT query to execute.
        :param params: Parameters for the query.
        :return: List of query results or an empty list if an error occurs.
        """
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
        """
        Initializes the database by creating necessary tables if they do not exist.
        This function ensures that the application has all required tables for 
        users, products, orders, and cart items.
        """
        try:
            conn = self.connect()
            if conn:
                cursor = conn.cursor()

                # Check if the 'users' table exists
                cursor.execute("SELECT name FROM MSysObjects WHERE type=1 AND name='users'")
                if not cursor.fetchall():
                    # Create the 'users' table if it doesn't exist
                    cursor.execute('''CREATE TABLE users (
                                        id AUTOINCREMENT PRIMARY KEY,
                                        username TEXT UNIQUE NOT NULL,
                                        email TEXT UNIQUE NOT NULL,
                                        password TEXT NOT NULL,
                                        is_admin YESNO DEFAULT FALSE)''')

                # Check if the 'products' table exists
                cursor.execute("SELECT name FROM MSysObjects WHERE type=1 AND name='products'")
                if not cursor.fetchall():
                    # Create the 'products' table if it doesn't exist
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

                # Check if the 'orders' table exists
                cursor.execute("SELECT name FROM MSysObjects WHERE type=1 AND name='orders'")
                if not cursor.fetchall():
                    # Create the 'orders' table if it doesn't exist
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

                # Check if the 'cart_items' table exists
                cursor.execute("SELECT name FROM MSysObjects WHERE type=1 AND name='cart_items'")
                if not cursor.fetchall():
                    # Create the 'cart_items' table if it doesn't exist
                    cursor.execute('''CREATE TABLE cart_items (
                                       id AUTOINCREMENT PRIMARY KEY,
                                       user_id INTEGER NOT NULL,
                                       product_id INTEGER NOT NULL,
                                       quantity INTEGER NOT NULL,
                                       FOREIGN KEY(user_id) REFERENCES users(id),
                                       FOREIGN KEY(product_id) REFERENCES products(id))''')

                conn.commit()
                conn.close()
                print("Database initialized successfully.")
        except Exception as e:
            print(f"Error initializing database: {e}")

    def create_admin(self):
        """
        Creates a default admin user if one does not already exist.
        The admin user has:
        - Username: "admin"
        - Email: "admin@example.com"
        - Password: "password123" (hashed for security)
        - is_admin: -1 (indicating admin privileges)
        """
        # Check if an admin user already exists
        query = "SELECT * FROM users WHERE is_admin = ?"
        result = self.fetch_query(query, ('-1',))  # Query for admin with is_admin = '-1'

        if not result:
            # Default admin credentials
            admin_username = "admin" # Default admin username
            admin_email = "admin@example.com" # Default admin email
            admin_password = 'password123'  # Default admin password

            # Hash the admin password for security
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
