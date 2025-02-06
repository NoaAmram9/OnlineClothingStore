from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from models.product_model import ProductModel
import logging
# Set up logging
logging.basicConfig(level=logging.DEBUG)
cart_bp = Blueprint('cart', __name__)
# Create a Flask Blueprint for cart-related routes
def create_cart_controller(db_handler):
    """Creates cart-related routes for the app."""
#add to cart route
    @cart_bp.route('/add_to_cart', methods=['POST'])
    def add_to_cart():
        """Route for adding a product to the cart."""
        try:
            # Get product data from the form
            product_id = int(request.form.get('product_id'))
            product_name = request.form.get('product_name')
            product_price = float(request.form.get('product_price', 0))  # Default to 0.0 if missing
            quantity = int(request.form.get('quantity', 1))  # Default to 1 if not provided

            # Fetch product details from the database
            product_model = ProductModel(db_handler)
            product = product_model.get_product_details(product_id)
            
            if not product:
                flash("Product not found.", "danger")
                return redirect(url_for('product.products'))  # Redirect to products page

            # Ensure the cart exists in the session
            if 'cart' not in session:
                session['cart'] = []

            # Access the cart from the session
            cart = session['cart']
            product_in_cart = next((item for item in cart if item['product_id'] == product_id), None)
            
            if product_in_cart:
                # If product already exists in the cart, update the quantity
                product_in_cart['quantity'] += quantity
            else:
                # Add a new product to the cart
                cart.append({
                    'product_id': product_id,
                    'name': product_name,
                    'price': product_price,
                    'quantity': quantity
                })

            # Save the modified cart back to the session
            session.modified = True  
            flash(f"Added {quantity} of {product_name} to the cart.", "success")
            return redirect(url_for('product.products'))  # Redirect to the product page

        except Exception as e:
            logging.error(f"Error adding product to cart: {e}")
            flash(f"Error adding product to cart: {e}", "danger")
            return redirect(url_for('product.products'))

    @cart_bp.route('/view_cart')
    def view_cart():
        """Route for viewing the cart."""
        # Ensure the cart is available in the session
        cart = session.get('cart', [])

        # Validate and normalize cart data
        for item in cart:
            if 'price' not in item or item['price'] is None:
                item['price'] = 0.0  # Default to 0.0 if missing
            if 'quantity' not in item or item['quantity'] is None:
                item['quantity'] = 1  # Default to 1 if missing

        logging.debug(f"Cart contents: {cart}")  # Print cart to console for debugging
        if not cart:
            flash("Your cart is empty.", "info")
        return render_template('cart.html', cart=cart)

    @cart_bp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
    def remove_from_cart(product_id):
        """Route for removing a product from the cart."""
        try:
            # Access the cart from the session
            cart = session.get('cart', [])

            # Remove the product from the cart
            cart = [item for item in cart if item['product_id'] != product_id]
            session['cart'] = cart  # Update the session cart
            session.modified = True  # Ensure the session is updated

            flash("Product removed from cart.", "success")
            return redirect(url_for('cart.view_cart'))
        except Exception as e:
            logging.error(f"Error removing product from cart: {e}")
            flash(f"Error removing product from cart: {e}", "danger")
            return redirect(url_for('cart.view_cart'))
#checkout route
    @cart_bp.route('/checkout')
    def checkout():
        """Route for proceeding to checkout."""
        cart = session.get('cart', [])
        if not cart:
            flash("Your cart is empty.", "warning")
            return redirect(url_for('product.products'))  # Redirect to products if the cart is empty
        
        # Here, you can handle the checkout process (e.g., payment, order placement)
        flash("Proceeding to checkout.", "success")
        return render_template('checkout.html', cart=cart)

    return cart_bp
