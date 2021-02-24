import requests
import logging
import datetime
import time
import json
from datetime import datetime
from bs4 import BeautifulSoup

#Configure logger to log timestamp in the format of YY-MM-DD h:m:s
logging.basicConfig(filename='connection_data.log', format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

#Setting up config parser
with open('config.json') as json_file:
    data = json.load(json_file)
periodicity = data['app_variables']['periodicity']

def request_data():
    #Go through all key-value pairs
    for url, tag in data['websites_and_content_requirements'].items():
        try:
            #Send a get request to a server, stop attempt to contact it after 10 seconds
            response = requests.get(url, timeout = 10)
            if response.ok:
                logging.info(f'Web page {url} is accessible')
                analyze_data(url, tag, response)
        except requests.exceptions.ConnectionError:
            logging.info(f'Attempt to connect to {url} produced a connection error. This website is either not accessible or does not exist. No content requirement will be retrieved')

def analyze_data(url, tag, response):
    #Initialize html parser
    soup = BeautifulSoup(response.text, 'html.parser')
    for item in soup.find_all(tag):
        if tag != 0:
            logging.info(f'Here is the {tag} tag for {url}: {item.text}')
        else:
            logging.info(f'Either {tag} is not specified for {url} or attempt to retrieve {tag} tag has failed')

def time_tracker_wrapper():
    start_time = datetime.now()
    request_data()
    logging.info(f'The response was processed in {str((datetime.now() - start_time).microseconds / 1000)} milliseconds')
    

def main():
    while True:
        time_tracker_wrapper()
        time.sleep(periodicity)


if __name__ == '__main__':
    main()