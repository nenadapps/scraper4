import re
import datetime
import os
#import sqlite3
#from fake_useragent import UserAgent
import shutil
#from stem import Signal
#from stem.control import Controller
#import socket
#import socks
import requests
from random import randint, shuffle
from time import sleep
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
'''
controller = Controller.from_port(port=9051)
controller.authenticate()

def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5 , "127.0.0.1", 9050)
    socket.socket = socks.socksocket

def renew_tor():
    controller.signal(Signal.NEWNYM)

def showmyip():
    url = "http://www.showmyip.gr/"
    r = requests.Session()
    page = r.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    try:
    	ip_address = soup.find("span",{"class":"ip_address"}).text()
    	print(ip_address)
    except:
        print('IP problem')
    
UA = UserAgent(fallback='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2')

hdr = {'User-Agent': "'"+UA.random+"'",
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
'''
def get_html(url):
    html_content = ''
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})#hdr)
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
        price = price.replace('£', '')
        stamp['price'] = price.replace('&pound;', '').strip()
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
        stamp['raw_text'] = raw_text.replace('¬†', '.').strip()
    except:
        stamp['raw_text'] = None
    
    try:
        temp = raw_text.split(" ")
        scott_num = temp[-2].replace('SC', '')
        SG = temp[-3].replace('SG', '')
        stamp['scott_num'] = scott_num
        stamp['SG'] = SG.replace(";", "")
    except:
        stamp['scott_num'] = None
        stamp['SG'] = None
        
    stamp['currency'] = "GBP"

    # image_urls should be a list
    images = []
    try:
        image_items = html.select('#eimgHovers img')
        if image_items:
            for image_item in image_items:
                img = image_item.get('src').replace('micro', 'zoom')
                images.append(img)
        else:
            img = html.find_all("a", {"id":"def_image"})[0].get('href')
            images.append(img)
    except:
        pass
        
    stamp['image_urls'] = images      

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
'''
def file_names(stamp):
    file_name = []
    rand_string = "RAND_ze"+str(randint(0,100000))
    file_name = [rand_string+"-" + str(i) + ".png" for i in range(len(stamp['image_urls']))]
    return(file_name)

def query_for_previous(stamp):
    # CHECKING IF Stamp IN DB
    os.chdir("/Volumes/Stamps/")
    conn1 = sqlite3.connect('Reference_data.db')
    c = conn1.cursor()
    col_nm = 'url'
    col_nm2 = 'raw_text'
    unique = stamp['url']
    unique2 = stamp['raw_text']
    c.execute('SELECT * FROM zeboose WHERE "{cn}" LIKE "{un}%" AND "{cn2}" LIKE "{un2}%"'.format(cn=col_nm, cn2=col_nm2, un=unique, un2=unique2)))
    all_rows = c.fetchall()
    conn1.close()
    price_update=[]
    price_update.append((stamp['url'],
    stamp['raw_text'],
    stamp['scrape_date'], 
    stamp['price'], 
    stamp['currency']))
    
    if len(all_rows) > 0:
        print ("This is in the database already")
        conn1 = sqlite3.connect('Reference_data.db')
        c = conn1.cursor()
        c.executemany("""INSERT INTO price_list (url, raw_text, scrape_date, price, currency) VALUES(?,?,?,?,?)""", price_update)
        conn1.commit()
        conn1.close()
        print (" ")
        #url_count(count)
        sleep(randint(10,45))
        pass
    else:
        os.chdir("/Volumes/Stamps/")
        conn2 = sqlite3.connect('Reference_data.db')
        c2 = conn2.cursor()
        c2.executemany("""INSERT INTO price_list (url, raw_text, scrape_date, price, currency) VALUES(?,?,?,?,?)""", price_update)
        conn2.commit()
        conn2.close()
    print("Price Updated")

def db_update_image_download(stamp): 
    req = requests.Session()
    directory = "/Volumes/Stamps/stamps/zeboose/" + str(datetime.datetime.today().strftime('%Y-%m-%d')) +"/"
    image_paths = []
    names = file_names(stamp)
    image_paths = [directory + names[i] for i in range(len(names))]
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)
    for item in range(0,len(names)):
        print (stamp['image_urls'][item])
        try:
            imgRequest1=req.get(stamp['image_urls'][item],headers=hdr, timeout=60, stream=True)
        except:
            print ("waiting...")
            sleep(randint(3000,6000))
            print ("...")
            imgRequest1=req.get(stamp['image_urls'][item], headers=hdr, timeout=60, stream=True)
        if imgRequest1.status_code==200:
            with open(names[item],'wb') as localFile:
                imgRequest1.raw.decode_content = True
                shutil.copyfileobj(imgRequest1.raw, localFile)
                sleep(randint(18,30))
    stamp['image_paths']=", ".join(image_paths)
    #url_count += len(image_paths)
    database_update =[]

    # PUTTING NEW STAMPS IN DB
    database_update.append((
        stamp['url'],
        stamp['raw_text'],
        stamp['title'],
        stamp['scott_num'],
        stamp['SG'],
        stamp['country'],
        stamp['year'],
        stamp['category'],
        stamp['sku'],
        stamp['scrape_date'],
        stamp['image_paths']))
    os.chdir("/Volumes/Stamps/")
    conn = sqlite3.connect('Reference_data.db')
    conn.text_factory = str
    cur = conn.cursor()
    cur.executemany("""INSERT INTO zeboose ('url','raw_text', 'title', 'scott_num','SG',
    'country','year','category','sku','scrape_date','image_paths') 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", database_update)
    conn.commit()
    conn.close()
    print ("all updated")
    print ("++++++++++++")
    print (" ")
    sleep(randint(45,140)) 
'''
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

count = 0
#connectTor()
#showmyip()
try:
    category_url = continents[continent]
    while(category_url):
        category_items, category_url = get_category_items(category_url)
        count += 1
        # loop through all category items
        for category_item in category_items:
            try:
                count += 1
                if count > randint(75, 156):
                    sleep(randint(500, 2000))
                    #connectTor()
                    count = 0
                else:
                    pass
                stamp = get_details(category_item, continent)
                count += len(file_names(stamp))
                #query_for_previous(stamp)
                #db_update_image_download(stamp)
            except:
                pass
except:
    print('This continent doesn\'t exist in list. Please pick some of provided continents.')