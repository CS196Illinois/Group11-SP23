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
    print(zipCode)
    return render_template("results.html", zipCode=zipCode)

if __name__ == '__main__':
    app.run()
