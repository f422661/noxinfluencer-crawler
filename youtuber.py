from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import webdriver_manager
import numpy as np
import selenium
import requests
import pandas as pd
import re
import time
import json


headers = { 
    # 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}


url_list = list()


## ignore warning
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(chrome_options=options,executable_path=ChromeDriverManager().install(),)

# driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get('https://tw.noxinfluencer.com/youtube-channel-rank/top-1000-tw-all-youtuber-sorted-by-views-monthly')


# scroll the web page
for x in range(1, 25):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)

time.sleep(5)

## get the link for first level page
for index, item in enumerate(driver.find_elements_by_class_name('star-avatar')):
    if index == 0:
        continue
    url_list.append(item.get_attribute('href'))

print("# of url:",len(url_list))

data = list()
for index, url in enumerate(url_list):


    print(str(index+1)+".","crawling url:",url)
    driver.get(url)
    # driver.find_element_by_xpath("//span[@switch-tab='29']").click()


    time.sleep(3)

    ## get youtuber id encoding
    id_encoding = url.split("/")[-1]

    ## get # of youtuber viewers in a year
    r = requests.get("https://tw.noxinfluencer.com/ws/star/trend/"+id_encoding+"?type=increase&dimension=view&interval=daily")
    j = json.loads(r.text)
    view_cnt_list = j["retData"]["history"]

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    title = soup.findAll("div",{"class": "title"})[0].span.text
    category = soup.findAll("a",{"class": "tag"})[0].text
    open_title = soup.findAll("p",{"class": "pull-right item-value"})[0].text
    location = soup.findAll("p",{"class": "pull-right item-value"})[1].span.text.strip()
    introduction = soup.findAll("div",{"class": "text"})[0].text

    fans_cnt = soup.findAll("div",{"class": "value-content"})[0].span.text
    view_cnt = soup.findAll("div",{"class": "value-content"})[1].span.text
    view_cnt_avg = soup.findAll("div",{"class": "value-content"})[2].span.text
    film_cnt = soup.findAll("div",{"class": "value-content"})[3].span.text
    income = soup.findAll("div",{"class": "est-content"})[1].text.strip()

    data.append([index+1,title, category, open_title, location, introduction, fans_cnt, view_cnt, view_cnt_avg, film_cnt,income, view_cnt_list])


driver.close()

df = pd.DataFrame(data,columns = ["rank","title","category","open_title","location","introduction","fans_cnt","view_cnt","view_cnt_avg","film_cnt","income","view_cnt_log"])

df.to_csv("influencer.csv", index = False)



