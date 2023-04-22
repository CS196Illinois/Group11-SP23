from flask import Flask, render_template, request
import pandas as pd
import json


app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("index.html")

@app.route('/results', methods=['GET', 'POST'])
def getZipInfo():
    zip = request.form.get('search')
    print("Testing getZipInfo")
    return render_template("results.html")

if __name__ == '__main__':
    app.run()
