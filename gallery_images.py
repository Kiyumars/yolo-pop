import sys
import os
import re
import itertools
import time
import webbrowser

import pyimgur
from tornado.ioloop import IOLoop
from PIL import Image, ImageDraw, ImageFont


CLIENT_ID = os.environ['IMGUR_CLIENT_ID']
CLIENT_SECRET = os.environ['IMGUR_CLIENT_SECRET']
img = pyimgur.Imgur(CLIENT_ID, CLIENT_SECRET)
# im = pyimgur.Imgur(CLIENT_ID)


############## global variables
Yolo = re.compile(r'.?yolo.?\b', re.IGNORECASE)
Bot_reply = "http://imgur.com/4ZP1q94"
Limit_requests = 20
Frontpage = 'hot'
Viral_or_new = 'viral'
How_long = 'day'
REPLY_DELAY = 60
Sleeping_time = 60*1
Uploading_image = '/home/kiyu/Projects/Imgur/yolopopo/personalised_yolo'

############## Helper functions

def authorisation():
	"""Gain posting authorisation from imgur"""
	auth_url = img.authorization_url('pin')
	webbrowser.open(auth_url)
	pin = raw_input('Tonto help Lone Ranger find Yolo beasts. Tonto need authorisation pin. Lone Ranger need to look at new screen.\n')
	img.exchange_pin(pin)
	print "Tonto go out find Yolo beasts. Do not follow Tonto. Too dangerous for Lone Ranger.\n"



def process_gallery(gallery_images):
	"""search image comments and only reply to one yolo comment per image"""
	total_yolos = 0
	for image in gallery_images:
		yolo_found = search_comments(image.get_comments(), total_yolos * REPLY_DELAY)
		if yolo_found:
			total_yolos += 1
		
	get_yolo_amount(total_yolos)

def search_comments(comments, delay):
	"""Search every comment for the regex pattern"""
	loopy = IOLoop.current()
	for comment in comments:
		if Yolo.search(comment.text):
			make_pic(comment.author.name)
			reply_link = upload_an_image()
			loopy.call_later(delay, reply_to_comment, comment, reply_link)
			return True

def reply_to_comment(comment, reply_link):
	"""bot replies to top yolo comments"""
	try:
		#this is just for my own edification
		author = str(comment.author.name)
		author_id = str(comment.author.id)
		comment_id = str(comment.id)
		text = comment.text
		print comment_id + ": " + text + " " + author + " " + author_id + "\n"
		print "Tonto kill Yolo beast. See dead yolo at " + comment.permalink + ". \n"
		#this actually posts the reply
		comment.reply(reply_link)
		make_pic(author)
		# yolo_amount += 1
	except UnicodeEncodeError:
		print "There was an unicode error."
		# continue
	except AttributeError:
		print "AttributeError. Skipping it."
		# continue	


def get_images():
	return img.get_gallery(section=Frontpage, sort=Viral_or_new, window=How_long, show_viral=True, limit=Limit_requests)

########## Please welcome the main function ##########

def yolo_police():
	"""the big Kahuna function."""

	#get all the gallery objects that fit the sorting criteria
	gallery = get_images()
	process_gallery(gallery)
	IOLoop.current().call_later(60 * 60, yolo_police)

def make_pic(username):
	"""Caption a pic or gif with the name of the author of the matched comment"""
	#only display part of overly long username
	if len(username) > 12:
		username = username[0:12]

	upper_msg = username.upper() + ". I am with the YOLO Police."
	lower_msg = "You are coming with me."
	image_original = 'yolopopo.jpg'
	image = Image.open(image_original)
	draw = ImageDraw.Draw(image)
	font = ImageFont.truetype("/usr/share/fonts/CODE Bold.otf", 45)

	draw.text((0,0), upper_msg, 'yellow', font=font)
	draw.text((0,600), lower_msg, 'yellow', font=font)

	image.save('personalised_yolo', 'PNG')
	# upload_an_image()

def upload_an_image():
	uploaded_image = img.upload_image(path=Uploading_image, title='We are with the YOLO police. You know what you did.')
	return uploaded_image.link


def get_yolo_amount(yolo_amount):
	if yolo_amount < 1:
		print "Tonto no find Yolos in wild.\n"
	else:
		print "Tonto find " + str(yolo_amount) + " Yolos out in wild.\n"
		print "Tonto now stalk Yolos, will strike when Yolos weak.\n"


########### Impressed? I thought so

if __name__ == '__main__':
	# see how this works if you enter a false pin
	def start_app():
		authorisation()
		yolo_police()

	loopy = IOLoop.current()
	loopy.call_later(0, start_app)
	loopy.start()

	# authorisation()

	# while True:
	# 	print "Tonto go out find Yolo beasts. Do not follow Tonto. Too dangerous for Lone Ranger."
	# 	yolo_police()
	# 	print "Tonto go sleep one hour. Then find Yolo again.\n"
	# 	time.sleep(Sleeping_time)
	# 	img.refresh_access_token()
