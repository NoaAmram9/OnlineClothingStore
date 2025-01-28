from database_handler import DatabaseHandler

class CartModel:
    def __init__(self, session, user_id, db_handler):
        self.session = session
        self.user_id = user_id
        self.db_handler = db_handler
        if 'cart' not in session:
            session['cart'] = {}  # Initialize an empty cart if it doesn't exist
        self.load_cart_from_db()

    def load_cart_from_db(self):
        """Load the cart items from the database for the given user."""
        query = "SELECT product_id, quantity FROM cart_items WHERE user_id = ?"
        cart_items = self.db_handler.fetch_query(query, (self.user_id,))
        for product_id, quantity in cart_items:
            self.session['cart'][product_id] = {'quantity': quantity}
    
    def save_cart_to_db(self):
        """Save the current session cart to the database."""
        for product_id, item in self.session['cart'].items():
            # Insert or update the cart item in the database
            query = """
                INSERT INTO cart_items (user_id, product_id, quantity) 
                VALUES (?, ?, ?)
                ON CONFLICT(user_id, product_id) DO UPDATE SET quantity = ?
            """
            self.db_handler.execute_query(query, (self.user_id, product_id, item['quantity'], item['quantity']))

    def add_item(self, product_id, name, price, quantity=1):
        """Add a product to the cart."""
        cart = self.session['cart']
        if product_id in cart:
            cart[product_id]['quantity'] += quantity  # Update quantity if product already exists
        else:
            cart[product_id] = {'name': name, 'price': price, 'quantity': quantity}
        self.save_cart_to_db()

    def remove_item(self, product_id):
        """Remove a product from the cart."""
        cart = self.session['cart']
        if product_id in cart:
            del cart[product_id]
        self.save_cart_to_db()

    def update_item_quantity(self, product_id, quantity):
        """Update the quantity of an existing product in the cart"""
        cart = self.session['cart']
        if product_id in cart:
            if quantity <= 0:
                self.remove_item(product_id)  # If quantity is 0 or less, remove the product
            else:
                cart[product_id]['quantity'] = quantity
        self.save_cart_to_db()

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
        # Clear the cart in the database as well
        query = "DELETE FROM cart_items WHERE user_id = ?"
        self.db_handler.execute_query(query, (self.user_id,))
