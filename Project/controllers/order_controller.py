from flask import Blueprint, render_template, request, redirect, flash, session, url_for, current_app
from models.order_model import OrderModel
from models.product_model import ProductModel

# יצירת הבלופרינט להזמנות
order_bp = Blueprint('order', __name__)
db_handler = None  # יוגדר בזמן אתחול ה-Blueprint

def __init__(self, db_handler):
    if not db_handler:
        raise ValueError("db_handler is required!")
    self.db_handler = db_handler

@order_bp.route('/place_order', methods=['GET', 'POST'])
def place_order():
    """Route for placing a new order."""
    if request.method == 'POST':
        try:
            # בדיקה אם המשתמש מחובר
            if 'user' not in session:
                flash("Please log in to place an order.", "danger")
                return redirect(url_for('auth.login'))

            # איסוף נתונים מהטופס
            user_id = session['user_id']
            product_id = request.form['product_id']
            quantity = request.form['quantity']
            delivery_address = request.form['delivery_address']
            delivery_date = request.form['delivery_date']

            # יצירת הזמנה
            order_model = OrderModel(db_handler)
            order_model.create_order(user_id, product_id, quantity, delivery_address, delivery_date)

            flash("Order placed successfully!", "success")
            return redirect(url_for('order.my_orders'))
        except Exception as e:
            flash(f"Error placing order: {e}", "danger")
            return redirect(url_for('order.place_order'))

    # הצגת כל המוצרים להוספה להזמנה
    product_model = ProductModel(db_handler)
    products = product_model.get_all_products()
    return render_template('order.html', products=products)

@order_bp.route('/my_orders')
def my_orders():
    """Route for viewing all orders of the logged-in user."""
    if 'user' not in session:
        flash("Please log in to view your orders.", "danger")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    try:
        order_model = OrderModel(db_handler)
        orders = order_model.get_user_orders(user_id)
        return render_template('my_orders.html', orders=orders)
    except Exception as e:
        flash(f"Error fetching your orders: {e}", "danger")
        return redirect(url_for('home'))

@order_bp.route('/admin/orders')
def admin_orders():
    """Route for viewing all orders as an admin."""
    if not session.get('is_admin'):
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('auth.login'))

    try:
        order_model = OrderModel(db_handler)
        orders = order_model.get_all_orders()
        return render_template('admin_orders.html', orders=orders)
    except Exception as e:
        flash(f"Error fetching orders: {e}", "danger")
        return redirect(url_for('home'))
