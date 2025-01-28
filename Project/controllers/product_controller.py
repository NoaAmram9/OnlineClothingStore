from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from models.product_model import ProductModel
import os

# יצירת הבלופרינט של המוצרים
product_bp = Blueprint('product', __name__)

def create_product_controller(db_handler):
    """Creates product-related routes for the app."""
    
    def save_image(image):
        """Function to save uploaded image and return the filename."""
        if image:
            upload_folder = os.path.join(os.getcwd(), 'static', 'images')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            image_path = os.path.join(upload_folder, image.filename)
            image.save(image_path)
            return image.filename
        return None

    def check_admin():
        """Helper function to check if the user is an admin."""
        if 'is_admin' not in session or not session['is_admin']:
            flash("You must be an admin to access this page.", "danger")
            return False
        return True

    @product_bp.route('/add_product', methods=['GET', 'POST'])
    def add_product():
        """Route for adding a new product (Admin only)."""
        if not check_admin():
            return redirect(url_for('auth.login'))  # הפניה אם המשתמש לא מנהל

        if request.method == 'POST':
            try:
                # איסוף נתונים מהטופס
                name = request.form.get('name')
                description = request.form.get('description')
                price = float(request.form.get('price', 0))
                size_s = int(request.form.get('size_s', 0))
                size_m = int(request.form.get('size_m', 0))
                size_l = int(request.form.get('size_l', 0))
                size_xl = int(request.form.get('size_xl', 0))
                image = request.files.get('image')

                # שמירת התמונה
                image_path = save_image(image)

                if image_path:
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

    @product_bp.route('/products')
    def products():
        """Route for displaying all products."""
        try:
            product_model = ProductModel(db_handler)
            products = product_model.get_all_products()
            return render_template('products.html', products=products)
        except Exception as e:
            flash(f"Error fetching products: {e}", "danger")
            return redirect(url_for('home'))

    @product_bp.route('/product/<int:product_id>')
    def product_detail(product_id):
        """Route for displaying details of a specific product."""
        try:
            product_model = ProductModel(db_handler)
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
        """Route for deleting a product (Admin only)."""
        if not check_admin():
            return redirect(url_for('auth.login'))  # הפניה אם המשתמש לא מנהל

        try:
            product_model = ProductModel(db_handler)
            product_model.delete_product(product_id)
            flash("Product deleted successfully!", "success")
            return redirect(url_for('product.products'))
        except Exception as e:
            flash(f"Error deleting product: {e}", "danger")
            return redirect(url_for('product.products'))

    return product_bp
