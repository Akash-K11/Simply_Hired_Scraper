import os
import requests
import json
from parsel import Selector
from pymongo import MongoClient
from urllib.parse import unquote
from dotenv import load_dotenv

load_dotenv()

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_DB = os.getenv('MONGO_DB')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')
SCRAPER_API_KEY = os.getenv('SCRAPER_API_KEY')

def get_cat():
    lists = ['Z']
    for lis in lists:
        while True:
            try:
                headers = {
                    # Your headers
                }
                response = requests.get(f'http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url=https://www.simplyhired.co.in/browse-jobs/titles/{lis}', headers=headers)
                dom = Selector(response.text)
                json_path = dom.xpath('//script[@id="__NEXT_DATA__"]/text()').get('')

                if response.status_code == 200:
                    directory = f"D:\\Programming Laugages\\py-lear\\Simply_Hired\\page save\\{lis}\\"
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    HTML_Save_Path1 = directory + f"{lis}_" + ".json"
                    f = open(HTML_Save_Path1, 'w+', encoding='utf-8')
                    f.write(response.text)
                    f.close()

                json_data = json.loads(json_path)
                break
            except Exception as e:
                pass
        all_data = json_data['props']['pageProps']['letterData']['externalContents']
        for data in all_data:
            link__ = data['externalLink']
            quary = data['title']
            build_id = json_data['buildId']
            get_links(link__, quary, build_id,lis)

def get_links(link__, quary, build_id, lis):
    page = 2

    while True:
        try:
            headers = {
                # Your headers
            }
            response = requests.get(f'http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url=https://www.simplyhired.co.in/_next/data/{build_id}/en-IN/search.json?{link__.split("?")[1]}', headers=headers)
            respo = response.text

            try:
                if response.status_code == 200:
                    directory = f"D:\\Programming Laugages\\py-lear\\Simply_Hired\\page save\\{lis}\\"
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    HTML_Save_Path1 = directory + f"{quary}_{page}" + ".json"
                    f = open(HTML_Save_Path1, 'w+', encoding='utf-8')
                    f.write(response.text)
                    f.close()

            except Exception as e:
                print(e)
                pass

            json_data = json.loads(respo)
            break
        except Exception as e:
            pass
    all_data = json_data['pageProps']['jobs']
    for data in all_data:
        item = {}
        # Extract and store job data
        # ...
        client = MongoClient(MONGO_HOST)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        collection.create_index('job_url', unique=True)
        try:
            print(item)
            collection.insert_one(item)
        except:
            print("duplicate")
            pass
    else:
        try:
            cursor = json_data['pageProps']['pageCursors'][f'{str(page)}']
            next_page(cursor, page, quary, build_id, link__, lis)
        except:
            pass

def next_page(cursor, page, quary, build_id, link__, lis):
    page += 1
    while True:
        try:
            headers = {
                # Your headers
            }
            response = requests.get(f'http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url=https://www.simplyhired.co.in/_next/data/{build_id}/en-IN/search.json?{link__.split("?")[1]}&cursor={cursor}', headers=headers)
            json_data = json.loads(response.text)

            try:
                if response.status_code == 200:
                    directory = f"D:\\Programming Laugages\\py-lear\\Simply_Hired\\page save\\{lis}\\"
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    HTML_Save_Path1 = directory + f"{quary}_{page}" + ".json"
                    f = open(HTML_Save_Path1, 'w+', encoding='utf-8')
                    f.write(response.text)
                    f.close()

            except Exception as e:
                print(e)
                pass

            break
        except Exception as e:
            pass
    all_data = json_data['pageProps']['jobs']
    for data in all_data:
        item = {}
        # Extract and store job data
        # ...
        client = MongoClient(MONGO_HOST)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        collection.create_index('job_url', unique=True)
        try:
            print(item)
            collection.insert_one(item)
        except:
            print("duplicate")
            pass
    else:
        try:
            if not page == 3:
                cursor = json_data['pageProps']['pageCursors'][f'{str(page)}']
                next_page(cursor, page, quary, build_id, link__, lis)
            else:
                pass
        except Exception as e:
            print('Error', e)

if __name__ == '__main__':
    get_cat()