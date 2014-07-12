import sys
import re

import webbrowser
import pyimgur

CLIENT_ID = "5551c39c732cf55"
CLIENT_SECRET = "ee9c26ce3daa35c4950407c5e8e1670431f1214f"

im = pyimgur.Imgur(CLIENT_ID, CLIENT_SECRET)

#phrase we are searching for and reply we will post
yolo = re.compile(r'yolo', re.IGNORECASE)
botReply = "http://imgur.com/InrBi3g"
limit_requests = 100
img_section = 'hot'
img_sort = 'viral'
window = 'day'

def authorisation():
	auth_url = im.authorization_url('pin')
	webbrowser.open(auth_url)
	pin = raw_input('Check the web browser. What is the pin shown there?\n')
	im.exchange_pin(pin)
	yolo_police()

def yolo_police():
	gallery = im.get_gallery(section=img_section, sort=img_sort, window=window, show_viral=True, limit=limit_requests)

	for image in gallery:
		img_comments = image.get_comments()

		for comment in img_comments:
			if yolo.search(comment.text):
				encoded_text = comment.text.encode('UTF-8')
				print str(comment.id) + ": " + encoded_text + "\n"
				comment.reply(botReply)
				break

if __name__ == '__main__':
	authorisation()