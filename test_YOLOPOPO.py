import sys
import re

import webbrowser
import pyimgur


CLIENT_ID = "5551c39c732cf55"
CLIENT_SECRET = "ee9c26ce3daa35c4950407c5e8e1670431f1214f"

#use pyimgur's authentication methods
im = pyimgur.Imgur(CLIENT_ID, CLIENT_SECRET)


#assign new authentication pin only if needed.

def authorisation():
	# ready_pin = raw_input("Do you already have an existing pin? Yes/No \n")
	
	# if ready_pin[0:2].lower() == 'no':
	auth_url = im.authorization_url('pin')
	webbrowser.open(auth_url)
	pin = raw_input('Check the web browser. What is the pin shown there?\n')
	im.exchange_pin(pin)
	yolo_police()
	# elif ready_pin[0:3].lower() == 'yes':
	# 	pin = raw_input('Type in the existing pin \n')
	# 	im.exchange_pin(pin)
	# 	yolo_police()
	# else:
	# 	print "Did not understand your answer. Please try again \n"
	# 	authorisation()

#phrase we are searching for and reply we will post
yolo = re.compile(r'yolo\b', re.IGNORECASE)
botReply = "http://imgur.com/InrBi3g"

#search for a comment with yolo in it, print
#the comment and it's replies out
def yolo_police():
	id_input = raw_input("What is the image ID? Type stop to exit. \n")
	if id_input[0:4].lower() == "stop":
		print "Fine. Be that way."
		sys.exit()
	gallery = im.get_gallery_image(id_input)
	comment_list = gallery.get_comments()
	
	for entry in comment_list:
		if yolo.search(entry.text):
			replies = entry.get_replies()
			#print the top YOLO comment
			entry.reply(botReply)
			print "Bot Success!"
			print entry.text + '\n'

			yolo_police()

if __name__ == '__main__':
	authorisation()
