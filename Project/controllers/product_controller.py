from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from models.product_model import ProductModel
import os

# Create the product blueprint
product_bp = Blueprint('product', __name__)

def create_product_controller(db_handler):
    """Creates product-related routes for the app."""
    
    def save_image(image):
     if image:
        upload_folder = os.path.join(os.getcwd(), 'static', 'images')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        image_path = os.path.join(upload_folder, image.filename)
        image.save(image_path)

        # Return the filename, not the full path
        return image.filename
     return None

    @product_bp.route('/add_product', methods=['GET', 'POST'])
    def add_product():
        """Route for adding a new product (Admin only)."""
        if 'is_admin' in session and session['is_admin']:  # Check if the user is an admin
            if request.method == 'POST':
                try:
                    # Collect form data
                    name = request.form.get('name')
                    description = request.form.get('description')
                    price = float(request.form.get('price', 0))
                    size_s = int(request.form.get('size_s', 0))
                    size_m = int(request.form.get('size_m', 0))
                    size_l = int(request.form.get('size_l', 0))
                    size_xl = int(request.form.get('size_xl', 0))
                    image = request.files.get('image')

                    # Save the image
                    image_path = save_image(image)

                    if image_path:
                        # Add product to the database
                        product_model = ProductModel(db_handler)
                        product_model.add_product(
                            name, description, price, image_path,
                            size_s, size_m, size_l, size_xl
                        )
                        flash("Product added successfully!", "success")
                        return redirect(url_for('product.products'))
                    else:
                        flash("Error uploading image. Please try again.", "danger")
                except Exception as e:
                    flash(f"Error adding product: {e}", "danger")

            return render_template('add_product.html')
        else:
            flash("You must be an admin to access this page.", "danger")
            return redirect(url_for('auth.login'))  # Redirect to login page if not admin

    @product_bp.route('/products')
    def products():
        """Route for displaying all products."""
        try:
            product_model = ProductModel(db_handler)
            products = product_model.get_all_products()
            return render_template('products.html', products=products)
        except Exception as e:
            flash(f"Error fetching products: {e}", "danger")
            return redirect(url_for('home'))  # Redirect to home or any other fallback page
    
    @product_bp.route('/product/<int:product_id>')
    def product_detail(product_id):
      try:
        product_model = ProductModel(db_handler)  # Ensure ProductModel uses the db_handler
        product = product_model.get_product_details(product_id)
        if not product:
            flash("Product not found.", "danger")
            return redirect(url_for('product.products'))
        return render_template('product_detail.html', product=product)
      except Exception as e:
        flash(f"Error fetching product details: {e}", "danger")
        return redirect(url_for('product.products'))
    
    @product_bp.route('/delete_product/<int:product_id>', methods=['POST'])
    def delete_product(product_id):
      if 'is_admin' in session and session['is_admin']:  # Check if the user is an admin
        try:
            product_model = ProductModel(db_handler)
            product_model.delete_product(product_id)  # Delete product by ID

            flash("Product deleted successfully!", "success")
            return redirect(url_for('product.products'))  # Redirect to products page after deletion
        except Exception as e:
            flash(f"Error deleting product: {e}", "danger")
            return redirect(url_for('product.products'))  # Stay on products page in case of error
      else:
        flash("You must be an admin to delete a product.", "danger")
        return redirect(url_for('auth.login'))  # Redirect to login page if not an admin


    return product_bp
