from flask import Flask, render_template, redirect
from flask import jsonify
from .scrape_mars import mars_info
from pymongo import MongoClient

app = Flask(__name__)

# Set up mongo connection
MONGO_URI = "mongodb://localhost:27017/"

client = MongoClient(MONGO_URI)

db = client.mars_db


@app.route("/")
def echo():
    return render_template("index.html", text="Mission to Mars")

@app.route("/scrape")
def scrape():
    return jsonify(mars_info())


if __name__ == "__main__":
    app.run(debug=True)
