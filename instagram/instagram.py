#!/usr/bin/env python

import json
import os
import requests
import getpass
import hashlib
import argparse
import numpy
from io import BytesIO

# third party module
from PIL import Image
import tqdm
import cv2

# import API
from instagram_private_api import Client

FETCH_DELAY = 3
DISPLAY_DELAY = 0.5

# util
def display_info(item):
    print(
"""
Name: {0}\n
Caption: {1}\n
Likes: {2}
""".format(
        item['user']['username'],
        item['caption']['text'],
        item['like_count']
    ))

def sleep(delay, normal=False, desc='Fetching for early posts'):
    from time import sleep as slp
    from tqdm import trange
    if normal:
        slp(delay)
    else:
        for _ in trange(delay*10, desc=desc):
            try:
                slp(0.1)
            except KeyboardInterrupt:
                raise()
        slp(0.1)

def remove_images():
    if not os.path.isdir('images'):
        return

    for fn in os.listdir('./images/'):
        os.remove('./images/' + fn)


def generate_header(api, headers=None):
    """
    generate header for session to fetch images because of limited API
    """
    if not headers:
        headers = {
            'User-Agent': api.user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
        }
        headers.update({
            'x-csrftoken': api.csrftoken,
            'x-requested-with': 'XMLHttpRequest',
            'x-instagram-ajax': '1',
            'Referer': 'https://www.instagram.com',
            'Authority': 'www.instagram.com',
            'Origin': 'https://www.instagram.com',
            'Content-Type': 'application/x-www-form-urlencoded'
            })
    return headers

def login():
    api = None
    while api is None:
        usr, pwd = None, None
        usr = input("User name: ")
        pwd = getpass.getpass("Password")

        try:
            api = Client(usr, pwd, auto_patch=True)
        except KeyboardInterrupt:
            raise()
        except:
            print("Fail to login")
            api = None

    return api

def fetch_timeline_feed(api, **kwargs):
    def read_image(ss, item):
        resp = ss.get(item['images']['standard_resolution']['url'])
        img = Image.open(BytesIO(resp.content))
        return img

    def save_image(item=None, img=None):
        if img is None or item is None:
            return

        try:
            fn = item['user']['username'] + '_' + \
                hashlib.md5((item['user']['username'] + \
                item['caption']['text']) \
                .encode('utf-8')).hexdigest() + '.jpg'
            img.save('images/' + fn)
        except:
            print("Fail to save image")

        # other way to save image from http
        """
        with open('images/' + fn, 'wb') as fp:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    fp.write(chunk)
        """

    # preprocess arguments and initialize variables
    saved = kwargs.pop('saved', False)
    once = kwargs.pop('once', False)
    content = kwargs.pop('content', False)
    next_max_id = ''


    if saved or content:
        # create session for fetching images
        img_ss = requests.Session()
        img_ss.get('https://www.instagram.com/')
        img_ss.headers.update(generate_header(api))

        # create a window to show the images
        if content:
            cv2.namedWindow('Fetched image', cv2.WINDOW_NORMAL)

    while True:
        try:
            if next_max_id != '':
                results = api.feed_timeline(max_id=next_max_id)
            else:
                results = api.feed_timeline()

            next_max_id = results.get('next_max_id', '')

        except:
            print("Fetch fail")
            exit()

        # timeline items
        items = [item.get('media_or_ad') for item in results.get('feed_items', []) if item.get('media_or_ad')]

        for _ in items:
            try:
                display_info(_)
                print("#" * 50)
                if content or saved:
                    img = read_image(img_ss, _)
                else:
                    img = None

                if saved:
                    save_image(item=_, img=img)

                if content:
                    cv_img = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
                    cv2.imshow('Fetched image', cv_img)
                    cv2.waitKey(0)
                else:
                    sleep(DISPLAY_DELAY, normal=True)
            except KeyboardInterrupt:
                raise()
            except:
                # drop invalid item
                pass
        sleep(FETCH_DELAY)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--saved', action='store_true', \
             default=False, help='Save images or not')
    parser.add_argument('-o', '--once', action='store_true', \
             default=False, help='Display one post at a time')
    parser.add_argument('-c', '--content-only', action='store_true', \
            default=False, help='Display with or without image, only support in once mode')

    api = login()
    args = parser.parse_args()
    saved, once = args.saved, args.once
    content = args.content_only if once else False


    if saved:
        if not os.path.exists('images'):
            os.makedirs('images')
        else:
            remove_images()

    fetch_timeline_feed(api, saved=saved, once=once, content=content)

if __name__ == '__main__':
    main()
