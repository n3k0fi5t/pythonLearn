#!/usr/bin/env python

from sys import argv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from bs4 import BeautifulSoup as bs
from time import sleep


SEARCH_STRING =  "角亭"
WAIT_INTERVAL = 2.2
SCROLL_PAUSE_TIME = 0.15

XPATH = {
    'store' : "//*[@id='pane']/div/div[2]/div/div/div[1]/div[1]/button[1]",
    'search' : "//*[@id='pane']/div/div[2]/div/div/button/jsl/jsl[7]",
    'comments' : "//*[@id='pane']/div/div[1]/div/div/div[1]/div[3]/div[2]/div/div[1]/span[3]/ul/li/span[2]/span[1]/button",
    'scroll_down' : '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[6]/div/div',
    'store_name' : "//*[@id='pane']/div/div[2]/div/div/div[1]/div[3]/div[1]"
}

def back(driver, xpath):
    ele = driver.find_element_by_xpath(xpath)
    ele.click()
    sleep(WAIT_INTERVAL)

def scroll_down(driver):
    # find all comments
    element = driver.find_element_by_xpath(XPATH['scroll_down'])
    #element = driver.find_element_by_class_name('section-reviewchart-numreviews')
    element.click()
    actions = ActionChains(driver)

    while(1):
        src = driver.page_source
        for i in range(10):
            #element.send_keys(Keys.SPACE)
            actions.send_keys(Keys.SPACE).perform()
            sleep(SCROLL_PAUSE_TIME)

        sleep(WAIT_INTERVAL)
        if src == driver.page_source:
            break
    print('comment end')

def get_comments(src):
    # list all comments
    code = bs(src, "html.parser")
    cmts = []
    for (idx,item) in enumerate(code.findAll(attrs={'class':'section-review-text'})):
        # only save valid comment
        if len(item.text) > 0:
            cmts.append("    {0}".format(item.text))
    return cmts

def perform_comment(driver, res, search=True, store_name=""):
    comment = driver.find_element_by_xpath(XPATH['comments'])
    comment.click()
    sleep(WAIT_INTERVAL)

    print("search... {}\n".format(store_name))
    scroll_down(driver)
    comments = get_comments(driver.page_source)
    res.append({store_name : comments})

    with open("search_result.txt", mode="a") as fp:
        fp.write("{0}\n".format(store_name))
        for c in comments:
            fp.write("{0}\n".format(c))
        fp.close()

    back(driver, XPATH['store'])

    if search:
        back(driver, XPATH['search'])

def main(search_string=SEARCH_STRING):
    driver = webdriver.Chrome()
    driver.get("https://www.google.com.tw/maps")

    res = []

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
    # wait for search
    WebDriverWait(driver, 20)
    src = driver.page_source

    eles = driver.find_elements_by_class_name("section-result-text-content")
    for i in range(len(eles)):
        store_name = eles[i].text
        eles[i].click()
        sleep(WAIT_INTERVAL)

        perform_comment(driver, res, store_name=store_name)

        eles = driver.find_elements_by_class_name("section-result-text-content")

    if len(eles) == 0 :
        comment = None
        try:
            comment = driver.find_element_by_xpath(XPATH['comments'])
        except:
            print("Not find any of {}".format(SEARCH_STRING))

        if comment:
            perform_comment(driver, res, search=False, store_name=search_string)


if __name__ == '__main__':
    if len(argv) > 1:
        main(search_string=argv[1])
    else:
        main()
