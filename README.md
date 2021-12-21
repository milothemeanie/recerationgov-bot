# recerationgov-bot 
## Introduction
This script is design to go to recreation.gov and then books the first campsite it finds on a given campsite for a given date range.
If the campsite is not available it will wait for a configurable amount of time before it refreshes to see if the site has become
available. The script starts by going to recreation.gov and login by configured username password. Then it will navigate to the configured
campsite and tranverse the availability table until the configured dates are visible. The table will be refreshed until the script is stopped or 
the desired dates are available. If the dates become available then the date boxes are selected and then added to the cart. 
At this point the automation is not running and the user will need to take control to finish the booking. 

## Installation 
* [Install python](https://www.python.org/downloads) 
* Download necessary packages ```pip install -r requirements.txt```
* Download [chrome webdriver](https://chromedriver.chromium.org/downloads)
  * Match the version of your chrome that is seen in chrome's Help->About Chrome
  * Unzip and place the exectuable to a location of your choosing

## Configuration
Currently all configurable properties are located at the top of the script file [main.py](main.py). Below is the list of all the configurable properties

Config Name | Example | Description
--- | -- | ---
WEB_DRIVER_EXEC | C:\Users\Downloads\chromedriver.exe | Absolute path to the location of the chrome web driver 
USER_NAME | cward | The recreation.gov account's username
PASSWORD | password1 | The recreation.gov account's password
CAMP_GROUND_URL | https://www.recreation.gov/camping/campgrounds/233543 | Full url of the desired campsite to book
START_DATE | 06/08/2022 | Start date of desired booking in *MM/DD/YYYY* format
END_DATE | 06/12/2022 | End date of desired booking in *MM/DD/YYYY* format
POLL_SPEED_SEC | .5 | Poll interval in seconds when refresing the availability table
TIME_ADD_CART | 7:00 | Wait until this time has passed before clicking add to cart

## Run
```python main.py```
