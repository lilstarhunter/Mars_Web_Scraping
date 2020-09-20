import pandas as pd
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import time
# from IPython.display import HTML


def mars_info():
    executable_path = {'executable_path': '/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    ##======= Nasa Mars News ========##
    browser.visit("https://mars.nasa.gov/news")

    # Create a soup object
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    # Find all headlines
    articles = soup.findAll("li", class_="slide")
    titles = []
    teasers = []

    # Loop through headlines to scrape titles and teasers
    for article in articles:
        title = article.find('div', class_="content_title").text
        titles.append(title)
        teaser = article.find('div', class_="article_teaser_body").text
        teasers.append(teaser)

    ##========== JPL Nasa =============##
    ##=================================##
    browser.visit(
        "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")

    # Create a soup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Use splinter to click on full image then open more info page
    browser.find_by_id('full_image').first.click()
    pic = browser.links.find_by_partial_text("more info")
    pic.click()

    # Reset soup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Scrape image url
    img_url = soup.select_one("figure.lede a img").get("src")
    feat_image_url = "https://www.jpl.nasa.gov" + img_url

    browser.back()

    ##========== Mars Facts ===========##
    ##=================================##
    url = 'https://space-facts.com/mars'

    # Convert url tables to pandas dataframe
    table = pd.read_html(url)

    # Reset Index to Attribute
    # Reset Index to Attribute
    mars_facts = table[0]
    mars_facts.columns = ["Attribute", "Value"]
    mars_facts = mars_facts.to_html(index=False, index_names=False)

    # Remove Index for HTML & Convert Mars Profile table to an html table
    # mars_facts = HTML(mars_facts.to_html(index=False))
    time.sleep(5)

    ##======= Mars Hemispheres ========##
    ##=================================##
    # Visit USGS webpage for Mars hemispehere images
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    time.sleep(5)

    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, "html.parser")
    # Create dictionary to store titles & links to images
    hemisphere_image_urls = []

    # Identifies the number of links (hemispheres)
    hemisphere_links = browser.find_by_css("a.product-item h3")
    for i in range(len(hemisphere_links)):

        # Good for when navigato
        browser.find_by_css("a.product-item h3")[i].click()

        # Reset soup object
        html = browser.html
        soup = BeautifulSoup(html, 'lxml')

        # Grab Hemisphere title, clean, save
        title = soup.select_one("h2.title").text
        title = title.replace("Enhanced", "")

        # Grab img url
        img_url = soup.select_one("div.downloads a")["href"]

        # Add hemisphere title and image url to hemisphere dictionary
        hemisphere_image_urls.append({"title": title, "img_url": img_url})

        # return to original landing page
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
