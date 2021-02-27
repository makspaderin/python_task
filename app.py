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
try:
    with open('config.json') as json_file:
        data = json.load(json_file)
except json.decoder.JSONDecodeError:
    print("Config.json is broken. Please fix syntax errors.")
    exit()
except FileNotFoundError:
    print("Config.json is missing. Please get it from GitHub repository or recreate it manually.")
    exit()
#Get periodicity value from config.json
periodicity = data['app_variables']['periodicity']

def request_data():
    #Go through all key-value pairs
    for url, tags in data['websites_and_content_requirements'].items():
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

def time_tracker_wrapper(validation_time):
    #Get current time at the start of the function
    start_time = datetime.now()
    #Run the request method which will run 
    request_data()
    #Get current time again after the function has been run, get the elapsed time and pretty print it
    logging.info(f'The response was processed in {str((datetime.now() - start_time + validation_time).microseconds / 1000)} milliseconds')

#Helper method that will check if periodicity value is a number, and if not, if it can be safely converted to number
def validate(periodicity):
    #If periodicity is a string, check if it is an string convertible to integer or float, then make it float
    if (isinstance(periodicity, int) or isinstance(periodicity, float)):
        stop_if_negative(periodicity)
        return periodicity
    elif (isinstance(periodicity, str)):
        if (periodicity.isdigit() or is_float(periodicity)):
            periodicity = float(periodicity)
            stop_if_negative(periodicity)
            return periodicity
        else:
            print('The value you provided for periodicity variable is invalid: it is a string that cannot be represented as a number')
            exit()
    else:
        print('The value you provided for periodicity variable is invalid: it can be only a number or a string that can be represented as a number')
        exit()

#Method that will stop the app's execution if number is either zero or negative
def stop_if_negative(number):
    if (float(periodicity) <= 0):
        print('The value you provided for periodicity variable is invalid: it cannot be neither a negative number nor a zero')
        exit()

#Helper method to check if number is a float
def is_float(number):
    try:
        float(number)
        return True
    except:
        return False
    
@app.route('/')
def main():
    start_time = datetime.now()
    validated_periodicity = validate(periodicity)
    elapsed_validation_time = (datetime.now() - start_time)
    while True:
        time_tracker_wrapper(elapsed_validation_time)
        time.sleep(validated_periodicity)


if __name__ == '__main__':
    main()
    #app.run()