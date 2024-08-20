import datetime
import json
import os
import uuid
import pandas as pd
from parsel import Selector
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_DB = os.getenv('MONGO_DB')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')
SCRAPER_API_KEY = os.getenv('SCRAPER_API_KEY')

def fetch_link():
    client = MongoClient(MONGO_HOST)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]

    all_data = collection.find({'status': None, 'quick_apply': False})
    for data in all_data:
        title = data['title']
        quick_p = data['quick_apply']
        if not quick_p:
            job_url = data['job_url']
            company_name = data['company_name']
            location = data['location']
            company_rating = data['company_rating']
            company_url = data['company_url']
            salary = data['salary']
            get_data(title, job_url, company_name, location, company_rating, company_url, salary)

def get_data(title, job_url, company_name, location, company_rating, company_url, salary):
    final_dir = f"D:\\Programming Laugages\\py-lear\\Simply_Hired\\page save 23_04_24\\"
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)
    page_path = final_dir + str(job_url).split('job/')[1].replace('-','_') + '.html'
    if not os.path.exists(page_path):
        while True:
            try:
                headers = {
                    # Your headers
                }
                response = requests.get(f'http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={job_url}', headers=headers)
                domss = Selector(response.text)
                json_path = domss.xpath('//script[@id="__NEXT_DATA__"]/text()').get('')
                json_data = json.loads(json_path)
                with open(page_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                break
            except Exception as e:
                pass
    else:
        with open(page_path, 'r', encoding='utf-8') as f:
            respon = f.read()
        domss = Selector(respon)
        json_path = domss.xpath('//script[@id="__NEXT_DATA__"]/text()').get('')
        json_data = json.loads(json_path)

    item = {}
    try:
        item['Quick Apply'] = json_data['props']['pageProps']['isIndeedApply']
    except:
        item['Quick Apply'] = ''
    try:
        item['Job_Title'] = title
    except:
        item['Job_Title'] = ''
    try:
        item['Company_Name'] = company_name
    except:
        item['Company_Name'] = ''
    try:
        item['Location'] = location
    except:
        item['Location'] = ''
    try:
        item['Company_URL'] = company_url
    except:
        item['Company_URL'] = ''
    try:
        item['Salary'] = salary
    except:
        item['Salary'] = ''
    try:
        item['Job_Type'] = ' | '.join(json_data['props']['pageProps']['jobTypes'])
    except:
        item['Job_Type'] = ''
    try:
        logo_url = json_data['props']['pageProps']['employerSquareLogoUrl']
    except:
        logo_url = ''
    if logo_url:
        try:
            random_id = uuid.uuid4()
            logo_request = requests.get(logo_url)
            with open(f'images/{random_id}.png', 'wb') as file:
                 file.write(logo_request.content)
        except Exception as e:
            print('Image Not Saved', e)
        try:
            item['Logo_ID'] = f'{random_id}.png'
        except:
            item['Logo_ID'] = ''
    else:
        try:
            item['Logo_ID'] = ''
        except:
            item['Logo_ID'] = ''
    try:
        datess = json_data['props']['pageProps']['datePublished']
        timestamp = datess / 1000
        date_time = datetime.datetime.fromtimestamp(timestamp)
        formatted_date_time = date_time.strftime('%Y-%m-%d')
        item['Date'] = formatted_date_time
    except:
        item['Date'] = ''
    try:
        item['Experience'] = ''
    except:
        item['Experience'] = ''
    try:
        item['Job Description '] = json_data['props']['pageProps']['jobDescriptionHtml']
    except:
        item['Job Description '] = ''
    try:
        item['Qualification'] = ' | '.join(json_data['props']['pageProps']['qualifications'])
    except:
        item['Qualification'] = ''
    try:
        data_col.insert_one(item)
        collection.update_many({'job_url': job_url},{'$set':{'status':'done'}})
        print('Inserted')
    except:
        pass

if __name__ == '__main__':
    client = MongoClient('mongodb://localhost:27017/')
    db = client['simpy_hires']
    collection = db['job_links_24_04_2024']
    data_col = db['job_data_24_04_2024']
    fetch_link()