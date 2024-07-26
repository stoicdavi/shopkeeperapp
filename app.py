import mysql.connector
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder where images will be stored
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit image size to 16 MB

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# MySQL connection
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Your password',
    database='shopkeeper'
)

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/view')
def view_product():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    return render_template('view_product.html', products=products)

@app.route('/add')
def add_product():
    return render_template('add_product.html')

@app.route('/add_product', methods=['POST'])
def add_product_post():
    product_name = request.form['product_name']
    product_price = request.form['product_price']
    product_quantity = request.form['product_quantity']
    product_description = request.form['product_description']
    product_image = request.files['product_image']

    if product_image:
        image_filename = os.path.join(app.config['UPLOAD_FOLDER'], product_image.filename)
        product_image.save(image_filename)
        image_path = image_filename  # Save the path or filename in the database

        cursor = mydb.cursor()
        cursor.execute(
            "INSERT INTO products (name, price, quantity, description, image_path) VALUES (%s, %s, %s, %s, %s)",
            (product_name, product_price, product_quantity, product_description, image_path)
        )
        mydb.commit()
        cursor.close()

    return redirect(url_for('view_product'))

if __name__ == '__main__':
    app.run(port=2002, debug=True)
