import requests
from bs4 import BeautifulSoup
from random import choice

def get_proxy():
    url ='https://www.sslproxies.org/'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    # doing it all at once
    data = list(map(lambda x:x[0]+':'+x[1], list(zip(map(lambda x:x.text, soup.findAll('td')[::8]), 
                                     map(lambda x:x.text, soup.findAll('td')[1::8])))))
    # get a random choice from list
    return {'https':choice(data)}

class forbidden_error(Exception):
#     print('Proxy select is 403 Forbidenn')
    pass
    

# def proxy_request(request_type, url, **kwargs):
#     #This is a infinate loop until its breaks hence the while ONE (not lowercase"L" or "I")
# #     while 1:
#     for x in range(0,100):
#         try:
#             if working_proxy is None:
#                 proxy = get_proxy()
#             else:
#                 proxy = working_proxy

#             print('Using proxy: {}'.format(proxy))
#             r = requests.request(request_type, url, proxies=proxy, timeout=5, **kwargs)
#             if BeautifulSoup(r.content, 'html.parser').select_one('title').text.strip() == '403 Forbidden':
#                 print('Proxy select is 403 Forbidenn')
#                 raise forbidden_error # Exception is raise to trip the try and move onto next attempt
#             break
#             working_proxy = proxy 
#         except:
#             pass
       
#     return r

def proxy_request(request_type, url, **kwargs):
    #This is a infinate loop until its breaks hence the while ONE (not lowercase"L" or "I")
#     while 1:
    for x in range(0,100):
        try:
            proxy = get_proxy()
            print('Using proxy: {}'.format(proxy))
            r = requests.request(request_type, url, proxies=proxy, timeout=5, **kwargs)

            if BeautifulSoup(r.content, 'html.parser').select_one('title').text.strip() == '403 Forbidden':
                print('Proxy select is 403 Forbidden')
                raise forbidden_error # Exception is raise to trip the try and move onto next attempt
            
            working_proxy = proxy
            break
        except:
            pass
    return r

def area_scraper(url):
    import sys
    
    if 'requests' not in sys.modules:
        import requests
    
    if 'BeautifulSoup' not in sys.modules:
        from bs4 import BeautifulSoup
        
    if 'datetime' not in sys.modules:
        import datetime as dt
        
    if 'sleep' not in sys.modules:
        from time import sleep
        
    if 'numpy' not in sys.modules:
        import numpy as np
        
    r = proxy_request('get', url)

    soup = BeautifulSoup(r.content, 'html.parser')
    
    area = dict()
    
    area['scrape_time'] = str(dt.datetime.now())
    
    area['source'] = 'Zoopla'
    
    area['postcode'] = soup.select_one('#content > h1').text.strip()
    
    area['average_price_paid'] = soup.select_one('#content > div.market-panel-wrapper > div > div.market-panel-stats > span:nth-of-type(1) > span.market-panel-stat-element-value.js-market-stats-average-price').text.strip()
    
    area['average_estimated_price'] = soup.select_one('#content > div.market-panel-wrapper > div > div.market-panel-stats > span:nth-of-type(3) > span.market-panel-stat-element-value.js-market-stats-average-value').text.strip()
    
    area['sales'] = soup.select_one('#content > div.market-panel-wrapper > div > div.market-panel-stats > span:nth-of-type(2) > span.market-panel-stat-element-value.js-market-stats-num-sales').text.strip()
    
    area['value_change'] = soup.select_one('#content > div.market-panel-wrapper > div > div.market-panel-stats > span:nth-of-type(4) > span.market-panel-stat-element-value.js-market-stats-value-change.market-panel-stat-value-change-up').text.strip()
    
    area['percentage_change'] = soup.select_one('#content > div.market-panel-wrapper > div > div.market-panel-stats > span:nth-of-type(4) > span.market-panel-stat-element-small.js-market-stats-value-change-pct.market-panel-stat-value-change-up').text.strip()
    
    sleeper = 10 * np.random.uniform(0,1)
    
    sleep(sleeper)
    
    return area
