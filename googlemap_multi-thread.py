#!/usr/bin/env python

from sys import argv, exit
from threading import Thread
from time import sleep


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs


SEARCH_STRING = "default"
WAIT_INTERVAL = 7
SCROLL_PAUSE_TIME = 0.2
THREAD_LIMIT = 2

XPATH = {
    'store': "//*[@id='pane']/div/div[2]/div/div/div[1]/div[1]/button[1]",
    'search': "//*[@id='pane']/div/div[2]/div/div/button/jsl/jsl[7]",
    #'comments': "//*[@id='pane']/div/div[2]/div/div/div[1]/div[3]/div[2]/div/div[1]/span[3]/ul/li/span",
    'comments':"//*[@id='pane']/div/div[1]/div/div/div[1]/div[3]/div[2]/div/div[1]/span[3]/ul/li/span[2]/span[1]/button",
    'scroll_down': "//*[@id='pane']/div/div[1]/div/div/div[2]/div[6]/div/div",
    'store_name': "//*[@id='pane']/div/div[2]/div/div/div[1]/div[3]/div[1]"
}


def back(driver, xpath):
    ele = driver.find_element_by_xpath(xpath)
    ele.click()
    sleep(WAIT_INTERVAL)


def scroll_down(driver):
    # find all comments
    element = driver.find_element_by_xpath(XPATH['scroll_down'])
    element.click() # use click to focus the position

    action = ActionChains(driver)

    while(1):
        src = driver.page_source
        for i in range(10):
            action.send_keys(Keys.SPACE).perform()
            sleep(SCROLL_PAUSE_TIME)

        # src not update anymore imply down to the last comment
        if len(src) == len(driver.page_source):
            break

def get_comments(src):
    # list all comments
    code = bs(src, "html.parser")
    cmts = []
    for (idx, item) in enumerate(code.findAll(attrs={'class': 'section-review-text'})):
        # only save valid comment
        if len(item.text) > 0:
            cmts.append("{0}".format(item.text))
    return cmts


def perform_comment(driver, res, search=True, store_name="", result_name=None):
    store_name = '  '.join(store_name.split('\n'))
    comment = driver.find_element_by_xpath(XPATH['comments'])
    #comment = driver.find_element_by_class_name('widget-pane-link')
    comment.click()
    sleep(WAIT_INTERVAL)

    print("searching... {}\n".format(store_name))
    scroll_down(driver)

    comment_src = driver.page_source
    # close the driver before parsing the source to save computing resource
    driver.close()
    print("searching {} finished\n".format(store_name))

    comments = get_comments(comment_src)
    res.append({store_name: comments})

    with open("{0}.txt".format("search_result" if result_name is None else result_name), mode="a") as fp:
        fp.write("###{0}###\n".format(store_name))
        for (idx, c) in enumerate(comments, 1):
            c = '\n\t'.join(c.split('\n'))
            fp.write("{0}.\n\t{1}\n".format(idx, c))
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
    ele = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.NAME, "q")))

    searchbox = driver.find_element_by_name('q')

    searchbox.clear()
    searchbox.send_keys(search_string)

    print("searching idx: %d"%idx)

    """
        this two line of code is equal to ```searchbox.send_keys(Keys.RETURN)```
    """
    searchbox_button = driver.find_element_by_class_name(
        "searchbox-searchbutton")
    searchbox_button.click()

    sleep(WAIT_INTERVAL)

    ele = driver.find_elements_by_class_name(
        "section-result-text-content")[idx]
    store_name = ele.text
    ele.click()
    sleep(WAIT_INTERVAL)

    perform_comment(driver, res, store_name=store_name,
                    result_name="{0}_{1}".format(store_name, idx))


def main(search_string=SEARCH_STRING):
    res = []
    threads = []

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://www.google.com.tw/maps")

    # wait for loading
    ele = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "searchboxinput")))

    searchbox = driver.find_element_by_id('searchboxinput')
    print(searchbox.get_attribute("type"))
    print(searchbox.text)

    searchbox.clear()
    searchbox.send_keys(search_string)
    """
        this two line of code is equal to ```searchbox.send_keys(Keys.RETURN)```
    """
    searchbox_button = driver.find_element_by_class_name(
        "searchbox-searchbutton")
    searchbox_button.click()

    sleep(WAIT_INTERVAL)

    # get the result tag
    eles = driver.find_elements_by_class_name("section-result-text-content")

    for i in range(len(eles)):
        res.append([])

        searchthread = Thread(target=crawl_handler,
                              args=(res[len(res)-1], i, search_string),
                              name="crawl thread_{0}".format(i))
        searchthread.setDaemon(1)
        threads.append(searchthread)
        searchthread.start()
        print("crawling thread_{0}  start".format(i))

        # limited total crawling threads
        while sum([1 if thread.isAlive() else 0 for thread in threads]) >= THREAD_LIMIT:
            continue

    # only a result or not found
    if len(eles) == 0:
        comment = None
        try:
            comment = driver.find_element_by_xpath(XPATH['comments'])
            #comment = driver.find_element_by_class_name('widget-pane-link')
        except:
            driver.close()
            print("Not find any of {}".format(search_string))
            print(driver.page_source)

        # store found
        if comment:
            perform_comment(driver, res, search=False,
                            store_name=search_string, result_name=search_string)
    else:
        driver.close()
        # wait until all thread finished
        while sum([1 if thread.isAlive() else 0 for thread in threads]) > 0:
            continue

    print("finished crawling")

if __name__ == '__main__':
    if len(argv) > 1:
        main(search_string=' '.join(argv[1:]))
    else:
        main()
