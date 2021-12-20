# recerationgov-bot 
## Introduction
This script is design to go to recreation.gov and then books the first campsite it finds on a given campsite for a given date range.
If the campsite is not available it will wait for a configurable amount of time before it refreshes to see if the site has become
available. The script starts by going to recreation.gov and login by configured username password. Then it will navigate to the configured
campsite and tranverse the availability table until the configured dates are visible. The table will be refreshed until the script is stopped or 
the desired dates are available. If the dates become available then the date boxes are selected and then added to the cart. 
At this point the automation is not running and the user will need to take control to finish the booking. 

## Installation 
* Download necessary packages ```pip install -r requirements.txt```
* Download [chrome webdriver](https://chromedriver.chromium.org/downloads)
  * Match the version of your chrome
  * Unzip and place the exectuable to a location of your choosing
