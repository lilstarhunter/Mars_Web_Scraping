from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

#Import app.py scrape_mars
import scrape_mars

#Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)


@app.route("/")
def index():
    #Store the mars_dictionary in a list
    mars_data = mongo.db.mars.find_one()
    
    #Render the index.html template 
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():
    #Create a Link to mongodb dict
    mars_data = mongo.db.mars

    #Run script
    mars_data = scrape_mars.mars_info()
    
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
