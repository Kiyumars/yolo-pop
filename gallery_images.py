import sys
import re

#from threading import Timer
import time

import webbrowser
import pyimgur

print "Version 2"

CLIENT_ID = "5551c39c732cf55"
CLIENT_SECRET = "ee9c26ce3daa35c4950407c5e8e1670431f1214f"

im = pyimgur.Imgur(CLIENT_ID, CLIENT_SECRET)

#phrase we are searching for and reply we will post
yolo = re.compile(r'yolo', re.IGNORECASE)
botReply = "http://imgur.com/InrBi3g"
limit_requests = 40
img_section = 'hot'
img_sort = 'viral'
window = 'day'
yolo_amount = []
bad_list = []

def authorisation():
	auth_url = im.authorization_url('pin')
	webbrowser.open(auth_url)
	pin = raw_input('Check the web browser. What is the pin shown there?\n')
	im.exchange_pin(pin)
	yolo_police()

def comment():
	pass

def yolo_police():
	gallery = im.get_gallery(section=img_section, sort=img_sort, window=window, show_viral=True, limit=limit_requests)
	img_comments = []

	for image in gallery:
		try:
			img_comments.append(image.get_comments())
		except ValueError:
			print "ValueError. It happens. \n"
	


	print str(len(gallery)) + " pictures in your gallery."
	print str(len(img_comments)) + " comments in img_comments."


	for comment in img_comments:
		# comment = comment.encode('UTF-8')
		if yolo.search(comment.text):
			#you might have to use the decode function on comment.text

			print str(comment.id) + ": " + str(comment.text) + "\n"
			#comment.reply(botReply)
			#time.sleep(7)
			continue

	if len(yolo_amount) < 1:
		print "No Yolos were found out in de wild, senor."
	else:
		str(len(yolo_amount)) + " were found, master."



if __name__ == '__main__':
	authorisation()
