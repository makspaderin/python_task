# python_task

Prerequisites and basic instructions:

1. To run this app, you need ```python3``` installed. It can also theoretically run on older Python versions, but I would not recommend trying that (I believe that .items() is supported only in python3). You will also most likely need ```pip``` or ```pip3``` to install new modules.
2. Install ```BeatifulSoup4``` and ```requests``` modules via pip or pip3. Those are required dependencies. This is usually done via ```pip install modulename``` or ```pip3 install modulename```
3. Run ```python3  script.py``` from the root directory of a project. I will recommend using ```tail``` command from the last part of the Readme in the second Terminal window, so you will have app running in one window and log will automatically update in the other.
4. App is basically in endless loop and will run forever, but can be interrupted via simple keyboard interrupt, so you can just Ctrl+C and run command again once you want to test some changes

Use of config file (config.json):

1. You can assign any integer number to ```periodicity``` variable, it reflects how often the whole script is run (in seconds).
2. You can provide a website (including specific webpage) and desired tag(s) to check for within this website. The app will log all the occurances of those tags on the webpage provided.
3. You can also provide a non-existing website, and it should return a log message, not break the app.
4. Log is not self-cleaning and will contain all output from previous script launches, but you can just delete the logfile and app will recreate it in empty state on next launch.

How to read log on UNIX systems (Linux, MacOS) or with UNIX terminals emulators for Windows (e.g. Git Bash):

1. ```tail -f -n *number of lines* connection_data.log``` - it will print the new data once it's in the log file
2. ```cat connection_data.log``` - it will not print the new data and you will need to rerun this command again