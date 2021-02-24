# python_task

Prerequisites:

1. To run this app, you need ```python3``` installed. You will also most likely need ```pip``` or ```pip3``` installed.
2. Install ```BeatifulSoup4``` and ```requests``` modules via pip or pip3. Those are required dependencies.
3. Run ```python3  script.py``` from the root directory of a project.

Use of config file (config.json):

1. You can assign any integer number to ```periodicity``` variable, it reflects how often the whole script is run (in seconds).
2. 

How to read log:

1. ```tail -f -n *number of lines* connection_data.log``` - it will print the new data once it's in the log file
2. ```cat connection_data.log``` - it will not print the new data and you will need to rerun this command again