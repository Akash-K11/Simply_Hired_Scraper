import numpy as np
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_DB = os.getenv('MONGO_DB')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')

client = MongoClient(MONGO_HOST)
db = client[MONGO_DB]
data_col = db[MONGO_COLLECTION]

cursor = data_col.find()
df = pd.DataFrame(list(cursor))

xlsx_file = 'output.xlsx'
df.to_excel(xlsx_file, index=False)

print(f"Data exported successfully to {xlsx_file}.")