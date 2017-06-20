from KEYS import ACCESS_TOKEN
import requests
import sys
import urllib2
import traceback

# -- Global Variables
#=====================================================

BASE_URL = 'https://api.instagram.com/v1/'


# -- Functions
#=====================================================

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

# To download a post by its id
def download_post(media_id):
	request_url = (BASE_URL + 'media/%s?access_token=%s') % (media_id, ACCESS_TOKEN)
	recent_post = requests.get(request_url).json()
	url = recent_post['data']['images']['standard_resolution']['url']

	# Download the post
	f = urllib2.urlopen(url)
	file_name = url.split('/')[-1]
	with open(file_name, "wb") as code:
		code.write(f.read())
	raw_input("The image has been downloaded. Press enter to continue. ")

# To fetch public posts of self
def get_recent_post_id():
	request_url = (BASE_URL+ 'users/self/media/recent/?access_token=%s')%(ACCESS_TOKEN)
	public_posts = requests.get(request_url).json()
	
	id = public_posts['data'][0]['id']
	try:
		id = search_specific_criteria(id,public_posts)
	except Exception:
		print traceback.format_exc()
		
	if id == -1:
		return -1
	prompt = raw_input("Do you want to download your most recent post? Press y/n: ")
	if prompt.lower() == 'y':
		download_post(id)
	return public_posts['data'][0]['id']


# To search for a specific criteria in the posts
def search_specific_criteria(recent_id,public_posts):
	specific_criteria = raw_input("Press y to search for a specific post based on a criteria. ")
		
	if specific_criteria.lower() == 'y':
		while True:
			print "What criteria are you looking for: "
			print "a. Least Number of likes"
			print "b. Search for a post with a specific caption."
			choice = raw_input("Enter your choice: ")
			
			# Search for the post with the fewest likes					
			if choice == 'a':
				least = 100000000000
				for post in public_posts['data']:
					if least > post['likes']['count']:
						least = post['likes']['count']
						recent_id = post['id']
				break; 
		
			# Search for the post with a specific caption
			elif choice == 'b':
				caption = raw_input("Enter the caption you are looking for: ")
				found = False
				
				for post in public_posts['data']:
					if post['caption'] != None:
						if caption.lower() in post['caption']['text'].lower():
							recent_id = post['id']
							found = True
							break			
				if found == False:
					raw_input('The image with that caption could not be found. Press enter to continue.')
					return -1

				break;
			else:
					raw_input("Enter a choice alphabet. eg. a or b . Press enter to try again!")

	return recent_id 

# To get recent media liked by the user
def recent_media_liked():
	request_url = (BASE_URL + 'users/self/media/liked?access_token=%s')%(ACCESS_TOKEN)
	media = requests.get(request_url).json()
	prompt = raw_input("Do you want to download your most recently liked post? Press y/n: ")
	id = media['data'][0]['id']
	if prompt.lower() == 'y':
		download_post(id)
	return id

# To fetch another user's public posts
def get_recent_post_id_user(user_name):
	user_id = user_info(user_name)
	print user_id
	try:
		request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s')%(user_id,ACCESS_TOKEN)
		public_posts = requests.get(request_url).json()
		recent_id = public_posts['data'][0]['id']
		
		try:
			recent_id = search_specific_criteria(recent_id,public_posts)
		except Exception:
			print traceback.format_exc()
		
		if recent_id == -1:
			return -1

		prompt = raw_input("Do you want to download the recent post by "+user_name+"? Press(y/n): ")
		
		if prompt.lower() == 'y':
			try:
				# If the recent post can be acquired, then download it
				download_post(recent_id)
			except: 
				print "Something went wrong. The post failed to be downloaded."
		return recent_id

	except:
		print "Failed to view the post"
		return -1;

# Function to like a post
def like_post():
	user_name = raw_input('Enter the user whose post you want to like: ')
	media_id = get_recent_post_id_user(user_name)
	request_url = (BASE_URL + 'media/%s/likes') % (media_id)
	payload = {'access_token': ACCESS_TOKEN}
	print 'Liking the post: '+request_url
	try:
		post_a_like = requests.post(request_url,payload).json()
		if post_a_like['meta']['code'] == 200:
			print 'Like was successfull'
		else:
			print 'Your like was unsuccessfull. Try Again!!'
	except:
		print 'An error occured while liking the post. Please try again!!'
		#print traceback.format_exc()
	
#Function to get comments from a post
def get_comments():
	user_name = raw_input('Enter the user whose post you want to fetch the list from: ')
	media_id = get_recent_post_id_user(user_name)
	
	if media_id == -1:
		return
	try:
		request_url = (BASE_URL + 'media/%s/comments?access_token=%s')%(media_id,ACCESS_TOKEN)
		comments = requests.get(request_url).json()
		comment_dict = {}
		print "Comments"
		print "====================================================="
		for comment in comments['data']:
			comment_dict[comment['text']] = comment['from']['username']
			print comment['text']+" \n --------------------------"+comment['from']['username']
			print '-----------------------------------------------------------'
	except:
		print traceback.format_exc()
		raw_input('Error fetching comments. Please try again!!') 


# Main
#=====================================================

print "Logging you in"
request_url = (BASE_URL + 'users/self/?access_token=%s') % (ACCESS_TOKEN)
my_info = requests.get(request_url).json()

# Print user's details
self_info()

# User for which an action has to be performed
user_name = raw_input("Enter a username: ")
id = user_info(user_name)
print "Searching for " + user_name
print "============================================="

# Options
while True:
	# Searches for the user name within your sandbox
	if id == -1:
		print "The username could not be found. Please try Again: "
		break
	print "============================================="
	print "What do you want to do with " + user_name
	print "1. Like a post"
	print "2. Comment on a post"
	print "6. Like a post"
	print "7. Get self recent post id"
	print "8. Get most recent post id"
	print "9. Exit"
	try:
		choice = int(raw_input("Enter your choice: "))
		if (choice == 9):
			print "The application will now terminate! Bbyee!!!"
			sys.exit()
		if choice == 8:
			recent_id = get_recent_post_id_user(user_name)
		if choice == 7:
			recent_id = get_recent_post_id()
		if choice == 6:
			like_post()

	except ValueError:
		print "Not a valid choice. Please enter a number as your choice."
		raw_input("Press Enter to continue.")	