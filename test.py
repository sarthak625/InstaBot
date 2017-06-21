from KEYS import GOOGLE_API_KEY
import requests

addr = raw_input("Enter the address: ")
addr = addr.replace(' ','+')
GOOGLE_BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address='+addr+'&key='+GOOGLE_API_KEY
coordinates = requests.get(BASE_URL).json()
latitude = coordinates['results'][0]['geometry']['location']['lat']
longitude = coordinates['results'][0]['geometry']['location']['lng']
print latitude
print longitude
print GOOGLE_BASE_URL