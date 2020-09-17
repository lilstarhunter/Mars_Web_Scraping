import pandas as pd
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import time

def scrape():
    executable_path = {'executable_path': '/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    mars_dict = {}
    
    ##======= Nasa Mars News ========##
    browser.visit("https://mars.nasa.gov/news")
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all("li", class_="slide")
    titles = []
    teasers = []

    for article in articles:
        title = article.find('div', class_="content_title").text
        titles.append(title)
        teaser = article.find('a').text
        teasers.append(teaser)

    mars_dict.update({"titles": titles, "teasers": teasers})

    ##======= JPL Mars Space Images ========##
    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    browser.find_by_id('full_image').first.click()
    pic = browser.links.find_by_partial_text("more info")
    pic.click()

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    img_url = soup.select_one("figure.lede a img").get("src")
    feat_img_url = "https://www.jpl.nasa.gov" + img_url

    mars_dict.update({"feat_img_url": feat_img_url})

    ##======= Mars Facts ========##
    url = 'https://space-facts.com/mars'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Mars Planet Profile', 'Value']
    html_table = df.to_html()
    html_table.replace('\n', '')
    mars_table = df.to_html('table.html')
    mars_dict.update({"mars_table": mars_table})

    ##======= Mars Hemispheres ========##
    main_url = 'https://astrogeology.usgs.gov'
    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemis_url)
    hemis_html = browser.html
    hemis_soup = BeautifulSoup(hemis_html, 'html.parser')

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

        mars_dict.update("image_dict": image_dict)


    return print(mars_dict)

scrape()
    

