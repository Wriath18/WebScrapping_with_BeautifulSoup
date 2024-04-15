import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

def scrape_website(website_url):
    try:
        response = requests.get(website_url)
        bs = BeautifulSoup(response.content, 'html.parser')
        text = bs.get_text()
        img_arr = []
        for img in bs.find_all('img'):
            src = img.get('src')
            if src:
                if src.startswith('http'):
                    img_arr.append(src)
                else:
                    img_url = urljoin(website_url, src)
                    img_arr.append(img_url)
        link_arr = []
        if bs.find('a', href=True):
            link_arr = [l['href'] for l in bs.find_all('a', href=True)]
        return {
            "Website_url": website_url,
            "Text": text,
            "Images": img_arr,
            "Links": link_arr
        }
    except Exception as e:
        print(f"Error scraping {website_url}: {e}")
        return None

def process_website_links(excel_file):
    try:
        df = pd.read_excel(excel_file, header=None)
        extracted_data = []

        for index, row in df.iterrows():
            url = row[0]
            data = scrape_website(url)
            if data:
                extracted_data.append(data)

        return extracted_data
    except Exception as e:
        print(f"Error processing links: {e}")
        return None

def save_as_json(data, output_path):
    try:
        with open(output_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {output_path}")
    except Exception as e:
        print(f"Error saving data to JSON file: {e}")

if __name__ == "__main__":
    excel_file = r"D:\Programming-1\Scraping_using_BS\Scrapping Python Assigment- Flair Insights.xlsx"
    scrapped_data = process_website_links(excel_file=excel_file)
    output_file = "scrapped_data.json"
    if scrapped_data:
        save_as_json(scrapped_data, output_file)
