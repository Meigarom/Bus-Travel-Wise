# -*- coding: utf-8 -*-

# libraries
import json
import time
import requests
import pandas                       as pd
from selenium import webdriver
from bs4      import BeautifulSoup 

## Chrome driver
#driver = webdriver.Chrome( executable_path='/Users/meigarom/chromedriver' )

# parameters
root = 'https://www.clickbus.com.br/'
vehicle = 'onibus'
origin = 'sao-paulo-sp-todos'
destination = 'mogi-guacu-sp'
date = '2018-12-25'

# website address
web_address = root+vehicle+'/'+origin +'/'+destination+'?departureDate='+date 

print( web_address )

# access the link
#driver.get( web_address )
#
## ----------------------------
## get to buy bus ticket
## ----------------------------
#time.sleep( 3 )
#btn = driver.find_element_by_xpath( '//*[@id="search-results"]/div[2]/div/div[1]/div[1]/div[7]/button[1]' )
#btn.click()
#
#time.sleep( 2 )

response = requests.get( web_address )
page = response.text
soup = BeautifulSoup( page,"lxml" )

#print( soup.prettify() )

buslines = soup.find_all( class_="search-item search-item-direct " )
data = buslines[0]['data-content']

print( buslines[0]['data-content'] ) 
print( type( buslines[0]['data-content'] ) )

# Convert to dataframe
df = pd.DataFrame.from_dict( json.loads( data ) )

# available seats
#seats = buslines[0].find( class_='available-seats' ).get_text()

# 


## seats available
#seats = soup.find_all( class_='available-seats' ) 
#for seat in seats:
#    print( seat.get_text() )


#print( len( soup.find_all( class_='available-seats' ) ) )
#print( soup.find_all( class_='available-seats' )[0].get_text() )

#table = driver.find_element_by_xpath( '//*[@id="search-item-details"]/div[2]/div[2]/ul' )
#table = driver.find_element_by_class_name( 'bus-seats' )

#seat = driver.find_element_by_xpath( '//*[@id="search-item-details"]/div[2]/div[2]/ul/li[6]/span' )

#print( seat.text )

## count how many places are available
#html = driver.page_source
#soup = bso( web_address )
#print( soup )
#for tag in soup.find_all( 'title' ):
#    print( tag.text )

# mount the dataset

# save the dataset as a csv file
