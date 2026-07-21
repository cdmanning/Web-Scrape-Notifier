import time
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from message import send_alert

load_dotenv()

def load_config(filepath="config.json"):
    with open(filepath, 'r') as file:
        return json.load(file)

def check_stock(target):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(target['url'], headers=headers, timeout=10)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find_all(target['element_tag'], class_=target.get('element_class', ''))
        if target['target_text'] not in str(data):
            return f"Alert triggered for: {target['name']} - {target['url']}"
    except requests.exceptions.RequestException as e:
        print(f"Error checking {target['name']}: {e}")
    return None

def main():
    config = load_config()
    current_time = time.ctime()
    print(f"[{current_time}] Checking targets for changes...")
    in_stock_alerts = []
    for target in config['targets']:
        result = check_stock(target)
        if result:
            in_stock_alerts.append(result)
    if in_stock_alerts:
        body = "\n".join(in_stock_alerts)
        print(f"Items found! Sending alert...\n{body}")
        send_alert("Web Scraper Alert!", body)
    else:
        print("No changes detected.")

if __name__ == '__main__':
    main()