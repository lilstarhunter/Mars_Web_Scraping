from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017"
mongo = PyMongo(app)

db = client.mars_db

mars_db.insert_one(mars_dict)

@app.route("/")
def index():
    info = mongo.db.listings.find_one()
    return render_template("index.html", listings=listings)


@app.route("/scrape")

if __name__ == "__main__":
    app.run(debug=True)