def for_sale_scraper(url):
    import sys
        
    if 'requests' not in sys.modules:
        import requests
        
    if 'BeautifulSoup' not in sys.modules:
        from bs4 import BeautifulSoup
            
    if 'datetime' not in sys.modules:
        import datetime as dt
            
    if 'sleep' not in sys.modules:
        from time import sleep
            
    if 'numpy' not in sys.modules:
        import numpy as np
        
    property_price = [] 
    visited_urls =[]
    
    print('Starting scraping from: ' + url)
    
    # while url not in visited_urls:
    while ((url not in visited_urls) & (len(visited_urls)<=5)) :
         
        r = proxy_request('get', url)

        soup = BeautifulSoup(r.content, 'html.parser')

        property_list = soup.select('#content > ul > li')


        for li in property_list:

            temp = dict()
            
            temp['scrape_time'] = str(dt.datetime.now())
    
            temp['source'] = 'Zoopla'

            temp['address'] = li.select_one('div > div.listing-results-right.clearfix > span > a')
            if temp['address'] is not None:
                temp['address'] = temp['address'].text.strip()

            temp['asking_price'] = li.select_one('div > div.listing-results-right.clearfix > a')
            if temp['asking_price'] is not None:
                temp['asking_price'] = temp['asking_price'].text.strip()

            temp['number_of_bedrooms'] = li.select_one('div > div.listing-results-right.clearfix > h3 > span.num-icon.num-beds')
            if temp['number_of_bedrooms'] is not None:
                temp['number_of_bedrooms'] = temp['number_of_bedrooms'].text.strip()       

            temp['number_of_bathrooms'] = li.select_one('div > div.listing-results-right.clearfix > h3 > span.num-icon.num-baths')
            if temp['number_of_bathrooms'] is not None:
                temp['number_of_bathrooms'] = temp['number_of_bathrooms'].text.strip()

            temp['number_of_reception_rooms'] = li.select_one('div > div.listing-results-right.clearfix > h3 > span.num-icon.num-reception')
            if temp['number_of_reception_rooms'] is not None:
                temp['number_of_reception_rooms'] = temp['number_of_reception_rooms'].text.strip()

            property_price.append(temp)
            
        visited_urls.append(url)
        
        next_page_url = soup.select('#content > div.paginate.bg-muted > a')[-1]
        if next_page_url is not None:
            url = 'https://www.zoopla.co.uk' + str(next_page_url['href'])
            sleeper = 10 * np.random.uniform(0,1)
            sleep(sleeper)
    #         print(next_page_url)
    #         self.log('About to scrape: ' + next_page_url
            print('About to scrape: ' + url)

#         self.log(next_page_url + 'has already been scraped.')
    print(url + ' has already been scraped.')
    return property_price

def property_rent_scraper(url):
    import sys
    
    if 'requests' not in sys.modules:
       import requests
        
    if 'BeautifulSoup' not in sys.modules:
        from bs4 import BeautifulSoup
            
    if 'datetime' not in sys.modules:
        import datetime as dt
            
    if 'sleep' not in sys.modules:
        from time import sleep
            
    if 'numpy' not in sys.modules:
        import numpy as np
        
    property_rent = [] 
    visited_urls =[]
    
    print('Starting scraping from: ' + url)
    
    # while url not in visited_urls:
    while ((url not in visited_urls) & (len(visited_urls)<=5)) :
         
        r = proxy_request('get', url)

        soup = BeautifulSoup(r.content, 'html.parser')

        property_list = soup.select('#content > ul > li')


        for li in property_list:

            temp = dict()
            
            temp['scrape_time'] = str(dt.datetime.now())
    
            temp['source'] = 'Zoopla'

            temp['address'] = li.select_one('div > div.listing-results-right.clearfix > span > a')
            if temp['address'] is not None:
                temp['address'] = temp['address'].text.strip()

            temp['cost'] = li.select_one('div > div.listing-results-right.clearfix > a')
            if temp['cost'] is not None:
                temp['cost'] = temp['cost'].text.strip()

            temp['number_of_bedrooms'] = li.select_one('div > div.listing-results-right.clearfix > h3 > span.num-icon.num-beds')
            if temp['number_of_bedrooms'] is not None:
                temp['number_of_bedrooms'] = temp['number_of_bedrooms'].text.strip()       

            temp['number_of_bathrooms'] = li.select_one('div > div.listing-results-right.clearfix > h3 > span.num-icon.num-baths')
            if temp['number_of_bathrooms'] is not None:
                temp['number_of_bathrooms'] = temp['number_of_bathrooms'].text.strip()

            temp['number_of_reception_rooms'] = li.select_one('div > div.listing-results-right.clearfix > h3 > span.num-icon.num-reception')
            if temp['number_of_reception_rooms'] is not None:
                temp['number_of_reception_rooms'] = temp['number_of_reception_rooms'].text.strip()

            temp['square_footage'] = li.select_one('div > div.listing-results-right.clearfix > h3 > span.num-icon.num-sqft')
            if temp['square_footage'] is not None:
                temp['square_footage'] = temp['square_footage'].text.strip()

            property_rent.append(temp)
            
        visited_urls.append(url)
        
        next_page_url = soup.select('#content > div.paginate.bg-muted > a')[-1]
        if next_page_url is not None:
            url = 'https://www.zoopla.co.uk' + str(next_page_url['href'])
            sleeper = 10 * np.random.uniform(0,1)
            sleep(sleeper)
    #         print(next_page_url)
    #         self.log('About to scrape: ' + next_page_url
            print('About to scrape: ' + url)

    print(url + ' has already been scraped.')
    return property_rent


