# IMPORT LIST

import os
from flask import Flask, render_template, request, redirect, url_for , jsonify
import Cosine_recommender
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import werkzeug.exceptions
from werkzeug.utils import secure_filename, send_from_directory
from werkzeug.datastructures import CombinedMultiDict

app = Flask(__name__, template_folder='Template')

# APP FUNCTIONS

# EXCEPTION HANDLING
@app.errorhandler(400)
def bad_request(error):
    error_header = "Bad Request - Client Error"
    error_message = "Please return to the previous page and try again.\nIf problem persists, please restart the program or contact the creator."
    return render_template('error.html', error_header=error_header, error_message=error_message), 404

@app.errorhandler(404)
def page_not_found(error):
    error_header = "Page Not Found"
    error_message = "The page may have been moved or deleted. Please return to the homepage."
    return render_template('error.html', error_header=error_header, error_message=error_message), 404

@app.errorhandler(500)
def internal_error(error):
    error_header = "Internal Server Error"
    error_message = "Please restart the program and try again.\nIf problem persists, please contact the creator."
    return render_template('error.html', error_header=error_header, error_message=error_message), 500

# GET DATA
df = pd.read_csv('static/csv_files/data.csv')
df.set_index("id", inplace=True)

# SET EMPTY GLOBAL VARIABLES TO SAVE PRODUCT FILTER
menu_filter = None
shop_filter = {}

# RECOMMEND PRODUCTS

def recommend_products(product_id, top_n=5):
    if product_id not in Cosine_recommender.product_vectors:
        return []
    user_vector = Cosine_recommender.product_vectors[product_id].toarray()
    similarities = cosine_similarity(user_vector, Cosine_recommender.tfidf_matrix)[0]

    df_copy = df.copy()
    df_copy["similarity"] = similarities
    df_copy = df_copy.drop(index=product_id)  # remove the current item
    top_matches = df_copy.sort_values(by="similarity", ascending=False).head(top_n)
    print("init\n", top_matches)
    return top_matches.index.tolist()

# FILTER BY MENU
def filter_by_menu(menu_type):
    global menu_filter  # call global variable
    menu_filter = menu_type  # stores menu filter
    data = df[df["subCategory"] == menu_filter]  # filter original data by menu category
    return data

# FILTER BY SHOP
def filter_by_shop(data):
    global shop_filter  # call global variable
    if shop_filter:  # if there is a shop filter saved
        for variable in shop_filter:
            if shop_filter[variable]:  # if list not empty
                data = data[data[variable].isin(shop_filter[variable])]
    return data

def recommend_outfit_completion(main_product_id, top_n=5):
    if main_product_id not in df.index:
        return []

    main_prod = df.loc[main_product_id]

    # Adjusted to match your subCategory values
    complementary_types = {
        'Topwear': ['Bottomwear', 'Dress', 'Loungewear and Nightwear', 'Socks'],
        'Bottomwear': ['Topwear', 'Dress', 'Loungewear and Nightwear', 'Socks'],
        'Dress': ['Topwear', 'Bottomwear', 'Loungewear and Nightwear'],
        'Loungewear and Nightwear': ['Topwear', 'Bottomwear'],
        'Apparel Set': ['Socks', 'Topwear', 'Bottomwear'],
        'Socks': ['Topwear', 'Bottomwear'],
        'Innerwear': [],  # not usually paired for public outfits
        'Saree': ['Socks']  # optional
    }

    main_type = main_prod['subCategory']
    possible_types = complementary_types.get(main_type, [])

    # Filter dataset
    candidates = df[df['subCategory'].isin(possible_types)]

    # Match gender
    candidates = candidates[candidates['gender'] == main_prod['gender']]

    # Match season if available
    if pd.notna(main_prod.get('season')):
        candidates = candidates[candidates['season'] == main_prod['season']]

    # Match usage if available
    if pd.notna(main_prod.get('usage')):
        candidates = candidates[candidates['usage'] == main_prod['usage']]

    # Match baseColour if available
    if pd.notna(main_prod.get('baseColour')):
        candidates = candidates[candidates['baseColour'] == main_prod['baseColour']]

    # Match material if relevant
    if pd.notna(main_prod.get('Material')):
        candidates = candidates[candidates['Material'] == main_prod['Material']]

    # Drop the original product itself
    candidates = candidates.drop(index=main_product_id, errors='ignore')

    # Sort by rating or price
    if 'rating' in candidates.columns and pd.api.types.is_numeric_dtype(candidates['rating']):
        candidates = candidates.sort_values(by='rating', ascending=False)
    else:
        candidates = candidates.sort_values(by='price', ascending=True)

    return candidates.head(top_n).index.tolist()




# ROUTE HOMEPAGE

# Comment out this function after fixing recommender function
# def recommend_products(id):
#     return [39386, 21379, 53759, 1855, 30805]

