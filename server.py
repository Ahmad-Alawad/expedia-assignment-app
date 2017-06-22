from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect
import requests
import os


app = Flask(__name__)

# Required to use Flask sessions
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "abcdef")

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/search')
def search():
    """Search."""

    # Get form inputs:
    destCity = request.args.get('destCity')
    length = int(request.args.get('length'))
    minStarRate = float(request.args.get('minStarRate'))
    maxStarRate = float(request.args.get('maxStarRate'))
    minGuestRate = float(request.args.get('minGuestRate'))
    maxGuestRate = float(request.args.get('maxGuestRate'))

    # Search API:
    search_url = "http://offersvc.expedia.com/offers/v2/getOffers?scenario=deal-finder&page=foo&uid=foo&productType=Hotel&destinationCity={}&lengthOfStay={}".format(destCity, length)
    try:
        r = requests.get(search_url)
    except:
        flash("Search isn't available now!!!")
        return redirect('/')

    # Display search results
    hotels_list = []
    data = r.json()
    for hotel in data['offers']['Hotel']:
        hotel_name = hotel['hotelInfo']['hotelName']
        price = float(hotel['hotelPricingInfo']['totalPriceValue'])
        star_rate = float(hotel['hotelInfo']['hotelStarRating'])
        guest_rate = float(hotel['hotelInfo']['hotelGuestReviewRating'])
        if ((star_rate>=minStarRate) & (star_rate>=maxStarRate) & (guest_rate>=minGuestRate) & (guest_rate>=maxGuestRate)) :
            hotels_list.append({'hotel_name':hotel_name, 'price':price, 'star_rate':star_rate, 'guest_rate':guest_rate})

    return render_template('search_results.html', hotels_list=hotels_list)

if __name__ == "__main__":
    app.debug = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    DEBUG = "NO_DEBUG" not in os.environ

    PORT = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)