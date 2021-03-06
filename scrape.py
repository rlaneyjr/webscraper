#!/usr/bin/env python
#title:             scrape.py
#description:       Scrape Any Website
#author:            Ricky Laney
#date:              20181215
#version:           0.1.0
#usage:             python scrape.py or ./scrape.py --class="MyClass" --id="MyID"
#notes:             Provide args to locate the class or id you are searching for.
#python_version:    3.6.5
#==============================================================================

import os
import sys
import requests
from bs4 import BeautifulSoup

BASE_URL1 = "https://en.wikipedia.org/wiki/List_of_dog_breeds"
BASE_URL2 = "https://en.wikipedia.org/wiki/List_of_cat_breeds"

base_page = requests.get(BASE_URL1)
base_soup = BeautifulSoup(base_page.content, 'html.parser')
table = base_soup.find('tbody')
table_rows = table.find_all('tr')
for row in table_rows:
    name = row.td

def input_base_url(url=None):
    if not url:
        url = input(f"Please enter your base URL: ")
        input_base_url(url)
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


def get_table_first_item(url):
    base_page = requests.get(url)
    base_soup = BeautifulSoup(base_page.content, 'html.parser')
    table = base_soup.find('table', attrs={'class': 'wikitable sortable jquery-tablesorter'})
    table_body = table.find('tbody')
    table_rows = table_body.find_all('tr')
    for name in table_rows.find_next_sibling('a'):
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

