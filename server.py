from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect
import requests
import os
try:
    from urllib import unquote  # Python 2.X
except ImportError:
    from urllib.parse import unquote  # Python 3+


app = Flask(__name__)

# Required to use Flask sessions
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "abcdef")

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    # RENDER THE MAIN TEMPLATE
    return render_template("homepage.html")


@app.route('/search')
def search():
    """Search."""

    # GET FORM INPUT VALUES:
    destCity = request.args.get('destCity')
    length = int(request.args.get('length'))
    minStarRate = float(request.args.get('minStarRate'))
    maxStarRate = float(request.args.get('maxStarRate'))
    minGuestRate = float(request.args.get('minGuestRate'))
    maxGuestRate = float(request.args.get('maxGuestRate'))

    # TRY TO SEARCH THE API:
    search_url = "http://offersvc.expedia.com/offers/v2/getOffers?scenario=deal-finder&page=foo&uid=foo&productType=Hotel&destinationCity={}&lengthOfStay={}".format(destCity, length)
    try:
        r = requests.get(search_url)
    except: #DISPLAY A FLASH MESSAGE IF REQUEST IS NOT POSSIBLE
        flash("Search isn't available now!!!")
        return redirect('/') # REDIRECT TO THE HOMEPAGE

    # DISPLAY SEARCH RESULTS:
    hotels_list = [] # THIS WILL HOLD THE HOTELS GET FROM THE RESPONCE
    data = r.json() # GET DATA FROM RESPONSE IN JSON FORMAT 
    
    # CREATE FILTER OUT THE RESULTS AND ADD THEM TO HOLTELS LIST ARRAY
    for hotel in data['offers']['Hotel']:
        hotel_name = hotel['hotelInfo']['hotelName']
        price = float(hotel['hotelPricingInfo']['totalPriceValue'])
        star_rate = float(hotel['hotelInfo']['hotelStarRating'])
        guest_rate = float(hotel['hotelInfo']['hotelGuestReviewRating'])
        if ((star_rate>=minStarRate) & (star_rate<=maxStarRate) & (guest_rate>=minGuestRate) & (guest_rate<=maxGuestRate)) :
            # CONSTRUCT HOTEL URL AND DECODE IT IN ORDER TO BE DIPLAYED IN RESULTS PAGE
            hotel_url = unquote(hotel['hotelUrls']['hotelInfositeUrl']).encode().decode('utf8')
            hotels_list.append({'hotel_name':hotel_name, 'price':price, 'star_rate':star_rate, 'guest_rate':guest_rate, 'hotel_url':hotel_url})

    # DISPLAY THE RESULTS IN A TEMPLATE
    return render_template('search_results.html', hotels_list=hotels_list)

if __name__ == "__main__":
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    DEBUG = "NO_DEBUG" not in os.environ

    PORT = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)