def property_price_scraper(url):
    import sys
    
    if 'requests' not in sys.modules:
        import requests
        
    if 'BeautifulSoup' not in sys.modules:
        from bs4 import BeautifulSoup
            
    if 'datetime' not in sys.modules:
        import datetime as dt
            
    if 'sleep' not in sys.modules:
        from time import sleep
            
    if 'numpy' not in sys.modules:
        import numpy as np

    property_price = [] 
    visited_urls =[]
    
    print('Starting scraping from: ' + url)
    
    # while url not in visited_urls:
    while ((url not in visited_urls) & (len(visited_urls)<=5)) :
         
        r = proxy_request('get', url)

        soup = BeautifulSoup(r.content, 'html.parser')

        table = soup.select('#content > div.browse-table-wrapper > table > tbody > tr')


        for tr in table:

            temp = dict()
            
            temp['scrape_time'] = str(dt.datetime.now())
    
            temp['source'] = 'Zoopla'

            temp['address'] = tr.select_one('td.browse-cell-address > a:nth-of-type(1) > div')
            if temp['address'] is not None:
                temp['address'] = temp['address'].text.strip()

            temp['address_url'] = tr.select_one('td.browse-cell-address > a:nth-of-type(1)')
            if temp['address_url'] is not None:
                temp['address_url'] = temp['address_url']['href']

            temp['last_sale_date'] = tr.select_one('td.browse-cell-date > div:nth-of-type(1) > div:nth-of-type(1)')
            if temp['last_sale_date'] is not None:
                temp['last_sale_date'] = temp['last_sale_date'].text.strip()       

            temp['last_sale_price'] = tr.select_one('td.browse-cell-date > div:nth-of-type(1) > div.sold-prices-data.sold-prices-data-price')
            if temp['last_sale_price'] is not None:
                temp['last_sale_price'] = temp['last_sale_price'].text.strip()

            temp['current_price_estimate'] = tr.select_one('td.browse-cell-estimate > span > a.jqModal > span')
            if temp['current_price_estimate'] is not None:
                temp['current_price_estimate'] = temp['current_price_estimate'].text.strip()

            property_price.append(temp)
            
        visited_urls.append(url)
        
        next_page_url = soup.select('#content > div.paginate.bg-muted > a')[-1]
        if next_page_url is not None:
            url = 'https://www.zoopla.co.uk' + str(next_page_url['href'])
            sleeper = 10 * np.random.uniform(0,1)
            sleep(sleeper)
    #         print(next_page_url)
    #         self.log('About to scrape: ' + next_page_url
            print('About to scrape: ' + url)

#         self.log(next_page_url + 'has already been scraped.')
    print(url + ' has already been scraped.')
    return property_price

def property_price_scraper(url):
    import sys
    
    if 'requests' not in sys.modules:
        import requests
        
    if 'BeautifulSoup' not in sys.modules:
        from bs4 import BeautifulSoup
            
    if 'datetime' not in sys.modules:
        import datetime as dt
            
    if 'sleep' not in sys.modules:
        from time import sleep
            
    if 'numpy' not in sys.modules:
        import numpy as np

    property_price = [] 
    visited_urls =[]
    
    print('Starting scraping from: ' + url)
    
    # while url not in visited_urls:
    while ((url not in visited_urls) & (len(visited_urls)<=5)) :
         
        r = proxy_request('get', url)

        soup = BeautifulSoup(r.content, 'html.parser')

        table = soup.select('#content > div.browse-table-wrapper > table > tbody > tr')


        for tr in table:

            temp = dict()
            
            temp['scrape_time'] = str(dt.datetime.now())
    
            temp['source'] = 'Zoopla'

            temp['address'] = tr.select_one('td.browse-cell-address > a:nth-of-type(1) > div')
            if temp['address'] is not None:
                temp['address'] = temp['address'].text.strip()

            temp['address_url'] = tr.select_one('td.browse-cell-address > a:nth-of-type(1)')
            if temp['address_url'] is not None:
                temp['address_url'] = temp['address_url']['href']

            temp['last_sale_date'] = tr.select_one('td.browse-cell-date > div:nth-of-type(1) > div:nth-of-type(1)')
            if temp['last_sale_date'] is not None:
                temp['last_sale_date'] = temp['last_sale_date'].text.strip()       

            temp['last_sale_price'] = tr.select_one('td.browse-cell-date > div:nth-of-type(1) > div.sold-prices-data.sold-prices-data-price')
            if temp['last_sale_price'] is not None:
                temp['last_sale_price'] = temp['last_sale_price'].text.strip()

            temp['current_price_estimate'] = tr.select_one('td.browse-cell-estimate > span > a.jqModal > span')
            if temp['current_price_estimate'] is not None:
                temp['current_price_estimate'] = temp['current_price_estimate'].text.strip()

            property_price.append(temp)
            
        visited_urls.append(url)
        
        next_page_url = soup.select('#content > div.paginate.bg-muted > a')[-1]
        if next_page_url is not None:
            url = 'https://www.zoopla.co.uk' + str(next_page_url['href'])
            sleeper = 10 * np.random.uniform(0,1)
            sleep(sleeper)
    #         print(next_page_url)
    #         self.log('About to scrape: ' + next_page_url
            print('About to scrape: ' + url)

