import sys
import os
import re
import itertools
import time
import webbrowser

import pyimgur
from PIL import Image, ImageDraw, ImageFont


CLIENT_ID = os.environ['Imgur_CLIENT_ID']
CLIENT_SECRET = os.environ['Imgur_CLIENT_SECRET']
img = pyimgur.Imgur(CLIENT_ID, CLIENT_SECRET)
# im = pyimgur.Imgur(CLIENT_ID)


############## global variables
Yolo = re.compile(r'.?yolo.?\b', re.IGNORECASE)
Bot_reply = "http://imgur.com/4ZP1q94"
Limit_requests = 3
Frontpage = 'hot'
Viral_or_new = 'viral'
How_long = 'day'
Reply_delay = 7
Sleeping_time = 60*1
Uploading_image = '/home/kiyu/Projects/Imgur/yolopopo/personalised_yolo'

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
		if Yolo.search(comment.text):
			make_pic(comment.author.name)
			reply_link = upload_an_image()
			bot_replies(comment, reply_link)
			break
		else:
			continue


def bot_replies(comment, reply_link):
	"""bot replies to top yolo comments"""
	try:
		#this is just for my own edification
		author = str(comment.author.name)
		author_id = str(comment.author.id)
		comment_id = str(comment.id)
		text = comment.text
		print comment_id + ": " + text + " " + author + " " + author_id + "\n"
		
		#this actually posts the reply
		comment.reply(reply_link)
		make_pic(author)
		time.sleep(Reply_delay)
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
	return img.get_gallery(section=Frontpage, sort=Viral_or_new, window=How_long, show_viral=True, limit=Limit_requests)

########## Please welcome the main function ##########

def yolo_police():
	"""the big Kahuna function."""

	#get all the gallery objects that fit the sorting criteria
	gallery = get_images()

	get_image_comments(gallery)

def make_pic(username):
	"""Caption a pic or gif with the name of the author of the matched comment"""
	upper_msg = username.upper() + ". I am with the YOLO Police."
	lower_msg = "You are coming with me."
	image_original = 'yolopopo.jpg'
	image = Image.open(image_original)
	draw = ImageDraw.Draw(image)
	font = ImageFont.truetype("/usr/share/fonts/CODE Bold.otf", 45)

	draw.text((0,0), upper_msg, 'white', font=font)
	draw.text((0,600), lower_msg, 'white', font=font)

	image.save('personalised_yolo', 'PNG')
	# upload_an_image()

def upload_an_image():
	uploaded_image = img.upload_image(path=Uploading_image, title='We are with the YOLO police. You know what you did.')
	return uploaded_image.link



########### Impressed? I thought so

if __name__ == '__main__':
	#see how this works if you enter a false pin
	authorisation()

	while True:
		print "Tonto go out find Yolo beasts. Do not follow Tonto. Too dangerous for Lone Ranger."
		yolo_police()
		print "Tonto go sleep one hour. Then find Yolo again.\n"
		time.sleep(Sleeping_time)
		img.refresh_access_token()
