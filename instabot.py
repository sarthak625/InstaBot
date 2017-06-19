from KEYS import ACCESS_TOKEN
import requests
import sys

# -- Global Variables
BASE_URL = 'https://api.instagram.com/v1/'


# -- Functions
# To fetch user's self details
def self_info():
    print "Profile"
    print "========================================="
    print 'Name --> '+my_info['data']['full_name']
    print 'Bio --> '+my_info['data']['bio']

# To get another user's id
def user_info(user_name):
    print "Searching for "+user_name
    print "========================================="
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s')%(user_name,ACCESS_TOKEN)
    user_details = requests.get(request_url).json()
    try:
        user_id = user_details['data'][0]['id']
        return user_id
    except IndexError:
        return -1


# To get public posts of self
def get_recent_post_id():
    request_url = (BASE_URL+ 'users/self/media/recent/?access_token=%s')%(ACCESS_TOKEN)
    public_posts = requests.get(request_url).json()
    return public_posts['data'][0]['id']
    #request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s')%(my_info['data']['id'],ACCESS_TOKEN)


# -- Main

print "Logging you in"
request_url = (BASE_URL + 'users/self/?access_token=%s') % (ACCESS_TOKEN)
my_info = requests.get(request_url).json()
# Print user's details
self_info()

# User for which an action has to be performed
user_name = raw_input("Enter a username: ")

# Options
while True:
    print "What do you want to do with "+user_name

    # Searches for the user name within your sandbox
    id = user_info(user_name)
    if id == -1:
        print "The username could not be found. Please try Again: "
        break
    print "1. Like a post"
    print "2. Comment on a post"
    print "9. Exit"
    try:
        choice = int(raw_input("Enter your choice: "))
        if (choice == 9):
            print "The application will now terminate! Bbyee!!!"
            sys.exit()

    except ValueError:
        print "Not a valid choice. Please enter a number as your choice."
        raw_input("")