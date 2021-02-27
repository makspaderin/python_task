# python_task

Prerequisites and basic instructions:

1. To run this app, you need ```python3``` installed. It should be installed by default on Unix systems, on Windows you can find it in Microsoft Store (download Python 3.9). The app can also theoretically run on older Python versions, but I would not recommend trying that (I believe that .items() is supported only in python3). You will also most likely need ```pip``` or ```pip3``` to install new modules.
2. Install ```BeatifulSoup4```, ```flask``` and ```requests``` modules via pip or pip3. Those are required dependencies. This is usually done via ```pip install *modulename*``` or ```pip3 install *modulename*```
3. Run ```python3  script.py``` from the root directory of a project. I will recommend using ```tail``` command (check the third part of this Readme) from the last part of the Readme in the second Terminal window, so you will have app running in one window and log will automatically update in the other.
4. App is basically in endless loop and will run forever, but can be interrupted via simple keyboard interrupt, so you can just Ctrl+C and run command again once you want to test some changes
5. Log is not self-cleaning and will contain all output from previous script launches, but you can just delete the logfile and app will recreate it in empty state on next launch.

Use of config file (config.json):

1. You can assign any integer number to ```periodicity``` variable, it reflects how often the whole script is run (in seconds).
2. You can provide a website (including specific webpage) and desired content requirements (aka tag(s)) to check for within this website. The app will log all the occurances of those tags on the webpage provided.
3. You can also provide a non-existing website, and it should return a log message, not break the app.
4. 

How to read log on UNIX systems (Linux, MacOS) or with UNIX terminals emulators for Windows (e.g. Git Bash):

1. ```tail -f -n *number of lines* connection_data.log``` - it will print the new data once it's in the log file
2. ```cat connection_data.log``` - it will not print the new data and you will need to rerun this command again

Possible  outputs:

1. The website is not accessible:
- ```Attempt to connect to *website url* failed. This website is either not accessible for some reason. No content requirement will be retrieved```
2. The website is accessible but tag is not for some reason (e.g. happens on Twitter with at least "title", I don't know the exact reason, maybe some sort of ddos protection attack against those automated get requests?), or the tag is missing:
- ```Webpage *website url* is accessible```
-  ```Either title is not specified for https://twitter.com or attempt to retrieve title tag has failed```
3. Both website and tag are accessible
- ```Webpage *website url* is accessible```
- ```Here is the title tag for *website url*: *tag text*```
4. Independently on cases 1, 2 and 3, it will produce ```The response was processed in *elapsed time* milliseconds```
5. If the periodicity value is invalid, it will immediately stop the app's execution and will print you the reason to the console

Possible optimization of elapsed time:
1. Everything regarding validating periodicity can be removed. The app will show exception for anything except positive floats and integers in that case, though.

Some justifications:

1. Why I use both time and datetime? It was easier to implement periodic checking via ```time.sleep()``` and more elegant to implement elapsed time tracker via *timedelta*, which is a part of *datetime*
2. Why is config file in .json format? I tried both .ini and .json and found json solution to be much more elegant, so I went with it. I also feel like json is more of a "modern solution"
3. Why I made periodicity variable foolproof? So the app doesn't run into exceptions on invalid values and also could handle "digit strings"
4. Why I always convert periodicity variable to float? Because float is more precise, and for this sort of task difference in performance is miniscule. Integer can easily be represented as float anyway.