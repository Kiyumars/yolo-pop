import sys
import re

import webbrowser
import pyimgur


CLIENT_ID = "5551c39c732cf55"
CLIENT_SECRET = "ee9c26ce3daa35c4950407c5e8e1670431f1214f"

# comments_file = open('rapcrapComments2.txt', 'r+')
im = pyimgur.Imgur(CLIENT_ID, CLIENT_SECRET)
auth_url = im.authorization_url('pin')
webbrowser.open(auth_url)
pin = raw_input('What is the pin?')
im.exchange_pin(pin)
#image = im.get_image(str(sys.argv[1]))
#comment = im.get_comment('243757516')
#comment = image.get_comment()
botReply = "http://imgur.com/InrBi3g"
gallery = im.get_gallery_image(raw_input("What is the image ID?"))
comment_list = gallery.get_comments()

yolo = re.compile(r'yolo\b', re.IGNORECASE)

#search for a comment with yolo in it, print
#the comment and it's replies out
for entry in comment_list:
	if yolo.search(entry.text):
		replies = entry.get_replies()
		#print the top YOLO comment
		entry.reply(botReply)
		print "Bot Success!"
		print entry.text + '\n'
		#print the replies to top YOLO comment
		for reply in replies:
			print reply.text + '\n'

		break

