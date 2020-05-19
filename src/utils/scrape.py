import os
import pandas as pd
from bs4 import BeautifulSoup as bs4
from splinter import Browser
import requests
import time

nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
twitter_url = 'https://twitter.com/marswxreport?lang=en'
space_facts_url = 'https://space-facts.com/mars/'
mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

mars_data = {}


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape_nasa_news(browser):
    browser.visit(nasa_url)
    time.sleep(2)
    html = browser.html
    soup = bs4(html, 'lxml')
    news_title = soup.find_all('div', class_="content_title")[1].text
    news_p = soup.find('div', class_='article_teaser_body').text
    return (news_title, news_p)


def scrape_featured_image_url(browser):
    browser.visit(jpl_url)
    browser.click_link_by_id('full_image')
    time.sleep(2)
    html = browser.html
    soup = bs4(html, 'lxml')

    feaured_image = soup.find('img', class_='fancybox-image').get('src')
    feaured_image_url = 'https://www.jpl.nasa.gov' + feaured_image

    return feaured_image_url


def scrape_twitter_weather(browser):
    browser.visit(twitter_url)
    time.sleep(2)
    html = browser.html
    soup = bs4(html, 'lxml')
    filepath = os.path.join("html", "twitter_mars.html")

    weathers = soup.find_all(
        'div',
        class_=
        'css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'
    )
    current_weather = weathers[0].find(
        'span',
        class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'
    ).text

    return current_weather


def scrape_space_fact():
    tables = pd.read_html(space_facts_url)
    table_html = tables[0].to_html(header=False, index=False)
    return table_html


def scrape_mars_hemispheres(browser):
    image_urls = list()
    titles = list()
    hemi_full_image_urls = list()

    browser.visit(mars_hemi_url)
    time.sleep(2)
    html = browser.html
    soup = bs4(html, 'lxml')
    filepath = os.path.join("html", "mars_hemi.html")
    links = browser.find_by_css('.description .itemLink')

    for link in links:
        image_urls.append(link['href'])
        titles.append(link.text)

    for index, image_url in enumerate(image_urls):
        browser.visit(image_url)
        time.sleep(1)
        image_link = browser.find_by_css('.downloads ul li a')[0]
        hemi_full_image_urls.append({
            'title': titles[index],
            'img_url': image_link['href']
        })

    return hemi_full_image_urls


def scrape_all():
    browser = init_browser()
    nasa_news = scrape_nasa_news(browser)
    featured_image = scrape_featured_image_url(browser)
    current_weather = scrape_twitter_weather(browser)
    table_html = scrape_space_fact()
    hemi_full_image_urls = scrape_mars_hemispheres(browser)

    mars_data['news_title'] = nasa_news[0]
    mars_data['news_p'] = nasa_news[1]
    mars_data['featured_image'] = featured_image
    mars_data['current_weather'] = current_weather
    mars_data['table_html'] = table_html
    mars_data['hemi_full_image_urls'] = hemi_full_image_urls

    browser.quit()
    print(mars_data)
    return mars_data
