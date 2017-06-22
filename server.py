from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, request, flash, redirect
import requests


app = Flask(__name__)

# Required to use Flask sessions
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")



@app.route('/search')
def search():
    """Search."""

    # get form inputs:
    destCity = request.args.get('destCity')
    length = int(request.args.get('length'))
    minStarRate = request.args.get('minStarRate')
    maxStarRate = request.args.get('maxStarRate')
    minGuestRate = request.args.get('minGuestRate')
    maxGuestRate = request.args.get('maxGuestRate')

    # Search API:
    search_url = "http://offersvc.expedia.com/offers/v2/getOffers?scenario=deal-finder&page=foo&uid=foo&productType=Hotel&destinationCity={}&lengthOfStay={}".format(destCity, length)
    try:
        r = requests.get(search_url)
    except:
        flash("Search isn't available now!!!")
        return redirect('/')

    print search_url
    print r.json()
    # # 3. Display search results
    # return render_template("search_results.html", customer=customer)
    return render_template('search_results.html')

# @app.route('/add-customer')
# def add_customer():
#     """Display Add Customer Form"""
    
#     return render_template("add_customer.html")

# @app.route('/process_adding_customer')
# def add_customer_to_db():
#     """Add customer to DB."""
#     f_name = request.args.get('fname')
#     l_name = request.args.get('lname')
#     zip_code = request.args.get('zipcode')

#     # To add this customer to db:
#     # 1. Create the customer
#     customer = Customer(fname=f_name, lname=l_name, zipcode=zip_code)

#     # 2. Add this customer to session
#     db.session.add(customer)

#     # 3. Commit the changes
#     db.session.commit()

#     # 4. Display a flash message to confirm adding
#     flash("Customer was addded successfully!!!")

#     return redirect("/")


# @app.route('/all_customers.json')
# def get_all_customers_view():
#     """Return all customers in json object"""

#     all_customers = get_all_customers()
#     customers_list = []
#     for customer in all_customers:
#         customer_dict = {'fname':customer.fname , 'lname':customer.lname}
#         customers_list.append(customer_dict)
#     return jsonify(customers_list)

if __name__ == "__main__":
    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    app.run(port=5001, host='0.0.0.0')