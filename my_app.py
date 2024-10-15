from flask import Flask, render_template, request, redirect , flash
from pymongo import MongoClient
import re
import os
from dotenv import load_dotenv
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
mongo_database = os.getenv("MONGO_DATABASE")
mongo_collection = os.getenv("MONGO_COLLECTION")

app = Flask(__name__)

client = MongoClient(mongo_uri)
db = client[mongo_database]
collection = db[mongo_collection]

app.secret_key = 'jachaninat'


@app.route('/')
def form():
    product_data = [{'product': '', 'unit': 1, 'price': 0.0}]
    return render_template('form.html',errors={},product_data=product_data)

@app.route('/submit', methods=['POST'])
def submit_data():
    customername = request.form['customername']
    phone_number = request.form['phone_number']
    sale_date =request.form['sale_date']

    product_data = []

    errors = {}
    
    products = request.form.getlist('product')
    quantities = request.form.getlist('quantity')
    prices = request.form.getlist('price')
    
    for product, quantity, price in zip(products, quantities, prices):
        product_errors = {}
        
        if not product:
            product_errors['product'] = 'Please select a product.'
        
        if not quantity.isdigit() or int(quantity) <= 0:
            product_errors['quantity'] = 'Quantity must be a positive integer.'
        
        if not re.match(r'^\d+(\.\d{1,2})?$', price):
            product_errors['price'] = 'Price must be a positive number with up to two decimal places.'
        
        if product_errors:
            errors.update(product_errors)
        else:
            product_data.append({
                'product': product,
                'unit': int(quantity),
                'price': float(price)
            })
    if not customername:
        errors['name'] = 'Please enter your name.'
    
    if not sale_date:
        errors['sale_date'] = 'Please enter sale_date'

    if not product:
        errors['product'] = 'Please enter a product.'

    if not phone_number:
        errors['phone_number'] = 'Please enter your phone number.'
    elif not re.fullmatch(r'\d{10}', phone_number):
        errors['phone_number'] = 'Phone number must be exactly 10 digits.'

    if not quantity:
        errors['quantity'] = 'Please enter a quantity.'
    elif not quantity.isdigit() or int(quantity) <= 0:
        errors['quantity'] = 'Quantity must be a positive integer.'

    if not price:
        errors['price'] = 'Please enter a price.'
    elif not re.match(r'^\d+(\.\d{1,2})?$', price):
        errors['price'] = 'Price must be a positive number with up to two decimal places.'
    
    if errors:
        return render_template('form.html', 
                               sale_date = sale_date,
                               customername=customername, 
                               phone_number=phone_number, 
                               product_data=product_data,
                               errors = errors
                               )




    user_data = {'sale_date': sale_date ,'customername': customername,'phone_number':phone_number,'product':product_data}
    
    collection.insert_one(user_data)
    
    return redirect('/success')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
