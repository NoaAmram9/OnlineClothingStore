class OrderModel:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def create_order(self, user_id, product_id, quantity, delivery_address, delivery_date):
        # Fetching product details
        product_query = "SELECT name, price FROM products WHERE id = ?"
        product = self.db_handler.fetch_query(product_query, (product_id,))

        if not product:
            raise ValueError("Product not found!")

        product_name = product[0][0]  # Assuming product name is in the first column
        price = product[0][1]         # Price is in the second column
        total_price = price * quantity  # Calculate the total price

        try:
            # Insert the order into the database
            order_query = '''INSERT INTO orders (user_id, product_id, product_name, quantity, total_price, 
                                delivery_address, delivery_date, status)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
            # Default order status can be "pending" upon creation
            self.db_handler.execute_query(order_query, 
                                          (user_id, product_id, product_name, quantity, total_price, 
                                           delivery_address, delivery_date, "pending"))
            return "Order placed successfully"
        except Exception as e:
            raise Exception(f"Error placing order: {str(e)}")

    def get_user_orders(self, user_id):
        try:
            query = "SELECT * FROM orders WHERE user_id = ?"
            return self.db_handler.fetch_query(query, (user_id,))
        except Exception as e:
            raise Exception(f"Error fetching user orders: {str(e)}")

    def get_all_orders(self):
        try:
            query = '''SELECT o.id, u.name AS customer_name, p.name AS product_name, o.quantity, 
                              o.total_price, o.delivery_address, o.delivery_date, o.status
                       FROM orders o
                       JOIN products p ON o.product_id = p.id
                       JOIN users u ON o.user_id = u.id'''
            result = self.db_handler.fetch_query(query)

            if not result:
                return []

            orders = []
            for row in result:
                order = {
                    'id': row[0],
                    'customer_name': row[1],
                    'product_name': row[2],
                    'quantity': row[3],
                    'total_price': row[4],
                    'delivery_address': row[5],
                    'delivery_date': row[6],
                    'status': row[7]
                }
                orders.append(order)

            return orders
        except Exception as e:
            raise Exception(f"Error fetching all orders: {str(e)}")

    def update_order_status(self, order_id, new_status):
        try:
            # Validate status before updating (you may define a list of valid statuses)
            valid_statuses = ["pending", "shipped", "delivered", "cancelled"]
            if new_status not in valid_statuses:
                raise ValueError("Invalid status value.")

            query = "UPDATE orders SET status = ? WHERE id = ?"
            self.db_handler.execute_query(query, (new_status, order_id))
        except Exception as e:
            raise Exception(f"Error updating order status: {str(e)}")
