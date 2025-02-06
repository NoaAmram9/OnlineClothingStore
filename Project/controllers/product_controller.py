from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from models.product_model import ProductModel  # Import the ProductModel for database operations
import os  # Import OS for file operations

# Create a Flask Blueprint for product-related routes
product_bp = Blueprint('product', __name__)

def create_product_controller(db_handler):
    """Creates product-related routes for the app."""
    
    def save_image(image):
        """Function to save uploaded image and return the filename."""
        if image:  # Check if an image is uploaded
            upload_folder = os.path.join(os.getcwd(), 'static', 'images')  # Define the upload folder path
            if not os.path.exists(upload_folder):  # Create folder if it doesn't exist
                os.makedirs(upload_folder)

            image_path = os.path.join(upload_folder, image.filename)  # Get full image path
            image.save(image_path)  # Save the image to the specified path
            return image.filename  # Return the filename for database storage
        return None  # Return None if no image is uploaded

    def check_admin():
        """Helper function to check if the user is an admin."""
        if 'is_admin' not in session or not session['is_admin']:  # Check admin session
            flash("You must be an admin to access this page.", "danger")
            return False  # Return False if the user is not an admin
        return True  # Return True if the user is an admin

    @product_bp.route('/add_product', methods=['GET', 'POST'])
    def add_product():
        """Route for adding a new product (Admin only)."""
        if not check_admin():  # Restrict access to admins
            return redirect(url_for('auth.login'))

        if request.method == 'POST':  # Handle form submission
            try:
                # Retrieve form data
                name = request.form.get('name')
                description = request.form.get('description')
                price = float(request.form.get('price', 0))
                size_s = int(request.form.get('size_s', 0))
                size_m = int(request.form.get('size_m', 0))
                size_l = int(request.form.get('size_l', 0))
                size_xl = int(request.form.get('size_xl', 0))
                image = request.files.get('image')  # Get uploaded image

                # Save image and get its filename
                image_path = save_image(image)

                if image_path:  # If image is successfully saved
                    product_model = ProductModel(db_handler)  # Create a ProductModel instance
                    product_model.add_product(
                        name, description, price, image_path,
                        size_s, size_m, size_l, size_xl
                    )
                    flash("Product added successfully!", "success")
                    return redirect(url_for('product.products'))  # Redirect to products page
                else:
                    flash("Error uploading image. Please try again.", "danger")
            except Exception as e:
                flash(f"Error adding product: {e}", "danger")

        return render_template('add_product.html')  # Render the add product form

    @product_bp.route('/products')
    def products():
        """Route for displaying all products."""
        try:
            product_model = ProductModel(db_handler)  # Create a ProductModel instance
            products = product_model.get_all_products()  # Fetch all products from the database
            return render_template('products.html', products=products)  # Render the products page
        except Exception as e:
            flash(f"Error fetching products: {e}", "danger")
            return redirect(url_for('home'))  # Redirect to home page if error occurs

    @product_bp.route('/product/<int:product_id>')
    def product_detail(product_id):
        """Route for displaying details of a specific product."""
        try:
            product_model = ProductModel(db_handler)  # Create a ProductModel instance
            product = product_model.get_product_details(product_id)  # Fetch product details
            if not product:
                flash("Product not found.", "danger")
                return redirect(url_for('product.products'))  # Redirect if product not found
            return render_template('product_detail.html', product=product)  # Render product details page
        except Exception as e:
            flash(f"Error fetching product details: {e}", "danger")
            return redirect(url_for('product.products'))  # Redirect in case of error

    @product_bp.route('/delete_product/<int:product_id>', methods=['POST'])
    def delete_product(product_id):
        """Route for deleting a product (Admin only)."""
        if not check_admin():  # Restrict access to admins
            return redirect(url_for('auth.login'))  

        try:
            product_model = ProductModel(db_handler)  # Create a ProductModel instance
            product_model.delete_product(product_id)  # Delete the product
            flash("Product deleted successfully!", "success")
            return redirect(url_for('product.products'))  # Redirect to products page
        except Exception as e:
            flash(f"Error deleting product: {e}", "danger")
            return redirect(url_for('product.products'))  # Redirect in case of error

    return product_bp  # Return the configured Blueprint
