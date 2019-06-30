import datetime
from random import randint
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

def get_details(url):
    
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

    try:
        year = html.find_all("a", {"class":"brand"})[0].get_text()
        stamp['year']=year
    except:
        stamp['year']=None

    try:
        country = html.find_all("dd", {"class":"scat"})[0].get_text()
        stamp['country']=country
    except:
        stamp['country']=None

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
	sleep(randint(25, 69)) # Waiting between 25s and 69s between requests.
    return stamp

url = 'https://www.zeboose.com/aden-1939-mlh-definitives-sg16-27-sc16-27/p3194'
stamp = get_details(url)
print(stamp)
         