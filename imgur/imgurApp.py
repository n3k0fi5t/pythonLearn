#!/usr/bin/env python
import os
from sys import argv
from imgurpython import ImgurClient
from authentication import authenticate
from config import album_id, client_id, client_secret

def upload(img):
    # authenticate first
    client = authenticate()
    config = {
            'album' : album_id
            }

    if client is not None:
        img_path = os.path.join('', img)
        if os.path.exists(img_path):
            resp = client.upload_from_path(img_path, config=config, anon=False)
        else:
            resp = client.upload_from_url(img_path, config=config, anon=False)
    print("Upload finished. \n\t id : {0:<10}\n\tlink : {1:<10}".format(resp['id'], resp['link']))

if __name__ == '__main__':
    assert len(argv)>1, 'Must have a image path'
    upload(argv[1])
