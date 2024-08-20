# Simply Hired Scraper

This project is a Python-based web scraper that extracts job data from the Simply Hired website. The scraper collects information such as job titles, company names, job descriptions, and more, and stores the data in a MongoDB database.

## Features
- Scrapes job listings from the Simply Hired website
- Saves job data to a MongoDB database
- Handles pagination and multiple pages of job listings
- Saves HTML pages for offline analysis
- Exports job data to an Excel file

## Requirements
- Python 3.x
- MongoDB
- Required Python packages listed in `requirements.txt`

## Installation
1. Clone the repository:
```
git clone https://github.com/your-username/Simply_Hired_Scraper.git
```
2. Install the required packages:
```
pip install -r requirements.txt
```
3. Create a `.env` file in the root directory of the project and add the following content:
```
MONGO_HOST=mongodb://localhost:27017/
MONGO_DB=simpy_hires
MONGO_COLLECTION=job_data_24_04_2024
SCRAPER_API_KEY=<YOUR_SCRAPER_API_KEY>
```
4. Replace `<YOUR_SCRAPER_API_KEY>` with your actual Scraper API key.
5. Run the scraper:
```
python get_data.py
```
6. Export the data to an Excel file:
```
python export.py
```

## Usage
The scraper has two main components:
1. `get_data.py`: This script handles the web scraping process, collecting job data and saving it to the MongoDB database.
2. `export.py`: This script exports the job data from the MongoDB database to an Excel file.

You can run these scripts separately or together to scrape and export the data.
