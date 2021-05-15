# importing libraries


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import json


#Configuring driver in selenium

path=r'C:\Users\win10\Documents\Untitled Folder 1\chromedriver.exe' #chromedriver path may differ from system to system
options = Options()
options.headless = True
driver = webdriver.Chrome(path,options=options)

#getting all districts link

driver.get('https://www.medicineindia.org/pharmacies-chemists-drugstores-in-india')
elems = driver.find_elements_by_css_selector('#main > div.row > div > a')
links = [elem.get_attribute('href') for elem in elems]


#getting data of individual district sequentially and making dict of arrays of medicalshops mapped to a district

data={}
for link in links:
    dname = link.split('/')[-1]
    driver.get(link)
    table = driver.find_element_by_xpath('//*[@id="main"]/div[2]/table/tbody[2]')
    rows = table.find_elements_by_css_selector('tr')
    arr = []
    storelink=[]
    for row in rows:
        storelink.append(row.find_element_by_css_selector('td:nth-of-type(1) > a').get_attribute('href'))
    if len(storelink)>0:
        for store in storelink:
            d={}
            driver.get(store)
            d['Medical Store Name']=driver.find_element_by_xpath('//*[@id="main"]/div[2]/dl/dd[1]').text
            d['Address']=driver.find_element_by_xpath('//*[@id="main"]/div[2]/dl/div/dd[1]').text
            d['Pin']=driver.find_element_by_xpath('//*[@id="main"]/div[2]/dl/div/dd[3]/a').text
            d['Phone Number']=driver.find_element_by_xpath('//*[@id="main"]/div[2]/dl/dd[2]').text
            arr.append(d)
    if(len(arr)>0):
        data[dname]=arr
    #break -- addded for testing purspose only
    


# saving as json


json_object = json.dumps(data, indent = 4)  
with open("sample.json", "w") as outfile:
    outfile.write(json_object)





