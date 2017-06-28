from collections import OrderedDict #ordered dict
from bs4 import BeautifulSoup # for pulling data out of html
import requests # for accesing web page
import datetime as dt
import time
import csv
from bs4 import BeautifulSoup # parsing data
import hmac, hashlib, urllib, base64
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


with open('C:\Users\YOONHO\Desktop\\cred\\WMT_API_cred.csv','r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        wmtauth_d = row
    

WMT_api_key = wmtauth_d['WMT_api_key'] 
consumer_id = wmtauth_d['ConsumerId']
private_key = wmtauth_d['PrivateKey']
Consumer_channel_type = wmtauth_d['Consumer_channel_type']
#walmart




class WMT(object):
    def __init__(self,consumer_id, private_key,Consumer_channel_type):
        self.headers = {
                        #walmart service name
                        'WM_SVC.NAME' : 'Walmart Marketplace',
                        #a unique ID to correlate your calls with the walmart system
                        'WM_QOS.CORRELATION_ID' : '123456abcdef',
                        'WM_SEC.TIMESTAMP' :str(int(time.time() * 1000)),
                        'WM_SEC.AUTH_SIGNATURE' : None,
                        #a unique Id to track the consumer request by channel
                        'WM_CONSUMER.CHANNEL.TYPE' : Consumer_channel_type,
                        'WM_CONSUMER.ID' : consumer_id,
                        #the returned data format in response
                        'Accept' : 'application/xml'            
                }
        self.privatekey = private_key
    
    def get_sig(self, url, httpmethod, timestamp):
        consumer_id =self.headers['WM_CONSUMER.ID']
        str_to_sign = consumer_id + '\n' + url +'\n' + httpmethod +'\n' +timestamp +'\n'
        encodedKeyBytes = base64.b64decode(self.privatekey)
        privspec = RSA.importKey(encodedKeyBytes, 'pkcs8')
        signer = PKCS1_v1_5.new(privspec)
        sign = signer.sign(SHA256.new(str_to_sign))
        return base64.b64encode(sign)
    
    def WMT_request(self, action, URI, **kwargs):
        baseurl = 'https://marketplace.walmartapis.com' + URI
        params = {}

        for k, v in kwargs.items():
            params[k] = v
                  
        url_params = '&'.join(['%s=%s'%(param[0], param[1]) for param in params.items()])
        url = baseurl + '?' + url_params
        signature = self.get_sig(url, action, self.headers['WM_SEC.TIMESTAMP'])
        #print(url, action, self.headers['WM_SEC.TIMESTAMP'] + '\n')
        #print(signature)
        self.headers['WM_SEC.AUTH_SIGNATURE'] = signature
        

        #print(url, params, self.headers)
                  
        session = requests.Session()
        r = session.get(baseurl, params = params, headers = self.headers)
       # print(r.headers.keys())
        return r
        #print(r)
        
class Orders(WMT):    
    #timestamp = str(int(time.time()))
    def AllReleasedOrders(self, **kwargs):
        URI = '/v3/orders/released'
        r = self.WMT_request('GET', URI, **kwargs)
        soup = BeautifulSoup(r.content, 'xml')
        return soup
    
    def AllOrders(self, **kwargs):
        URI = '/v3/orders'
        r = self.WMT_request('GET', URI, **kwargs)
        soup = BeautifulSoup(r.content, 'xml')
        return soup
        


zz = Orders(consumer_id, private_key, Consumer_channel_type)
soup = zz.AllReleasedOrders(createdStartDate = '2017-06-16', limit = '200')


zz = Orders(consumer_id, private_key, Consumer_channel_type)
orders = zz.AllOrders(createdStartDate = '2017-06-16', limit = '200')
for order in orders.find_all('order'):
    print(order)
len(orders.find_all('order'))


