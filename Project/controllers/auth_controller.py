# from flask import Blueprint, render_template, request, redirect, flash, session, url_for
# from models.user_model import UserModel

# auth_bp = Blueprint('auth', __name__)
# user_model = UserModel()  # Initialize with DatabaseHandler as needed

# @auth_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form["email"]
        
#         # Attempt to register the user
#         success = user_model.register_user(username, email, password)
#         if success:
#             flash("You have successfully registered", "success")
#             return redirect(url_for('auth.login'))
#         else:
#             flash("Registration failed, please try again.", "danger")
    
#     return render_template('register.html')

# @auth_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         try:
#             username = request.form['username']
#             password = request.form['password']
            
#             # Authenticate user using the UserModel
#             user = user_model.authenticate_user(username, password)
            
#             if user:
#                 # Store user info in the session
#                 session['user'] = username
#                 session['user_id'] = user[0]  # Assuming user[0] is the ID
#                 session['is_admin'] = user[4]  # Assuming user[3] is the is_admin flag
#                 flash(f"Welcome back, {username}!", "success")
#                 return redirect(url_for('home'))
#             else:
#                 flash('Invalid username or password', 'danger')
#         except Exception as e:
#             flash(f"Error logging in: {e}", "danger")
    
#     return render_template('login.html')

# @auth_bp.route('/logout')
# def logout():
#     # Clear session data
#     session.pop('user', None)
#     session.pop('is_admin', None)
#     session.pop('user_id', None)
#     flash("You have been logged out.", "info")
#     return redirect(url_for('home'))
from flask import Blueprint, render_template, request, redirect, flash, session, url_for, current_app
from models.user_model import UserModel

auth_bp = Blueprint('auth', __name__)

# יצירת המודל עם db_handler
def create_user_model():
    db_handler = current_app.config['DB_HANDLER']  
    return UserModel(db_handler)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form["email"]

        # בדיקת שדות ריקים
        if not username or not password or not email:
            flash("All fields are required!", "danger")
            return render_template('register.html')
        
        # יצירת מודל משתמש עם db_handler
        user_model = create_user_model()

        # ניסיון לרשום את המשתמש
        success = user_model.register_user(username, email, password)
        if success:
            flash("You have successfully registered", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("Registration failed, please try again.", "danger")
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            if not username or not password:
                flash("Please provide both username and password", "danger")
                return render_template('login.html')
            
            user_model = create_user_model()
            user = user_model.authenticate_user(username, password)
            
            if user:
                session['user'] = username
                session['user_id'] = user[0]
                session['is_admin'] = user[4]

                flash(f"Welcome back, {username}!", "success")
                if user[4] == -1:  # Redirect admins to the admin dashboard
                    return redirect(url_for('home'))
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'danger')
        except Exception as e:
            flash(f"Error logging in: {e}", "danger")
            
    return render_template('login.html')
@auth_bp.route('/logout')
def logout():
    # ניקוי נתוני session
    session.pop('user', None)
    session.pop('is_admin', None)
    session.pop('user_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))
