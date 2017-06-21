from KEYS import ACCESS_TOKEN
from KEYS import GOOGLE_API_KEY
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
	print request_url
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
	try:
		request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s')%(user_id,ACCESS_TOKEN)
		#print request_url
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
	payload = {
	'access_token': ACCESS_TOKEN
	}
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
			print comment['text']+" \n =======>> "+comment['from']['username']
			print '-----------------------------------------------------------'
	except:
		print traceback.format_exc()
		raw_input('Error fetching comments. Please try again!!') 

# Function to comment on a post
def comment_on():
	user_name = raw_input('Enter the user whose post you want to fetch the list from: ')
	media_id = get_recent_post_id_user(user_name)
	
	if media_id == -1:
		return
	try:
		request_url = (BASE_URL + 'media/%s/comments')%(media_id)
		#print request_url
		comment = raw_input("Enter your comment: ")
		payload = {
		'access_token':ACCESS_TOKEN,
		'text': comment
		}
		post_comment = requests.post(request_url,payload).json()
		if post_comment['meta']['code']==200:
			print "Successfully posted a comment"
		else:
			print "Failed to post the comment"
	except:
		print traceback.format_exc()


# ---------------------------------------------------------
#				IMAGES OF NATURAL CALAMITIES
# ---------------------------------------------------------
def img_natural_calamities():
	addr = raw_input("Enter the address: ")
	addr = addr.replace(' ','+').lower()
	GOOGLE_BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address='+addr+'&key='+GOOGLE_API_KEY
	
	# Get the latitude and longitude of the location
	try:
		coordinates = requests.get(GOOGLE_BASE_URL).json()
		latitude = coordinates['results'][0]['geometry']['location']['lat']
		longitude = coordinates['results'][0]['geometry']['location']['lng']
	except:
		#print traceback.format_exc()
		print "There was some error returning the coordinates of your location."
		return
	
	# Get all the media at that location
	print 'Searching at lat: '+str(latitude)+" , lng:"+str(longitude)
	try:
		request_url = (BASE_URL + 'media/search?lat=%s&lng=%s&access_token=%s')%(str(latitude),str(longitude),ACCESS_TOKEN)
		search_media = requests.get(request_url).json()
		keywords = ['disaster','earthquake','flood','calamit','landslide','tsunami','cyclone','avalanche','typhoon']
		count = 0
		for media in search_media['data']:
			for keyword in keywords:
				if keyword in media['caption']:
					download_post(media['id'])
					count+=1
		raw_input(str(count)+" posts found regarding disaster.")
		
	except:
		#print traceback.format_exc()
		print "There was some error fetching your posts."
		return
	
	
#img_natural_calamities()


# Main
#=====================================================

print "Logging you in"
request_url = (BASE_URL + 'users/self/?access_token=%s') % (ACCESS_TOKEN)
my_info = requests.get(request_url).json()

# Print user's details
self_info()

# Options
while True:
	print "============================================="
	print "================== M E N U =================="
	print "============================================="
	print "1. Like a post"
	print "2. Comment on a post"
	print "3. Get recent post id of self"
	print "4. Get recent post id of a user"
	print "5. View comments"
	print "6. Get images based on a location on natural calamities"
	print "7. Exit"
	try:
		choice = int(raw_input("Enter your choice: "))
		if choice == 1:
			like_post()
		elif choice==2:
			comment_on()
		elif choice == 3:
			get_recent_post_id()
		elif choice == 4:
			user_name = raw_input("Enter the name of the user:")
			recent_id = get_recent_post_id_user(user_name)
			print recent_id
		elif choice == 5:
			get_comments()
		elif choice == 6:
			img_natural_calamities()
		elif choice == 7:
			print "The application will now terminate! Bbyee!!!"
			sys.exit()
		else:
			print "Invalid Choice!!"

	except ValueError:
		print "Not a valid choice. Please enter a number as your choice."
		raw_input("Press Enter to continue.")	