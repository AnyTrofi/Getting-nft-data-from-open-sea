import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import bs4
import csv
import json


def request(url):
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url=url)
    requiredHtml = browser.page_source
    soup = bs4.BeautifulSoup(requiredHtml, 'html.parser').text
    json_data = json.loads(soup)
    return json_data

# Request url / You can use any request
url = f'https://api.opensea.io/api/v1/assets?format=json&include_orders=false&limit=1&order_direction=desc'
print(request(url))