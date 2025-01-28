from flask import Blueprint, render_template, flash, redirect, url_for, session
from models.user_model import UserModel

def create_users_controller(db_handler):
    # Create the blueprint for users
    user_bp = Blueprint('user', __name__)

    @user_bp.route('/users')
    def users():
        try:
            # Check if the user is logged in and has admin privileges
            if not session.get('is_admin'):
                flash("You must be an admin to view this page.", "danger")
                return redirect(url_for('auth.login'))

            # Initialize UserModel with db_handler
            user_model = UserModel(db_handler)
            users = user_model.get_all_users()

            # Render the users page with the fetched data
            return render_template('users.html', users=users)

        except Exception as e:
            # Log the exception and flash a user-friendly message
            print(f"Error fetching users: {e}")  # Log for debugging
            flash("An error occurred while fetching user data. Please try again later.", "danger")
            return redirect(url_for('home'))

    return user_bp
