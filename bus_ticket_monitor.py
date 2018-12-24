# -*- coding: utf-8 -*-

# libraries
from bs4            import BeautifulSoup 
from datetime       import datetime

import re
import json
import pandas        as pd
import requests     

# generate range of date to consult
date_range = pd.date_range(pd.datetime.now(), periods=32).strftime( '%Y-%m-%d' ).tolist()

# parameters
root = 'https://www.clickbus.com.br/'
vehicle = 'onibus'
origin = 'sao-paulo-sp-todos'
destinations = ['campinas-sp', 'mogi-guacu-sp']

df_final = pd.DataFrame()
for destination in destinations:

    for date in date_range:
        # website address
        web_address = root+vehicle+'/'+origin +'/'+destination+'?departureDate='+date 

        print( web_address )

        # access the link
        response = requests.get( web_address )
        page = response.text
        soup = BeautifulSoup( page,"lxml" )

        # get bus lines information & seats available
        date_now = datetime.now().strftime( '%Y-%m-%dT%H:%M:%S' )
        seats = soup.find_all( class_='available-seats' ) 
        buslines = soup.find_all( class_="search-item search-item-direct " )

        # iterate over bus lines information and seats available
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
                          'price': data['price'],
                          'timestampScrape': date_now }
            data_list.append( data_dict )

        df = pd.DataFrame( data_list, columns=['departureDate', 'arrivalDate', 'departureStation', 'arrivalStation', 'departureTime', 'arrivalTime', 
                                               'durationTime', 'company', 'price', 'seats_available', 'timestampScrape'] )

    df_final = pd.concat( [df_final, df] )

# save the dataset as a csv file
df_final.to_csv( 'buslines-at-{}.csv'.format( re.sub( r':', '-', date_now ) ) )
