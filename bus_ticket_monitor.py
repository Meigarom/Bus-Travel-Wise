# -*- coding: utf-8 -*-

# libraries
import re
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

# ------------------------
# get all seats available
# ------------------------
seats = soup.find_all( class_='available-seats' ) 

df_seats = list()
for seat in seats:
    df_seats.append( int( re.findall( r'\d+', seat.get_text() )[0] )  )

# ------------------------
# get bus lines information
# ------------------------
buslines = soup.find_all( class_="search-item search-item-direct " )
for busline in buslines:
    data = json.loads( busline['data-content'] )['trips'][0]
    data_dict = { 'departureTime': data['departureTime'], 
                  'company': data['companySlug'], 
                  'arrivalDate': data['arrivalDate'], 
                  'arrivalStation': data['arrivalStation'], 
                  'departureStation': data['departureStation'],
                  'arrivalTime': data['arrivalTime'],
                  'departureDate': data['departureDate'], 
                  'durationTime': data['durationTime'] }
    print( data_dict )


## create dataframe
#df = pd.DataFrame( [ {'departureTime': data['trips'][0]['departureTime'], 
#                     'company': data['trips'][0]['companySlug'], 
#                     'arrivalDate': data['trips'][0]['arrivalDate'], 
#                     'arrivalStation': data['trips'][0]['arrivalStation'], 
#                     'departureStation': data['trips'][0]['departureStation'],
#                     'arrivalTime': data['trips'][0]['arrivalTime'],
#                     'departureDate': data['trips'][0]['departureDate'], 
#                     'durationTime': data['trips'][0]['durationTime'] } ] )
#
#print( df )
#
# Convert to dataframe



#print( len( soup.find_all( class_='available-seats' ) ) )
#print( soup.find_all( class_='available-seats' )[0].get_text() )


#print( soup )
#for tag in soup.find_all( 'title' ):
#    print( tag.text )

# mount the dataset

# save the dataset as a csv file
