import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import bs4
import csv
import json


def request(continuation):
    global writer, total_nfts_was_founded, browser
    url = f'https://api.opensea.io/api/v1/assets?cursor={continuation}&format=json&include_orders=false&limit=200&order_direction=desc'
    browser.get(url=url)
    requiredHtml = browser.page_source
    soup = bs4.BeautifulSoup(requiredHtml, 'html.parser').text
    json_data = json.loads(soup)
    if 'assets' in json_data.keys():
        nfts = json_data['assets']
        continuation = json_data['next']
        for nft in nfts:
            if nft['image_url'] != None:
                writer.writerow((
                    nft['id'],
                    nft['image_url'],
                    nft['asset_contract']['name'],
                    nft['asset_contract']['address'],
                    nft['asset_contract']['owner'],
                    nft['permalink'],
                    nft['token_id'],
                    ))
                total_nfts_was_founded += 1
        print(f"{total_nfts_was_founded} nfts was founded")
        return continuation


browser = webdriver.Chrome(ChromeDriverManager().install())
csvfile = open("database.csv", "a")
writer = csv.writer(csvfile)
writer.writerow(('id', 'image_url', 'name', 'address', 'owner', 'permalink', 'token_id'))
total_nfts_was_founded = 0
continuation = ""

while continuation != None:
	try:
		continuation = request(continuation)
	except:
		time.sleep(5)
		browser = webdriver.Chrome(ChromeDriverManager().install())
