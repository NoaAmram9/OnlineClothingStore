import pyodbc
from werkzeug.security import generate_password_hash, check_password_hash
from database_handler import DatabaseHandler  # יש לוודא ש-DatabaseHandler מותאם לשימוש ב-ODBC

class UserModel:
    def __init__(self, db_handler=None):
        # חיבור למסד נתונים דרך ODBC
        self.db_handler = db_handler if db_handler else DatabaseHandler()

    def register_user(self, username, email, password):
        try:
            hashed_password = generate_password_hash(password)  # Hash the password
            query = """
                INSERT INTO users (username, email, password, is_admin) 
                VALUES (?, ?, ?, ?)
            """
            self.db_handler.execute_query(query, (username, email, hashed_password, False))  # Always False for now
            return True  # Indicate success
        except pyodbc.IntegrityError as e:
            print(f"Database error during registration: {e}")
            return False  # Failure due to duplicate username/email
        except Exception as e:
            print(f"Unexpected error during registration: {e}")
            return False
    
    def authenticate_user(self, username, password):
     """Authenticate a user based on username and password."""
     query = "SELECT * FROM users WHERE username = ?"
     user = self.db_handler.fetch_query(query, (username,))
    
     print(f"Fetched user: {user}")  # Debug: Show the fetched user object
    
     if user:
        stored_password = user[0][3]  # Assuming user[0][3] is the password hash
        print(f"Stored password: {stored_password}, Provided password: {password}")  # Debug
        
        if check_password_hash(stored_password, password):
            print("Password verification succeeded.")  # Debug
            return user[0]
        else:
            print("Password verification failed.")  # Debug
     else:
        print("No user found.")  # Debug
    
     return None  # Return None if no match

    def get_all_users(self):
        """Fetch all users from the database"""
        query = "SELECT * FROM users"
        return self.db_handler.fetch_query(query)

    def get_user_by_id(self, user_id):
        """Fetch a user by their ID."""
        query = "SELECT * FROM users WHERE id = ?"
        result = self.db_handler.fetch_query(query, (user_id,))
        return result[0] if result else None
