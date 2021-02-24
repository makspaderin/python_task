import requests
import logging
import datetime
import time
import json
from datetime import datetime
from bs4 import BeautifulSoup

#Configure logger to log timestamp
logging.basicConfig(filename='connection_data.log', format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

#Setting up config parser
with open('config.json') as json_file:
    data = json.load(json_file)
periodicity = data['variables']['periodicity']

def time_tracker_wrapper():
    start_time = datetime.now()
    get_request()
    logging.info(f'The response was processed in {str((datetime.now() - start_time).microseconds / 1000)} milliseconds')

def get_request():

    for url, tag in data['website_list'].items():
        #open with GET method
        response = requests.get(url, timeout = 60)
        
        #checker
        if response.ok:
            logging.info(f'Web page {url} is accessible')
            soup = BeautifulSoup(response.text, 'html.parser')
            for item in soup.find_all(tag):
                if tag is not None:
                    logging.info(f'Here is the {tag} tag info: {item.text}')
                else:
                    logging.info(f'{tag} is not specified for {url}')
        else:
            logging.info(f'The website {url} is not accessible')
    

def main():
    while True:
        time_tracker_wrapper()
        time.sleep(periodicity)


if __name__ == '__main__':
    main()