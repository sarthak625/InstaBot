# InstaBot
A bot app using python that allows you to use the various features of the Instagram API.

## Features
* Get images between certain geographical coordinates, analyse the caption and determine if it is about a natural calamity such as earthquake, floods etc using the google maps API.
* Like and comment on posts.
* Read user profiles.
* Search for the recent media by the user by its caption or by the number of likes.
* Download posts from Instagram.

# Installation

* Create a KEYS.py file with the variables ACCESS_TOKEN and GOOGLE_API_KEY. You can generate these by following the methods below:

### Generate ACCESS TOKEN
* Goto https://instagram.com/developer
* Click on Manage Clients tab in the header.
* If not already logged in, login in using your existing instagram account.
* Click on Register a new client, the green colored button just below the header on the right.

### Generate GOOGLE_API_KEY
* Go to https://developers.google.com/maps/documentation/geocoding/start and click on GET A KEY

### REQUIRED LIBRARIES

> pip install requests

> pip install urllib2
