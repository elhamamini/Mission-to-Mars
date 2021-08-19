from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import  scraping

app=Flask(__name__)

#Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"]="mongodb://localhost:27017/mars_app"
mongo=PyMongo(app)
#The code we create next will set up our Flask routes: 
# one for the main HTML page everyone will view when visiting the web app,
#  and one to actually scrape new data using the code we've written.

#first write  rout for out html page
@app.route("/")
def index():
    #uses PyMongo to find the "mars" collection in our database, 
    # which we will create when we convert our Jupyter scraping code to Python Scrip
    mars=mongo.db.mars.find_one()
    #the line belloq tells flask return html template using an index.html file
    #we will create this file after we build the flask routes
    #and mars=masrs tells python to use the mars collection mongodb
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars=mongo.db.mars    
    mars_data=scraping.scrape_all()
    mars.update({},mars_data,upsert=True)
    return redirect('/',code=302)


if __name__ == "__main__":
   app.run()
