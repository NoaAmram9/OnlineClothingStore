import os
from database_handler import DatabaseHandler

class ProductModel:
    def __init__(self, db_handler=None):
        self.db_handler = db_handler

    def add_product(self, name, description, price, image, size_s, size_m, size_l, size_xl):
        """Adds a new product to the database"""
        try:
            query = '''INSERT INTO products 
                       (name, description, price, image, size_s, size_m, size_l, size_xl) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
            self.db_handler.execute_query(query, (name, description, price, image, size_s, size_m, size_l, size_xl))
        except Exception as e:
            print(f"Error adding product: {e}")
            
    def get_all_products(self):
        try:
            query = "SELECT * FROM products"
            raw_products = self.db_handler.fetch_query(query)
            products = [
                {
                    'id': product[0],
                    'name': product[1],
                    'description': product[2],
                    'price': product[3],
                    'image': product[4],
                    'sizes': {
                        'S': product[5],
                        'M': product[6],
                        'L': product[7],
                        'XL': product[8]
                    }
                }
                for product in raw_products
            ]
            return products
        except Exception as e:
            print(f"Error fetching all products: {e}")
            return []

    def get_product_details(self, product_id):
        """Fetches details of a specific product."""
        try:
            query = "SELECT * FROM products WHERE id = ?"
            result = self.db_handler.fetch_query(query, (product_id,))
            if result:
                product = result[0]  # Assuming result is a list of tuples
                product_details = {
                    'id': product[0],
                    'name': product[1],
                    'description': product[2],
                    'price': product[3],
                    'image': product[4],
                    'sizes': {
                        'S': product[5],
                        'M': product[6],
                        'L': product[7],
                        'XL': product[8]  # Assuming size_xl is at the 8th position
                    }
                }
                return product_details
            return None
        except Exception as e:
            print(f"Error fetching product details: {e}")
            return None

    def get_products_by_category(self, category):
        """Fetches products by category."""
        try:
            query = "SELECT * FROM products WHERE category = ?"
            return self.db_handler.fetch_query(query, (category,))
        except Exception as e:
            print(f"Error fetching products by category: {e}")
            return []

    def get_products_by_price_range(self, min_price, max_price):
        """Fetches products within a given price range."""
        try:
            query = "SELECT * FROM products WHERE price BETWEEN ? AND ?"
            return self.db_handler.fetch_query(query, (min_price, max_price))
        except Exception as e:
            print(f"Error fetching products by price range: {e}")
            return []
        
    def delete_product(self, product_id):
        # Get the image path before deleting the product (if exists)
        conn = self.db_handler.connect()  # Get the connection from db_handler
        cursor = conn.cursor()  # Create a cursor from the connection

        # Fetch the image path from the product
        query = "SELECT image FROM products WHERE id = ?"
        cursor.execute(query, (product_id,))  # Execute the query
        result = cursor.fetchone()

        if result:
            image_path = result[0]  # Assuming the image path is in the first column
            if image_path and os.path.exists(image_path):
                os.remove(image_path)  # Delete the image file from the server

        # Now delete the product from the database
        query = "DELETE FROM products WHERE id = ?"
        cursor.execute(query, (product_id,))  # Run the delete query
        conn.commit()  # Commit the transaction to save changes
        conn.close()  # Close the connection