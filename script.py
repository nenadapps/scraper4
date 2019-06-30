import datetime
from random import randint,shuffle
from time import sleep
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def get_html(url):
    html_content = ''
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        html_content = BeautifulSoup(html_page, "html.parser")
    except: 
        pass
        
    return html_content

def get_details(url, category):
    
    stamp = {}

    try:
       html = get_html(url)
    except:
       return stamp

    try:
        price = html.find_all("div", {"id":"showProdPrice"})[0].get_text()
        price = price.replace('£','')
        stamp['price'] = price.replace('&pound;','').strip()
    except:
        stamp['price'] = None

    try:
        name = html.find_all("span", {"class":"summary"})[0].get_text()
        stamp['title'] = name
    except:
        stamp['title'] = None

    try:
        sku = html.find_all("dd", {"id":"prodModel"})[0].get_text()
        stamp['sku'] = sku
    except:
        stamp['sku'] = None

    stamp['category'] = category

    try:
        year = html.find_all("a", {"class":"brand"})[0].get_text()
        stamp['year'] = year
    except:
        stamp['year'] = None

    try:
        country = html.find_all("dd", {"class":"scat"})[0].get_text()
        stamp['country'] = country
    except:
        stamp['country'] = None

    try:
        raw_text = html.find_all("div", {"id":"desc_1"})[0].get_text()
        stamp['raw_text'] = raw_text.replace('¬†','.').strip()
    except:
        stamp['raw_text'] = None

    stamp['currency'] = "GBP"

    # image_urls should be a list
    try:
        images = html.find_all("a", {"id":"def_image"})[0].get('href')
        stamp['image_urls'] = images
    except:
        stamp['image_urls'] = None

    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    stamp['url'] = url
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 69)) # Waiting between 25s and 69s between requests.
    return stamp

def get_category_items(category_url):
    items = []
    next_url = ''

    try:
        category_html = get_html(category_url)
    except:
        return items, next_url

    try:
        for item in category_html.select('.product a'):
            item_link = 'https://www.zeboose.com' + item.get('href')
            items.append(item_link)
    except: 
        pass

    try:
        next_url = category_html.select('link[rel=next]')[0].get('href')
    except:
        pass

    shuffle(items)

    return items, next_url

# choose category url with an input statement
continents = {
    'Africa':'https://www.zeboose.com/africa/c70', 
    'Asia':'https://www.zeboose.com/asia/c69',
    'America':'https://www.zeboose.com/america/c72',
    'Europe':'https://www.zeboose.com/europe/c68',
    'Oceania':'https://www.zeboose.com/oceania/c71'
}

for key in continents:
    print(key + ': ' + continents[key]) 

continent = input('Pick a continent: ')

try:
    category_url = continents[continent]
    while(category_url):
        category_items, category_url = get_category_items(category_url)
        # loop through all category items
        for category_item in category_items:
            stamp = get_details(category_item, continent) 
except:
    print('This continent doesn\'t exist in list. Please pick some of provided continents.')
         