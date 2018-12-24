# -*- coding: utf-8 -*-

# libraries
from bs4            import BeautifulSoup 
from datetime       import datetime

import re
import json
import pandas        as pd
import requests     

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
response = requests.get( web_address )
page = response.text
soup = BeautifulSoup( page,"lxml" )

# -------------------------------------------
# get bus lines information & seats available
# -------------------------------------------
seats = soup.find_all( class_='available-seats' ) 
buslines = soup.find_all( class_="search-item search-item-direct " )
data_list = list()
for busline, seat in zip( buslines, seats ):
    data = json.loads( busline['data-content'] )['trips'][0]
    data_dict = { 'departureTime': data['departureTime'], 
                  'company': data['companySlug'], 
                  'arrivalDate': data['arrivalDate'], 
                  'arrivalStation': data['arrivalStation'], 
                  'departureStation': data['departureStation'],
                  'arrivalTime': data['arrivalTime'],
                  'departureDate': data['departureDate'], 
                  'durationTime': data['durationTime'], 
                  'seats_available': int( re.findall( r'\d+', seat.get_text() )[0] ), 
                  'timestampScrape': datetime.now().strftime( '%Y-%m-%dT%H:%M:%S' ) }
    data_list.append( data_dict )

df = pd.DataFrame( data_list )
print( df )

# save the dataset as a csv file
