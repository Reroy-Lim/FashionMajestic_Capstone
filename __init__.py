# IMPORT LIST

import os
from flask import Flask, render_template, request, redirect, url_for
import Cosine_recommender
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import werkzeug.exceptions
from werkzeug.utils import secure_filename, send_from_directory
from werkzeug.datastructures import CombinedMultiDict

app = Flask(__name__)

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

# ROUTE HOMEPAGE

# Comment out this function after fixing recommender function
# def recommend_products(id):
#     return [39386, 21379, 53759, 1855, 30805]

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/loginWebsite")
def login_website():
    return render_template("signup.html")

@app.route("/loginGoogle", methods=["GET"])
def login_google():
    return render_template("loginGoogle.html")

@app.route("/selected/<user>/")
def selected(user):
    return render_template("selected.html", selected_user=user)

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/shop/<menu_type>/", methods=["GET", "POST"])
def shop(menu_type):

    data = filter_by_menu(menu_type)  # 1st filter

    if request.method == "POST":  # if search filter form is posted, get input and save shop filter
        # get inputs from filter (form)
        article_type = list(map(lambda y: y[1], filter(lambda x: "articleType" in x[0], request.form.items())))
        base_colour = list(map(lambda y: y[1], filter(lambda x: "baseColour" in x[0], request.form.items())))
        made_in = list(map(lambda y: y[1], filter(lambda x: "madeIn" in x[0], request.form.items())))

        # TO-DO
        article_type_detailed = []

        # save shop filter
        global shop_filter
        shop_filter = {
            "articleType": article_type_detailed,
            "baseColour": base_colour,
            "Made In": made_in
        }

    data = filter_by_shop(data)  # 2nd filter

    # subset filtered data
    n = 15
    data = data.head(n)
    return render_template("shop.html", data=data, n=n)


@app.route("/searchFilter")
def search_filter():
    global menu_filter
    return render_template("searchFilter.html", menu_type=menu_filter)

@app.route("/viewProduct/<int:id>/", methods=["GET"])
def view_product(id):
    global menu_filter
    main_prod = df.loc[id]  # get data of selected product
    rec_ids = recommend_products(id)  # get id of recommended products
    n = len(rec_ids)  # get total no. of recommended products
    rec_prods = df[df.index.isin(rec_ids)]  # subset data
    return render_template("viewProduct.html", main_prod=main_prod, rec_prods=rec_prods, n=n, menu_type=menu_filter)


if __name__ == '__main__':
    app.run()