@app.route("/")
def welcome():
    return render_template("1_Welcome.html")


@app.route("/login")
def login():
    return render_template("3Login_.html")

@app.route("/sign_up")
def sign_up():
    return render_template("2Sign-up_.html")

@app.route("/loginGoogle")
def login_google():
    return render_template("4Signin_google_Page_.html")

@app.route("/selected/<path:user>/")
def selected(user):
    return render_template("5selected.html", selected_user=user)

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/menu")
def menu():
    return render_template("6menu.html")

@app.route("/Input_measurement")
def Input_measurement():
    return render_template("Input_measurement_.html")

@app.route("/based_recommendation_screen")
def based_recommendation_screen():
    recommended = request.args.get("recommended", "")
    gender = request.args.get("gender", "male")
    product_id = request.args.get("id", type=int)  # get product ID as int

    main_prod = None
    if product_id and product_id in df.index:
        main_prod = df.loc[product_id]
    else:
        # Optionally handle missing product (e.g. flash message or error)
        main_prod = None

    return render_template(
        "based_measurement_recommendscreen_.html",
        recommended=recommended,
        gender=gender,
        main_prod=main_prod
    )


@app.route("/Settings_Page")
def Settings_Page():
    return render_template("Settings_Page.html")

@app.route("/Settings_measurements")
def Settings_measurements():
    return render_template("Settings_Measurements.html")

@app.route("/Settings_Cart")
def Settings_Cart():
    return render_template("Settings_Cart.html")

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/searchFilter")
def search_filter():
    global menu_filter
    return render_template("searchFilter.html", menu_type=menu_filter)

@app.route("/shop/<menu_type>/", methods=["GET", "POST"])
def shop(menu_type):
    data = filter_by_menu(menu_type)  # 1st filter

    rating_filter = []  # ✅ define this early so it's always available

    if request.method == "POST":
        # Extract filters from form
        gender = request.form.getlist("gender")
        article_type = request.form.getlist("subCategory")
        base_colour = request.form.getlist("baseColour")
        made_in = request.form.getlist("Made In")
        min_price = request.form.get("min_price", "0")
        max_price = request.form.get("max_price", "999999")
        rating_filter = request.form.getlist("rating")  # still works here
        material = request.form.getlist("Material")

        # Save shop filter globally (rating excluded intentionally)
        global shop_filter
        shop_filter = {
            "gender": gender,
            "subCategory": article_type,
            "baseColour": base_colour,
            "Made In": made_in,
            "Material": material
        }

        # Filter price range
        try:
            df["price"] = df["price"].astype(float)
            data = data[(df["price"] >= float(min_price)) & (df["price"] <= float(max_price))]
        except:
            pass

    # Apply non-rating filters
    data = filter_by_shop(data)

    # ✅ Apply rating filter here if any selected
    if rating_filter:
        try:
            rating_filter = list(map(int, rating_filter))
            data = data[data["rating"].astype(int).isin(rating_filter)]
        except:
            pass

    # Limit to 100 items
    # Get 'limit' from query parameters, default to 100
    limit = int(request.args.get("limit", 100))
    data = data.head(limit)

    return render_template("shop.html", data=data, n=len(data), limit=limit, menu_filter=menu_filter)


@app.route("/outfit_recommendation/<int:id>/", methods=["GET"])
def outfit_recommendation(id):
    global menu_filter
    if id not in df.index:
        return render_template("error.html", error_header="Product Not Found", error_message="The product ID doesn't exist.")

    main_prod = df.loc[id].copy()
    main_prod['id'] = id  # ensure ID is included

    rec_ids = recommend_outfit_completion(id)
    
    rec_df = df.loc[rec_ids].copy()
    rec_df["id"] = rec_df.index  # Fix: include ID in each record
    recommendations = rec_df.to_dict(orient='records')

    return render_template(
        "outfit_recommendation.html",
        main_prod=main_prod,
        recommendations=recommendations,
        menu_type=menu_filter
    )







# #Searchbar(?)
# @app.route('/search')
# def search():
#     query = request.args.get('q', '').lower()
#     # Filter from your dataset
#     results = df[df['productDisplayName'].str.lower().str.contains(query, na=False)]

#     # Convert to list of dicts
#     return jsonify(results.to_dict(orient='records'))

@app.route("/viewProduct/<int:id>/", methods=["GET"])
def view_product(id):
    global menu_filter
    main_prod = df.loc[id]  # get data of selected product
    main_prod['id'] = id
    rec_ids = recommend_products(id)  # get id of recommended products
    n = len(rec_ids)  # get total no. of recommended products
    rec_prods = df[df.index.isin(rec_ids)]  # subset data
    return render_template("viewProduct.html", main_prod=main_prod, rec_prods=rec_prods, n=n, menu_type=menu_filter)


if __name__ == '__main__':
    app.run()

