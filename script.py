import requests, threading, configparser, logging, datetime, time
from datetime import datetime
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read('config.ini')
periodicity = config.getint('variables', 'Periodicity')

def url_request():
    start_time = datetime.now()
    #Runs monitoring function with set periodicity
    #threading.Timer(periodicity, monitoring).start()
    #testURL
    url = 'https://google.fi'

    logging.basicConfig(filename='connection_data.log', format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    #open with GET method
    response = requests.get(url)

    #checker
    if response.ok:
        logging.info('Web page ' + url + ' is accessible')
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.find_all('meta', {'name':'description'}):
            logging.info('Here is the meta tag info: ' + item['content']) if item else 'Meta tag is not specified'
    else:
        logging.info('The website ' + url + ' is not accessible')

    logging.info('The response was processed in ' + str((datetime.now() - start_time).microseconds / 1000) + ' milliseconds')

while True:
    url_request()
    time.sleep(periodicity)