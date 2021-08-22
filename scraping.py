#!/usr/bin/env python
# coding: utf-8




from splinter import Browser, browser
from bs4 import BeautifulSoup as soup
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title,news_paragraph=mars_news(browser)
    data={
        "news_title":news_title,
        "news_paragraph":news_paragraph,
        "featured_image":featured_image(browser),
        "facts":mars_facts(),
        "hemisphere":hempisphere_image_and_title(browser),
        "last_modified":dt.datetime.now(),

    }
    browser.quit()
    return data

def mars_news(browser):
# Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
# Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html=browser.html
    news_soup=soup(html,'html.parser')
    try:
        slide_elem=news_soup.select_one('div.list_text')
        

    #we are returning the most recent news in the website
        news_title =slide_elem.find('div',class_='content_title').get_text()
        

        news_p=slide_elem.find('div',class_="article_teaser_body").get_text()
    except AttributeError:
        return None,None

    return news_title,news_p
# ### Featured Images

#now we will setup our url

def featured_image(browser):
#if you check the browser you can see we are in a diffrent page after we run this cell
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    full_image_elem=browser.find_by_tag('button')[1]
    full_image_elem.click()

    #since we are in the new page we need to parse the html again
    html=browser.html
    img_soup=soup(html,'html.parser')
    try:
    #now we need to get the img url bc we are in a new page and it has a new source
        img_url_rel=img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    # we did this bc we want to get url like this not getting it manualy bc if the page updated we are still getting the first image

    #get the first part of url from the webpage adress bar
    img_url=url+img_url_rel

    return img_url


#unnecessery line of code
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None   
    df.columns=['Description','Mars','Earth']
    df.set_index("Description", inplace=True)
    # df.drop(labels='Mars - Earth Comparison', axis=0,inplace=True)
    

    #with this line of code now we have the table in our web app
    return df.to_html()

def hempisphere_image_and_title(browser):
    url = 'https://marshemispheres.com/'

    browser.visit(url)
    html=browser.html
    img_soup=soup(html,'html.parser')
    hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
    container_em=img_soup.find('div',class_="collapsible results")

    div_tags=container_em.find_all('div',class_='description')

    # a_tags=div_tags.find_all('a')
    # print(a_tags)
    for d in div_tags:
        hemisphere={}
        next_url=d.find('a').get('href')
    
        browser.visit(url + next_url)
        html=browser.html
        full_img_soup=soup(html,'html.parser')
        
        img_url=full_img_soup.find('img',class_="wide-image").get('src')
    
        title=full_img_soup.find('h2',class_="title").get_text()
        print(title)
        hemisphere['img_url']= url+img_url
        hemisphere['title']=title

        hemisphere_image_urls.append(hemisphere)

    return hemisphere_image_urls

if __name__=="__main__":
    #if running as script, print scraped data
    print(scrape_all())

