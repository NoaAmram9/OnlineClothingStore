from database_handler import DatabaseHandler

class CartModel:
    def __init__(self, session):
        self.session = session
        if 'cart' not in session:
            session['cart'] = {}  # Initialize an empty cart if it doesn't exist

    def add_item(self, product_id, name, price, quantity=1):
        """Add a product to the cart."""
        cart = self.session['cart']
        if product_id in cart:
            cart[product_id]['quantity'] += quantity  # Update quantity if product already exists
        else:
            cart[product_id] = {'name': name, 'price': price, 'quantity': quantity}

    def remove_item(self, product_id):
        """Remove a product from the cart."""
        cart = self.session['cart']
        if product_id in cart:
            del cart[product_id]

    def update_item_quantity(self, product_id, quantity):
        """Update the quantity of an existing product in the cart"""
        cart = self.session['cart']
        if product_id in cart:
            if quantity <= 0:
                self.remove_item(product_id)  # If quantity is 0 or less, remove the product
            else:
                cart[product_id]['quantity'] = quantity

    def get_cart(self):
        """Retrieve the current cart."""
        return self.session['cart']

    def get_total_price(self):
        """Calculate the total price of all items in the cart."""
        total = 0
        for item in self.session['cart'].values():
            total += item['price'] * item['quantity']
        return total

    def clear_cart(self):
        """Clear the cart."""
        self.session['cart'] = {}
