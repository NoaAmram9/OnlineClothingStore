# Online Clothing Store

This project is a Flask-based web application for managing an online clothing store. It includes functionality for user authentication, product management, order placement, and cart management.
### Visual details about the site and its use can be found on the WIKI.

---

## Prerequisites

Before running the application, ensure you have the following installed on your system:

1. **Python** (version 3.7 or higher)
2. **Microsoft Access Database**
3. **Required Python libraries** (specified in `requirements.txt`)

---

## Setup Instructions

### 1. Clone the Repository
Clone the project to your local machine or download it as a ZIP file and extract it.

```bash
https://github.com/your-repo-url
cd OnlineClothingStore
```

### 2. Install Dependencies
Install the required Python libraries using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Prepare the Database

1. Navigate to the project directory.
2. Locate the `database.accdb` file in the project folder.
3. Ensure that the `database.accdb` path is correctly configured in `app.py`:

```python
db_handler = DatabaseHandler(db_path='path/to/your/database.accdb')
```

4. The application will initialize the database and create required tables automatically.

### 4. Run the Application
Start the Flask application by running the following command:

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000/`.

### 5. Access the Application

1. Open your browser and navigate to `http://127.0.0.1:5000/`.
2. Use the default admin credentials to log in:
   - **Username**: `admin`
   - **Password**: `admin_password` (defined in `database_handler.py` during `create_admin()`).

---

## File Structure

### Key Directories and Files

- **`app.py`**: Main application entry point.
- **`database_handler.py`**: Manages database operations and initialization.
- **`controllers/`**: Contains Flask Blueprints for various modules (auth, cart, product, user, order).
- **`models/`**: Defines data models for the application.
- **`views/templates/`**: HTML templates for the frontend.
- **`static/`**: Static files such as CSS, images, and videos.

---

## Features

1. **User Authentication**: Login, registration, and session management.
2. **Admin Panel**: Manage products and view orders.
3. **Product Management**: Add, view, and update product details.
4. **Cart Management**: Add/remove items to/from the cart.


---

## Troubleshooting

1. **Database Issues**:
   - Ensure the `database.accdb` file is accessible.
   - Verify the `db_path` in `app.py`.

2. **Missing Dependencies**:
   - Run `pip install -r requirements.txt` to install all required libraries.

3. **Server Not Starting**:
   - Ensure you are in the correct directory.
   - Check if the `Flask` library is installed.

---

## All rights reserved.

