import requests, pandas as pd
from bs4 import BeautifulSoup
from glob import glob
from datetime import datetime
from time import sleep 

HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Accept-Language': 'en-US, en;q=0.5'})

# Filename, whether the list is kindle items or not
def scrape(filename, kindle=False):
    filename = 'tracker/' + filename
    now = datetime.now()

    prod_tracker = pd.read_csv(filename , sep=';')
    prod_tracker_URLS = prod_tracker.url

    if kindle:
        id = 'kindle-price'
        history = 'history-kindle.txt'
    else:
        id = 'priceblock_ourprice'
        history = 'history.txt'

    f = open('scrapes/{history}'.format(history=history),'a')

    for x, url in enumerate(prod_tracker_URLS):
        page = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(page.content, features='lxml')

        title = soup.find(id='productTitle').getText().strip()

        # Catch error incase of missing price
        try:
            price = float(soup.find(id=id).getText().replace('£','').strip())
        except:
            price = ''

        #format date and time 
        dateTime = now.strftime("%d/%m/%Y %H:%M:%S")
        write = dateTime + ': ' + title + ': ' + str(price) + '\n'
        f.write(write)
    
    f.close()

    # Test
    # print(type(price))
    # print(price)
    # print(title)


scrape('price-tracker.csv')