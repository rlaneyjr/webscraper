#!/usr/bin/env python
#title:             scrape.py
#description:       Scrape Mostly Mutts - https://www.mostlymutts.org
#author:            Ricky Laney
#date:              20181215
#version:           0.1.0
#usage:             python scrape.py or ./scrape.py
#notes:             Grab urls from menu items to recurse. Saves main content text from each page.
#python_version:    3.6.5
#==============================================================================

import os
import sys
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.mostlymutts.org"


def input_base_url():
    url = input(f"Please enter your base URL or hit enter for the default \
                 ({BASE_URL}): ")
    if not url:
        return BASE_URL
    elif url.startswith('http://') or url.startswith('https://'):
        return url
    else:
        print(f"It looks like you did not enter a valid URL: {url}.\n \
               Hint: Make sure to enter the http:// or https:// for valid \
               URL.\nPlease try again.")
        input_base_url()


def make_dirs():
    if 'content' in os.scandir():
        os.rmdir('content')
    os.mkdir('content')
    if 'all_text' in os.scandir():
        os.rmdir('all_text')
    os.mkdir('all_text')


def get_urls(url):
    base_page = requests.get(url)
    base_soup = BeautifulSoup(base_page.content, 'html.parser')
    menu = base_soup.find('ul', attrs={'class': 'menu'})
    urls = []
    for link in menu.find_all('a'):
        ref = link.get('href')
        if ref.startswith('/') and ref != "/":
            urls.append(ref)
    return urls


def write_all_text(urls):
    for url in urls:
        page = requests.get(BASE_URL + url)
        soup = BeautifulSoup(page.content, 'html.parser')
        text_file = url.lstrip('/').replace('/', '_') + '.txt'
        text_file = os.path.join('all_text', text_file)
        with open(text_file, 'w') as tfile:
            for s in soup.body.stripped_strings:
                tfile.write(f"{s}\n")



def write_content(urls):
    for url in urls:
        page = requests.get(BASE_URL + url)
        soup = BeautifulSoup(page.content, 'html.parser')
        text_file = url.lstrip('/').replace('/', '_') + '_content.txt'
        text_file = os.path.join('content', text_file)
        with open(text_file, 'w') as tfile:
            for i in soup.body('p'):
                if i.find_next_sibling('strong'):
                    line = f"{i.text} {i.nextSibling.text}"
                else:
                    line = f"{i.text}"
                tfile.write(f"{line}\n")



if __name__ == '__main__':
    print("Please make sure you are in a empty directory.")
    print("This program will create and delete the directories 'content' and 'all_text'")
    if input("To continue type 'y' and hit enter: ") == 'y':
        url = input_base_url()
        make_dirs()
        urls = get_urls(url)
        write_all_text(urls)
        write_content(urls)
    else:
        sys.exit(1)