#         self.log(next_page_url + 'has already been scraped.')
    print(url + ' has already been scraped.')
    return property_price

def insert_area(data):
    with conn:
        c.executemany("INSERT INTO area (scrape_time ,source ,postcode ,average_price_paid ,average_estimated_price ,sales ,value_change ,percentage_change) VALUES (:scrape_time ,:source ,:postcode ,:average_price_paid ,:average_estimated_price ,:sales ,:value_change ,:percentage_change)",[data])

def insert_rent(data):
    with conn:
#         Note data has no square beackets as the input will ahve multiple records
        c.executemany("INSERT INTO rental_prices (scrape_time ,source ,address ,cost ,number_of_bedrooms ,number_of_bathrooms ,number_of_reception_rooms ,square_footage) VALUES (:scrape_time ,:source ,:address ,:cost ,:number_of_bedrooms ,:number_of_bathrooms ,:number_of_reception_rooms ,:square_footage)",data)

def insert_propert_price(data):
    with conn:
        c.executemany("INSERT INTO Property_price (scrape_time ,source ,address ,address_url ,last_sale_date ,last_sale_price ,current_price_estimate) VALUES (:scrape_time ,:source ,:address ,:address_url ,:last_sale_date ,:last_sale_price ,:current_price_estimate)",data)

def insert_for_sale(data):
    with conn:
#         Note data has no square beackets as the input will ahve multiple records
        c.executemany("INSERT INTO for_sale_price (scrape_time, source, address, asking_price, number_of_bedrooms, number_of_bathrooms, number_of_reception_rooms) VALUES (:scrape_time, :source, :address, :asking_price, :number_of_bedrooms, :number_of_bathrooms, :number_of_reception_rooms)",data)


import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
 
 

create_connection(r"database.db")

conn = sqlite3.connect('database.db',timeout=10)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTs area (scrape_time INTEGER ,source TEXT ,postcode TEXT ,average_price_paid INTEGER ,average_estimated_price INTEGER ,sales INTEGER ,value_change INTEGER ,percentage_change TEXT)")
conn.commit()

import csv
import datetime as dt

postcode_list_csv = r'Scotland_Postcode_Area_List_For_Testing.csv'

base_price_url = 'https://www.zoopla.co.uk/house-prices/'
base_rent_url = 'https://www.zoopla.co.uk/to-rent/property/'
base_for_sale_url = 'https://www.zoopla.co.uk/for-sale/property/'
# global working_proxy
working_proxy = None



with open(postcode_list_csv,'rt',encoding='utf8') as f:
    reader = csv.reader(f)
    postcode_list = list(reader)
    

for pc in postcode_list:
    price_url = base_price_url + str(pc[0]) + '/'
    rent_url = base_price_url + str(pc[0]) + '/'
    for_sale_url = base_for_sale_url + str(pc[0]) + '/'
    print('price url is: ' + price_url)
    print('rent url is: ' + rent_url)
    print('for sale url is: ' + for_sale_url)
    
    rental_data = property_rent_scraper(rent_url)
    property_data = property_price_scraper(price_url)
    area_data = area_scraper(price_url)
    sale_data = for_sale_scraper(for_sale_url)
    
    insert_area(area_data)
    insert_rent(rental_data)
    insert_propert_price(property_data)
    insert_for_sale(sale_data)
    
    # self.log('Next URL :' + follow_url)

conn.close()
    


