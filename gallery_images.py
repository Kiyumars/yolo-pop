import sys
import os
import re
import itertools
import time
import webbrowser

import pyimgur


CLIENT_ID = os.environ['Imgur_CLIENT_ID']
CLIENT_SECRET = os.environ['Imgur_CLIENT_SECRET']
img = pyimgur.Imgur(CLIENT_ID, CLIENT_SECRET)
# im = pyimgur.Imgur(CLIENT_ID)


############## global variables
yolo = re.compile(r'.?yolo.?\b', re.IGNORECASE)
botReply = "http://imgur.com/4ZP1q94"
limit_requests = 3
img_section = 'hot'
img_sort = 'viral'
window = 'day'
reply_delay = 7
sleeping_time = 60*1

############## Helper functions

def authorisation():
	"""Gain posting authorisation from imgur"""
	auth_url = img.authorization_url('pin')
	webbrowser.open(auth_url)
	pin = raw_input('Tonto help Lone Ranger find Yolo beasts. Tonto need authorisation pin. Lone Ranger need to look at new screen.\n')
	img.exchange_pin(pin)


def get_image_comments(gallery_images):
	"""search image comments and only reply to one yolo comment per image"""
	for image in gallery_images:
		search_comments(image.get_comments())


def search_comments(comments):
	"""Search every comment for the regex pattern"""
	for comment in comments:
		if yolo.search(comment.text):
			bot_replies(comment)
			break
		else:
			continue


def bot_replies(comment):
	"""bot replies to top yolo comments"""
	try:
		#this is just for my own edification
		author = str(comment.author.name)
		author_id = str(comment.author.id)
		comment_id = str(comment.id)
		text = comment.text
		print comment_id + ": " + text + " " + author + " " + author_id + "\n"
		
		#this actually posts the reply
		comment.reply(botReply)
		time.sleep(reply_delay)
		# yolo_amount += 1
	except UnicodeEncodeError:
		print "There was an unicode error."
		# continue
	except AttributeError:
		print "AttributeError. Skipping it."
		# continue	


def yolo_again():
	"""imgur access tokens only last an hour, so we need to refresh it"""
	img.refresh_access_token()
	yolo_police()


def get_images():
	return img.get_gallery(section=img_section, sort=img_sort, window=window, show_viral=True, limit=limit_requests)

########## Please welcome the main function ##########

def yolo_police():
	"""the big Kahuna function."""

	#get all the gallery objects that fit the sorting criteria
	gallery = get_images()

	get_image_comments(gallery)


########### Impressed? I thought so

if __name__ == '__main__':
	#see how this works if you enter a false pin
	authorisation()

	while True:
		print "Tonto go out find Yolo beasts. Do not follow Tonto. Too dangerous for Lone Ranger."
		yolo_police()
		print "Tonto go sleep one hour. Then find Yolo again.\n"
		time.sleep(sleeping_time)
		img.refresh_access_token()
