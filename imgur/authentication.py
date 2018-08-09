#!/usr/bin/env python
import requests
import re
from bs4 import BeautifulSoup
from imgurpython import ImgurClient
from config import client_id, client_secret, pa44w0rd, acc0un5


API_URL='https://api.imgur.com/'

def getUrl(resp_type='pin'):
    return '{0}oauth2/authorize?client_id={1}&response_type={2}'.format(API_URL, client_id, resp_type)

def getPin(auth_url):
    rs = requests.session()
    #auth_url = getUrl()

    resp = rs.get(auth_url)
    payload={
            'username' : acc0un5,
            'password' : pa44w0rd,
            'allow' : rs.cookies.get('authorize_token'),
            '_jafo[activeExperiments]' : [],
            '_jafo[experimentData]' : {}
     }
    resp = rs.post(auth_url,data=payload)

    code = BeautifulSoup(resp.text, "html.parser")
    resp = rs.post(auth_url, data=payload)

    r = code.find('link',rel='canonical')
    m = re.search('pin=.+" rel',str(r))

    pin = ''
    if m :
        s = m.group()
        pin=s[4:len(s)-5]
    return pin

def authenticate():
    client = ImgurClient(client_id, client_secret)

    authorization_url = client.get_auth_url('pin')

    pin = getPin(authorization_url)
    print("Get pin {0}".format(pin))

    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

    print("Authentication finished.")

    return client
if __name__ == '__main__':
    print(getPin())
