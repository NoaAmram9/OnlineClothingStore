from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.cart_model import CartModel
from models.product_model import ProductModel

cart_bp = Blueprint('cart', __name__)

# Route to view the cart
@cart_bp.route('/cart')
def view_cart():
    cart_model = CartModel(session)
    cart = cart_model.get_cart()
    total_price = cart_model.get_total_price()
    return render_template('cart.html', cart=cart, total_price=total_price)

# Route to add a product to the cart
@cart_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product_model = ProductModel()  # Make sure the ProductModel is correctly initialized
    product = product_model.get_product_by_id(product_id)
    if product:
        cart_model = CartModel(session)
        cart_model.add_item(product_id, product['name'], product['price'])
        flash(f"{product['name']} added to your cart!", "success")
    else:
        flash("Product not found!", "danger")
    
    return redirect(url_for('product.closet'))  # Redirect back to the product list

# Route to remove a product from the cart
@cart_bp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart_model = CartModel(session)
    cart_model.remove_item(product_id)
    flash("Item removed from your cart.", "success")
    return redirect(url_for('cart.view_cart'))

# Route to update the quantity of a product in the cart
@cart_bp.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = int(request.form['quantity'])
    cart_model = CartModel(session)
    cart_model.update_item_quantity(product_id, quantity)
    flash("Cart updated.", "success")
    return redirect(url_for('cart.view_cart'))

# Route to finalize the order (dummy for now)
@cart_bp.route('/finalize_order', methods=['POST'])
def finalize_order():
    cart_model = CartModel(session)
    cart_model.clear_cart()
    flash("Order has been placed!", "success")
    return redirect(url_for('home'))  # Redirect to home after order is placed
