import sys
import re
import itertools

#from threading import Timer
import time

import webbrowser
import pyimgur


CLIENT_ID = "5551c39c732cf55"
CLIENT_SECRET = "ee9c26ce3daa35c4950407c5e8e1670431f1214f"

im = pyimgur.Imgur(CLIENT_ID, CLIENT_SECRET)
#im = pyimgur.Imgur(CLIENT_ID)

#phrase we are searching for and reply we will post
yolo = re.compile(r'yolo', re.IGNORECASE)
botReply = "http://imgur.com/InrBi3g"
limit_requests = 40
img_section = 'hot'
img_sort = 'time'
window = 'day'


def authorisation():
	auth_url = im.authorization_url('pin')
	webbrowser.open(auth_url)
	pin = raw_input('Tonto help Lone Ranger find Yolo beasts. Tonto need authorisation pin. Lone Ranger need to look at new screen.\n')
	im.exchange_pin(pin)
	yolo_police()

#just in case I need some helper function for comments
def comment():
	pass

#the big Kahuna function. 
def yolo_police():
	#get all the gallery objects that fit the sorting criteria
	gallery = im.get_gallery(section=img_section, sort=img_sort, window=window, show_viral=True, limit=limit_requests)
	comments_storage = []
	img_comments = []
	yolo_amount = 0
	checking_amount = 0


	for image in gallery:
		try:
			comments_storage.append(image.get_comments())
 
			# for storage_entries in comments_storage:
			# 	storage_entries.text
			# 	img_comments.append(storage_entries)
			# comments_storage = []
		except ValueError:
			print "ValueError. It happens. \n"

	#create a flatted list from the nested list in comments_storage
	img_comments = list(itertools.chain.from_iterable(comments_storage))

	#print statements for monitoring purposes
	print str(len(gallery)) + " pictures in your gallery."
	print str(len(comments_storage)) + " items in comments_storage."
	print str(len(img_comments)) + " items in img_comments."
	print "Img comments is a " + str(type(img_comments))
	print "comments_storage is a " + str(type(comments_storage))
	#print img_comments
	#print str(len(img_comments)) + " comments in img_comments."
	#print img_comments

	#search all comments for the term yolo, print out the matched results

	for comment in img_comments:
		try:
		# comment = comment.encode('UTF-8')
			if yolo.search(comment.text):
				#you might have to use the decode function on comment.text
				print str(comment.id) + ": " + str(comment.text) + "\n"
				comment.reply(botReply)
				time.sleep(7)
				yolo_amount += 1
				break

		except UnicodeEncodeError:
			print "There was an unicode error."
			continue

	if yolo_amount < 1:
		print "Tonto no find Yolos out in wild. Tonto go sleep, try again in hour."
	else:
		print str(yolo_amount) + " found, Lone Ranger. Must wait hour, find new Yolos."

	#start program again in an hour
	time.sleep(60*60)
	print "Tonto go look for Yolo tracks again, Lone Ranger."
	yolo_again()

def yolo_again():
	#imgur access tokens only last an hour, so we need to refresh it
	im.refresh_access_token()
	yolo_police()

if __name__ == '__main__':
	authorisation()
	#yolo_police()