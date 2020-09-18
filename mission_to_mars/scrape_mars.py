import pandas as pd
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import time

def mars_info():
    executable_path = {'executable_path': '/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    
    ##======= Nasa Mars News ========##
    browser.visit("https://mars.nasa.gov/news")
    
    #Create a soup object 
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    
    # Find all headlines
    articles = soup.findAll("li", class_="slide")
    titles = []
    teasers = []

    #Loop through headlines to scrape titles and teasers
    for article in articles:
        title = article.find('div', class_="content_title").text
        titles.append(title)
        teaser = article.find('div', class_="article_teaser_body").text
        teasers.append(teaser)


    ##========== JPL Nasa =============##
    ##=================================##
    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    
    #Create a soup object 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Use splinter to click on full image then open more info page
    browser.find_by_id('full_image').first.click()
    pic = browser.links.find_by_partial_text("more info")
    pic.click()

    #Reset soup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Scrape image url
    img_url = soup.select_one("figure.lede a img").get("src")
    feat_image_url = "https://www.jpl.nasa.gov" + img_url


    ##========== Mars Facts ===========##
    ##=================================##
    url = 'https://space-facts.com/mars'
    
    #Convert url tables to pandas dataframe
    table = pd.read_html(url)
    
    #Reset Index to Attribute
    mars_facts = table[1]
    mars_facts.columns = ["Attribute", "Value"]
    mars_facts = mars_facts.set_index("Attribute")
    
    #Convert Mars Profile table to an html table
    mars_facts = mars_facts.to_html(classes="table table-striped")

    time.sleep(5)

    ##======= Mars Hemispheres ========##
    ##=================================##
     # Visit USGS webpage for Mars hemispehere images
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, "html.parser")

    # Create dictionary to store titles & links to images
    hemisphere_image_urls = []

    # Retrieve all elements that contain image information
    results = soup.find("div", class_ = "result-list" )
    hemispheres = results.find_all("div", class_="item")
    
    # Iterate through each image
    for hemisphere in hemispheres:

        #Scrape and clean title
        title = hemisphere.find("h2").text
        title = title.replace("Enhanced", "")

        #Get Image Link
        hemi_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + hemi_link    

        #Go to image link and set BeautifulSoup object
        browser.visit(image_link)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")

        #Find image download and grab href
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]

        #Add ttitle and image url to hemisphere dictionary
        hemisphere_image_urls.append({"title": title, "img_url": image_url})
        
        browser.back()
        
    #=========STORE DATA IN FINAL DICTIONARY=============#

    mars_data = {
        "titles": titles,
        "teasers": teasers,
        "featured_image_url": feat_image_url,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    return mars_data
    

