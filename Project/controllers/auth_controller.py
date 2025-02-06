from flask import Blueprint, render_template, request, redirect, flash, session, url_for, current_app
from models.user_model import UserModel

# Create a Blueprint for authentication-related routes
auth_bp = Blueprint('auth', __name__)

def create_user_model():
    """
    Helper function to create an instance of the UserModel with the 
    application's database handler.
    """
    db_handler = current_app.config['DB_HANDLER']  # Retrieve the database handler from the app config
    return UserModel(db_handler)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.
    - If the request method is GET, renders the registration form.
    - If the request method is POST, processes the form submission,
      validates input, and attempts to register the user.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form["email"]

        # Validate input: Ensure all required fields are filled
        if not username or not password or not email:
            flash("All fields are required!", "danger")
            return render_template('register.html')
    
        # Create a UserModel instance to interact with the database
        user_model = create_user_model()

        # Attempt to register the user
        success = user_model.register_user(username, email, password)
        if success:
            flash("You have successfully registered", "success")
            return redirect(url_for('auth.login'))  # Redirect to login page upon successful registration
        else:
            flash("Registration failed, please try again.", "danger")  # Show error message if registration fails
    
    # Render the registration form for GET requests or after a failed registration
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.
    - If the request method is GET, renders the login form.
    - If the request method is POST, processes the form submission,
      validates credentials, and logs in the user if valid.
    """
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            # Validate input: Ensure both username and password are provided
            if not username or not password:
                flash("Please provide both username and password", "danger")
                return render_template('login.html')
            
            # Create a UserModel instance to interact with the database
            user_model = create_user_model()
            
            # Authenticate the user
            user = user_model.authenticate_user(username, password)
            
            if user:
                # Store user session data
                session['user'] = username
                session['user_id'] = user[0]  # Assuming user[0] is the user ID
                session['is_admin'] = user[4]  # Assuming user[4] indicates admin status

                flash(f"Welcome back, {username}!", "success")

                # Redirect admins to the admin dashboard, otherwise to home
                if user[4] == -1:  
                    return redirect(url_for('home'))  # Admin dashboard (modify if needed)
                return redirect(url_for('home'))  # Redirect normal users to the homepage
            else:
                flash('Invalid username or password', 'danger')  # Show error if authentication fails
        except Exception as e:
            flash(f"Error logging in: {e}", "danger")  # Handle unexpected errors
            
    # Render the login form for GET requests or after a failed login attempt
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """
    Handles user logout.
    - Clears session data and redirects the user to the homepage.
    """
    session.pop('user', None)  # Remove the user from session
    session.pop('is_admin', None)  # Remove admin status from session
    session.pop('user_id', None)  # Remove user ID from session
    flash("You have been logged out.", "info")  # Inform the user they have logged out
    return redirect(url_for('home'))  # Redirect to the homepage
