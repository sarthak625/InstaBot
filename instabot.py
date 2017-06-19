from KEYS import ACCESS_TOKEN
import requests

BASE_URL = 'https://api.instagram.com/v1/'

#username for which you want to perform any of the action
#user_name = raw_input("Enter the user")

#A function declaration to fetch user's self details
def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (ACCESS_TOKEN)
    my_info = requests.get(request_url).json()
    print "Profile"
    print "========================================="
    print 'Name --> '+my_info['data']['full_name']
    print 'Bio --> '+my_info['data']['bio']


self_info()