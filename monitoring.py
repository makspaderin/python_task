import json
import requests
import time
from tcp_latency import measure_latency

class MonitoredUrl:

    def __init__(self, url, latency, status, is_monitored):
        self.url = url #string
        self.latency = latency #float
        self.status = status #boolean
        self.is_monitored = is_monitored #boolean


try:
    with open('config.json') as json_file:
        data = json.load(json_file)
except json.decoder.JSONDecodeError:
    print("Config.json is broken. Please fix syntax errors")
    exit()
except FileNotFoundError:
    print("Config.json is missing. Please get it from GitHub repository or recreate it manually")
    exit()

def get_status(url):
    try:
        #Send a get request to a server, stop attempt to contact it after 10 seconds
        response = requests.get(url, timeout = 10)
        #Perform the app's main logics if connection is established
        if response.ok:
            return True
    #Catch ConnectionError (which is what will happen if a website doesn't exist, for example) and show log message instead of an error message.
    except requests.exceptions.ConnectionError:
        return False

def output():
    for url, tag in data['websites_and_content_requirements'].items():
        if (get_status(url)):
            latency = measure_latency(host=url, port=80)
            MonitoredUrl(url, latency, True, True)
            print(f"Server hosting {url} is up, latency to it is {latency}")
        else:
            MonitoredUrl(url, 0, False, True)
            print(f"Server hosting {url} is down")

def main():
    while True:
        output()
        time.sleep(3)


if __name__ == '__main__':
    main()