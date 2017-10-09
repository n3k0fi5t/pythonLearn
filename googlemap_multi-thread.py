#!/usr/bin/env python

from sys import argv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs
from threading import Thread
from time import sleep


SEARCH_STRING =  "角亭"
WAIT_INTERVAL = 7
SCROLL_PAUSE_TIME = 0.2

XPATH = {
    'store' : "//*[@id='pane']/div/div[2]/div/div/div[1]/div[1]/button[1]",
    'search' : "//*[@id='pane']/div/div[2]/div/div/button/jsl/jsl[7]",
    'comments' : "//*[@id='pane']/div/div[2]/div/div/div[1]/div[3]/div[2]/div/div[1]/span[3]/ul/li/span",
    'scroll_down' : "//*[@id='pane']/div/div[2]/div/div/div[2]/div[8]",
    'store_name' : "//*[@id='pane']/div/div[2]/div/div/div[1]/div[3]/div[1]"
}

def back(driver, xpath):
    ele = driver.find_element_by_xpath(xpath)
    ele.click()
    sleep(WAIT_INTERVAL)

def scroll_down(driver):
    # find all comments
    element = driver.find_element_by_xpath(XPATH['scroll_down'])
    
    while(1):
        src = driver.page_source
        for i in range(10):
            element.send_keys(Keys.SPACE)
            sleep(SCROLL_PAUSE_TIME)
        # sleep(WAIT_INTERVAL)
        if len(src) == len(driver.page_source):
            break    

def get_comments(src):
    # list all comments
    code = bs(src, "html.parser")
    cmts = []
    for (idx,item) in enumerate(code.findAll(attrs={'class':'section-review-text'})):
        # only save valid comment
        if len(item.text) > 0: 
            cmts.append("    {0}".format(item.text))
    return cmts

def perform_comment(driver, res, search=True, store_name="", result_name=None):
    comment = driver.find_element_by_xpath(XPATH['comments'])
    comment.click()
    sleep(WAIT_INTERVAL)

    print("search... {}\n".format(store_name))
    scroll_down(driver)

    comment_src = driver.page_source
    # close the driver before parsing the source to save computing resource
    driver.close()

    comments = get_comments(comment_src)
    res.append({store_name : comments})

    with open("{0}.txt".format("search_result" if result_name is None else result_name), mode="a") as fp:
        fp.write("###{0}###\n".format(store_name))
        for c in comments:
            fp.write("{0}\n".format(c))
        fp.close()

    # try:
    #     back(driver, XPATH['store'])
    # except:
    #     driver.close()

    # if search:
    #     try:
    #         back(driver, XPATH['search'])
    #     except:
    #         driver.close()
        

def crawl_handler(res, idx, search_string):

    driver = webdriver.Chrome()
    driver.get("https://www.google.com.tw/maps")

    # wait for loading
    ele = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, "q")))

    searchbox = driver.find_element_by_name('q')

    searchbox.clear()
    searchbox.send_keys(search_string)

    """
        this two line of code is equal to ```searchbox.send_keys(Keys.RETURN)```
    """
    searchbox_button = driver.find_element_by_class_name("searchbox-searchbutton")
    searchbox_button.click()

    sleep(WAIT_INTERVAL)

    ele = driver.find_elements_by_class_name("section-result-text-content")[idx]
    store_name = ele.text
    ele.click()
    sleep(WAIT_INTERVAL)

    perform_comment(driver, res, store_name=store_name, result_name="{0}_{1}".format(store_name, idx))

def main(search_string=SEARCH_STRING):
    res = []
    threads = []

    driver = webdriver.Chrome()
    driver.get("https://www.google.com.tw/maps")

    # wait for loading
    ele = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, "q")))

    searchbox = driver.find_element_by_name('q')

    searchbox.clear()
    searchbox.send_keys(search_string)

    """
        this two line of code is equal to ```searchbox.send_keys(Keys.RETURN)```
    """
    searchbox_button = driver.find_element_by_class_name("searchbox-searchbutton")
    searchbox_button.click()

    sleep(WAIT_INTERVAL)

    eles = driver.find_elements_by_class_name("section-result-text-content")
    for i in range(len(eles)):
        res.append([])

        searchthread = Thread(target = crawl_handler,
                             args = (res[len(res)-1], i, search_string),
                             name="crawl thread_{0}".format(i))
        searchthread.setDaemon(1)
        threads.append(searchthread)
        searchthread.start()
        print("crawl thread_{0}  start...".format(i))


    if len(eles) == 0 :
        comment = None
        try:
            comment = driver.find_element_by_xpath(XPATH['comments'])
        except:
            print("Not find any of {}".format(search_string))

        if comment:
            perform_comment(driver, res, search=False, store_name=search_string, result_name=search_string)
    else :
        driver.close()
        while sum([1 if thread.isAlive() else 0 for thread in threads]) > 0:
            continue

    print("finished")

if __name__ == '__main__':
    if len(argv) > 1:
        main(search_string=argv[1])
    else:
        main()