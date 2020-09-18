import pandas as pd
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import time

def mars_info():
    executable_path = {'executable_path': '/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    mars_dict = {}
    
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

    #Append to the Mars Dictionary
    mars_dict.update({"titles": titles, "teasers": teasers})

    ##======= JPL Mars Space Images ========##
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
    feat_img_url = "https://www.jpl.nasa.gov" + img_url

    #Update dictionary with featured image url
    mars_dict.update({"Featured_Image_URL": feat_img_url})

    ##======= Mars Facts ========##
    url = 'https://space-facts.com/mars'
    
    #Convert url tables to pandas dataframe
    tables = pd.read_html(url)
    
    #change column names
    df = tables[0]
    df.columns = ['Mars Planet Profile', 'Value']
    
    #Convert table to html
    html_table = df.to_html()
    html_table.replace('\n', '')
    mars_table = df.to_html('table.html')

    #Update Dictionary
    mars_dict.update({"Mars_Facts_Table": mars_table})
    time.sleep(2)

    ##======= Mars Hemispheres ========##
    main_url = 'https://astrogeology.usgs.gov'
    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #Create Beautiful Soup Object
    browser.visit(hemis_url)
    hemis_html = browser.html
    hemis_soup = BeautifulSoup(hemis_html, 'html.parser')

    #Find hemispheres 
    all_hemis = hemis_soup.find('div', class_='collapsible results')
    mars_hemis = all_hemis.find_all('div', class_='item')

    hemi_img_urls = []

    # Loop through the main hemisphere data page
    for hemi in mars_hemis:
        # Collect Title
        hemisphere = hemi.find('div', class_="description")
        title = hemisphere.h3.text
        
        # Scrape image links on hemisphere page
        hemi_link = hemi.a["href"]    
        browser.visit(main_url + hemi_link)
        
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')
        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        # Create Dictionary to with key: title and value: url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
        
        hemi_img_urls.append(image_dict)

        mars_dict.update({"image_dict": image_dict})

    return mars_dict
    

