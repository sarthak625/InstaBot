from KEYS import ACCESS_TOKEN
import requests
import sys
import urllib2
import urllib

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
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s')%(user_name,ACCESS_TOKEN)
    user_details = requests.get(request_url).json()
    try:
        user_id = user_details['data'][0]['id']
        return user_id
    except IndexError:
        return -1


# To fetch public posts of self
def get_recent_post_id():
    request_url = (BASE_URL+ 'users/self/media/recent/?access_token=%s')%(ACCESS_TOKEN)
    public_posts = requests.get(request_url).json()
    return public_posts['data'][0]['id']

# To fetch another user's public posts
def get_recent_post_id_user(user_name):
    user_id = user_info(user_name)
    print user_id
    try:
        request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s')%(user_id,ACCESS_TOKEN)
        public_posts = requests.get(request_url).json()
        return public_posts['data'][0]['id']
    except:
        print "You are not allowed to view the post of this user. This is probably because this account is private."
        return -1;


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
    # Searches for the user name within your sandbox
    id = user_info(user_name)
    print "Searching for " + user_name
    print "========================================="
    if id == -1:
        print "The username could not be found. Please try Again: "
        break

    print "What do you want to do with " + user_name
    print "1. Like a post"
    print "2. Comment on a post"
    print "8. Get most recent post id"
    print "9. Exit"
    try:
        choice = int(raw_input("Enter your choice: "))
        if (choice == 9):
            print "The application will now terminate! Bbyee!!!"
            sys.exit()
        if choice == 8:
            recent_id = get_recent_post_id_user(user_name)
            if recent_id!=-1:
                # If the recent post can be acquired, then download it
                req = (BASE_URL + 'media/%s?access_token=%s')%(recent_id,ACCESS_TOKEN)
                recent_post = requests.get(req).json()
                url = recent_post['data']['images']['standard_resolution']['url']
                #Download the post
                f = urllib2.urlopen(url)
                file_name = url.split('/')[-1]
                with open(file_name, "wb") as code:
                    code.write(f.read())

    except ValueError:
        print "Not a valid choice. Please enter a number as your choice."
        raw_input("")