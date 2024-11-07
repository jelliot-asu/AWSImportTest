from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Create all tables
with app.app_context():
    db.create_all()

# route 1 (page 1) #homepage (dynamic)
@app.route('/')
def home():
    return render_template('home.html', page_title='Home')

# route 2 (page 2) #about (dynamic)
@app.route('/about')
def about():
    return render_template('about.html', page_title='About Us')

# route 3 (page 3) #contact (dynamic)
@app.route('/contact')
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
    return render_template('contact.html', page_title='Contact Us')

# route 4 (page 4) #add-product
@app.route('/add-product/<string:product_name>/<float:price>', methods=['GET'])
def add_product(product_name, price):
    new_product = Product(product_name=product_name, price=price)
    db.session.add(new_product)
    db.session.commit()
    return f"Added {product_name} priced at {price} to the database!"

# route 5 (page 5) #products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [{"product_name": product.product_name, "price": product.price} for product in products]
    return {"products": product_list}

if __name__ == "__main__": 
    app.run(debug=True)