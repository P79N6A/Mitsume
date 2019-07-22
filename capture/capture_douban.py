# encoding: utf-8
'''
@author: Beck.yang
@contact: wb-ysc255177@alibaba-inc.com
@file: capture_douban.py
@time: 2019-07-18 17:07
@desc: 
'''

import requests
from lxml import etree
from time import time
from threading import Thread
import gevent
from gevent import monkey
monkey.patch_all()

url ='https://movie.douban.com/top250'

def fetch_page(url):
    response = requests.get(url)
    return response

def fetch_content(url):
    response = fetch_page(url)
    page = response.content
    return page

def parse(url):
    page = fetch_content(url)
    html = etree.HTML(page)

    xpath_movie = '//*[@id="content"]/div/div[1]/ol/li'
    xpath_title = './/span[@class="title"]'
    xpath_pages = '//*[@id="content"]/div/div[1]/div[2]/a'

    pages = html.xpath(xpath_pages)
    fetch_list = []
    result = []

    for element_movie in html.xpath(xpath_movie):
        result.append(element_movie)

    for p in pages:
        fetch_list.append(url+p.get('href'))

    jobs = [gevent.spawn(fetch_content, url) for url in fetch_list]
    gevent.joinall(jobs)
    [job.value for job in jobs]

    for page in [job.value for job in jobs]:
        html = etree.HTML(page)
        for element_movie in html.xpath(xpath_movie):
            result.append(element_movie)


    for i, movie in enumerate(result, 1):
        title = movie.find(xpath_title).text

def main():
    from time import time
    start = time()
    parse(url)
    end = time()
    print ('Cost {} seconds'.format(end - start))

main()