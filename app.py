from Research.mkatt9.ML_withLatLon import find_best_restaurant_type
from flask import Flask, render_template, request
import pandas as pd
import json


app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("index.html")

@app.route('/results', methods=['POST'])
def getZipInfo():
    data = request.form
    print(data)
    zipCode = data['searchInput']
    bestType = find_best_restaurant_type(int(zipCode))
    return render_template("results.html", zipCode=zipCode, bestType = bestType[0])

if __name__ == '__main__':
    app.run()
