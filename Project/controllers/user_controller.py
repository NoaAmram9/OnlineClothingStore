from flask import Blueprint, render_template, flash, redirect, url_for, session
from models.user_model import UserModel
from models.product_model import ProductModel

user_bp = Blueprint('user', __name__)

@user_bp.route('/users')
def users():
    try:
        # Check if the user is logged in and has admin privileges
        if 'is_admin' not in session or not session['is_admin']:
            flash("You must be an admin to view this page", "danger")
            return redirect(url_for('auth.login'))  # Redirect to login page if not admin

        # Initialize UserModel and fetch all users from the database
        user_model = UserModel()
        users = user_model.get_all_users()

        # Render the 'users.html' template with the fetched users
        return render_template('users.html', users=users)
    except Exception as e:
        flash(f"Error fetching users: {e}", "danger")
        return redirect(url_for('home'))  # Redirect to home or any other fallback page
