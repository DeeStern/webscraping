from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests

#Set up the chromedriver path
def init_browser():
        executable_path = {'executable_path': 'C:\chromedrv\chromedriver.exe'}
        return Browser('chrome', **executable_path, headless=False)
        

def scrape():
        browser = init_browser()

#JPL Scraping (1)
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)

        time.sleep(1)

        html = browser.html
        soup = bs(html, 'html.parser')

        button = soup.find('footer', class_='button fancybox')
        browser.click_link_by_partial_text('FULL IMAGE')

        locate = soup.find(class_='carousel_item')['style']
        new_url = locate.split("'")[1]
        featured_image_url = 'https://www.jpl.nasa.gov' + new_url

        print(featured_image_url) #This needs to be appended to a dictionary

        #News Scraping (2)
        url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
        response = requests.get(url)

        soup = bs(response.text, 'lxml')

        news_title = soup.find(class_='content_title').text
        print(news_title)

        # Retrieve the paragraph text
        news_p = soup.find(class_='rollover_description_inner').text
        print(news_p)

        #Twitter Scraping (3)
        twitter_url = "https://twitter.com/marswxreport?lang=en"
        browser.visit(twitter_url)

        time.sleep(1)

        html = browser.html
        soup = bs(html, "html.parser")

        mars_weather = soup.find(class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

        print(mars_weather)
        #Space Facts Scraping (4)

        facts_url = 'https://space-facts.com/mars/'
        browser.visit(facts_url)

        time.sleep(1)

        tables = pd.read_html(facts_url)

        #Create scraped table into dataframe
        df = tables[0]
        df.columns = ['Feature', 'Description']

        html_table = df.to_html()
        html_table

        print(html_table)

        #USGS Image Scraping (5)
        url_usgs = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url_usgs)

        time.sleep(1)

        usgs_links = soup.find('a', class_='item')
        browser.click_link_by_partial_text('Cerberus')


        html = browser.html
        soup = bs(html, 'html.parser')

        links_with_text_1 = []
        for a in soup.find_all('a', href=True):
                if a.text:
                        links_with_text_1.append(a['href'])

        Cerberus = links_with_text_1[4]                                       

        print(Cerberus)
        browser.execute_script("window.history.go(-1)")


        usgs_links = soup.find('a', class_='item')
        browser.click_link_by_partial_text('Schiaparelli')

        html = browser.html
        soup = bs(html, 'html.parser')

        links_with_text_2 = []
        for a in soup.find_all('a', href=True):
                if a.text:
                        links_with_text_2.append(a['href'])

        Schiaparelli = links_with_text_2[4]
        print(Schiaparelli)

        browser.execute_script("window.history.go(-1)")

        usgs_links = soup.find('a', class_='item')
        browser.click_link_by_partial_text('Syrtis')

        html = browser.html
        soup = bs(html, 'html.parser')

        links_with_text_3 = []
        for a in soup.find_all('a', href=True):
                if a.text:
                        links_with_text_3.append(a['href'])

        Syrtis = (links_with_text_3[4])  
        print(Syrtis)                     

        browser.execute_script("window.history.go(-1)")

        usgs_links = soup.find('a', class_='item')
        browser.click_link_by_partial_text('Valles')

        html = browser.html
        soup = bs(html, 'html.parser')

        links_with_text_4 = []
        for a in soup.find_all('a', href=True):
                if a.text:
                        links_with_text_4.append(a['href'])

        Valles = links_with_text_4[4]                     
        print(Valles)

        browser.execute_script("window.history.go(-1)")

        # Store data in a dictionary
        mars_data = {
        "JPL_featured_img": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": html_table,
        "Cerberus": Cerberus,
        "Schiaparelli": Schiaparelli,
        "Syrtis": Syrtis,
        "Valles": Valles,
        "News_Title": news_title,
        "News_p": news_p,
        }

        # Close the browser after scraping
        browser.quit()

        return mars_data

if __name__ == '__main__':
    scrape()