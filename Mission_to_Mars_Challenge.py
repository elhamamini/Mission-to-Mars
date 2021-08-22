#!/usr/bin/env python
# coding: utf-8



from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd




executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)




# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)




html=browser.html
news_soup=soup(html,'html.parser')
slide_elem=news_soup.select_one('div.list_text')
slide_elem




#we are returning the most recent news in the website
news_title =slide_elem.find('div',class_='content_title').get_text()
news_title 


# news_p=slide_elem.find('div',class_="article_teaser_body").get_text()
# news_p

# ### Featured Images


#now we will setup our url
url = 'https://spaceimages-mars.com'
browser.visit(url)




#if you check the browser you can see we are in a diffrent page after we run this cell
full_image_elem=browser.find_by_tag('button')[1]
print(full_image_elem)
full_image_elem.click()




#since we are in the new page we need to parse the html again
html=browser.html
img_soup=soup(html,'html.parser')




#now we need to get the img url bc we are in a new page and it has a new source
img_url_rel=img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel
# we did this bc we want to get url like this not getting it manualy bc if the page updated we are still getting the first image





#get the first part of url from the webpage adress bar
img_url=f'https://spaceimages-mars.com/{img_url_rel}'
img_url





#unnecessery line of code
url = 'https://galaxyfacts-mars.com/'
browser.visit(url)





#zero index means we just need a first table
# first we need to extract a data then return it to html again we use read_html bc its much easier than scrapping each row of the table
df=pd.read_html(url)[0]
df.columns=['Description','Mars','Earth']
df.set_index("Description", inplace=True)
# df.drop(labels='Mars - Earth Comparison', axis=0,inplace=True)
df





#with this line of code now we have the table in our web app
df.to_html()








# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# 




url = 'https://marshemispheres.com/'

browser.visit(url)

html=browser.html
img_soup=soup(html,'html.parser')


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
container_em=img_soup.find('div',class_="collapsible results")

div_tags=container_em.find_all('div',class_='description')

# a_tags=div_tags.find_all('a')
# print(a_tags)
for d in div_tags:
    hemisphere={}
    next_url=d.find('a').get('href')
    print(next_url)
    
    browser.visit(url + next_url)
    html=browser.html
    full_img_soup=soup(html,'html.parser')
    
    img_url=full_img_soup.find('img',class_="wide-image").get('src')
   
    title=full_img_soup.find('h2',class_="title").get_text()
    print(title)
    hemisphere['img_url']=img_url
    hemisphere['title']=title
    hemisphere_image_urls.append(hemisphere)
    
    
print(hemisphere_image_urls)    








browser.quit()

