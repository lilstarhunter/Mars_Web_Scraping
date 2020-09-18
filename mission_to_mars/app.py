from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

#Import app.py scrape_mars
import scrape_mars

#Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    #Store the mars_dictionary in a list
    mars_info = mongo.db.mars_db.find_one()
    
    #Render the index.html template 
    return render_template("index.html", mars=mars_info)

@app.route("/scrape")
def scrape():
    #Create a Link to mongodb dict
    mars_dict = mongo.db.mars_dict

    #Run the scrape_mars.py and store as variable
    mars_data = scrape_mars.mars_info()
    
    # Update the Mongo database using update and upsert=True
    mars_dict.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
