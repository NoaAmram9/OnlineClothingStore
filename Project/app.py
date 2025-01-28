from flask import Flask, render_template
from database_handler import DatabaseHandler
from controllers.user_controller import create_users_controller
from controllers.order_controller import order_bp
from controllers.auth_controller import auth_bp
from controllers.product_controller import create_product_controller
from controllers.cart_controller import create_cart_controller  # Import the cart controller

# Initialize the Flask app
app = Flask(__name__, template_folder='views/templates', static_url_path='/static', static_folder='static')

# Configurations
app.secret_key = 'your_secret_key'  # Secret key for session management
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize the DatabaseHandler with Access database
db_handler = DatabaseHandler(db_path='C:/Users/noaam/Desktop/ASP/ClothingStroreNew/OnlineClothingStore/project/database.accdb')
db_handler.init_db()       # Initialize the database and create tables
db_handler.create_admin()  # Create the default admin user

# Pass the DatabaseHandler to controllers
product_bp = create_product_controller(db_handler)  # Pass db_handler to product controller
user_bp = create_users_controller(db_handler)       # Pass db_handler to user controller
cart_bp = create_cart_controller(db_handler)        # Pass db_handler to cart controller

# Attach db_handler to the app configuration
app.config['DB_HANDLER'] = db_handler

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(order_bp, url_prefix='/order')
app.register_blueprint(product_bp, url_prefix='/product')
app.register_blueprint(cart_bp, url_prefix='/cart')
app.register_blueprint(user_bp, url_prefix='/user')

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

