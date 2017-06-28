from collections import OrderedDict #ordered dict
from bs4 import BeautifulSoup # for pulling data out of html
import requests # for accesing web page
import datetime as dt
import time
import csv
from bs4 import BeautifulSoup # parsing data


with open('C:\Users\YOONHO\Desktop\\cred\\WMT_API_cred.csv','r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        wmtauth_d = row
    

WMT_open_API_key = wmtauth_d['WMT_api_key'] 
consumer_id = wmtauth_d['ConsumerId']
private_key = wmtauth_d['PrivateKey']
Consumer_channel_type = wmtauth_d['Consumer_channel_type']
#walmart

'''
class WMT(Object):
    def __init__:
'''

def wmt_item_lookup(WMT_Item_id):
    WMT_Item_id = str(WMT_Item_id)
    URI_item = 'http://api.walmartlabs.com/v1/items/' + WMT_Item_id + '?apiKey=' + WMT_open_API_key + '&lsPublisherId={}&format=xml'
    r = requests.get(URI_item)
    soup = BeautifulSoup(r.content, 'xml')
    price = round(float(soup.find('salePrice').string), 2)
    
    
    return price

