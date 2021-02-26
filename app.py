import requests
import logging
import datetime
import time
import json
from datetime import datetime
from bs4 import BeautifulSoup
from flask import Flask
app = Flask(__name__)

#Configure logger to log timestamp in the format of YY-MM-DD h:m:s
logging.basicConfig(filename='connection_data.log', format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

#Setting up config parser from a json file (config.json)
with open('config.json') as json_file:
    data = json.load(json_file)
#Get periodicity value from config.json
periodicity = data['app_variables']['periodicity']

def request_data():
    #Go through all key-value pairs
    for url, tag in data['websites_and_content_requirements'].items():
        try:
            #Send a get request to a server, stop attempt to contact it after 10 seconds
            response = requests.get(url, timeout = 10)
            #Perform the app's main logics if connection is established
            if response.ok:
                logging.info(f'Webpage {url} is accessible')
                list_logics_handler(url, tags, response)
        #Catch ConnectionError (which is what will happen if a website doesn't exist, for example) and show log message instead of an error message.
        except requests.exceptions.ConnectionError:
            logging.info(f'Attempt to connect to {url} failed. This website is either not accessible for some reason. No content requirement will be retrieved')

def list_logics_handler(url, tags, response):
    #Initialize html parser
    soup = BeautifulSoup(response.text, 'html.parser')
    #Check if tags variable is list, if so, run the content requirement checker for each tag separately 
    if(isinstance(tags, list)):
        for tag in tags:
            analyze_data(url, tag, soup)
    else:
        analyze_data(url, tags, soup)

def analyze_data(url, tags, soup):
    #Check for tags on one-by-one basis for each URL provided
    if len(soup.find_all(tags)) > 0:
        for tag_item in soup.find_all(tags):
            logging.info(f'Here is the {tag_item.name} tag for {url}: {tag_item.text}')
    else:
        logging.info(f'Either {tags} is not specified for {url} or attempt to retrieve {tags} tag has failed')

def time_tracker_wrapper():
    #Get current time at the start of the function
    start_time = datetime.now()
    #Run the request method which will run 
    request_data()
    #Get current time again after the function has been run, get the elapsed time and pretty print it
    logging.info(f'The response was processed in {str((datetime.now() - start_time).microseconds / 1000)} milliseconds')
    
@app.route('/')
def main():
    while True:
        time_tracker_wrapper()
        time.sleep(periodicity)


if __name__ == '__main__':
    main()
    #app.run()