import sys
import re
import itertools
import time

import webbrowser
import pyimgur


CLIENT_ID = "5551c39c732cf55"

im = pyimgur.Imgur(CLIENT_ID)

#phrase we are searching for and reply we will post and other global variables
match_word = str(sys.argv[1])
yolo = re.compile(r'{}'.format(match_word), re.IGNORECASE)
yolo_amount = 0
botReply = "http://imgur.com/InrBi3g"
limit_requests = 20	
img_section = 'hot'
img_sort = 'time'
window = 'day'
img_comments = []
total_img_comments = []

def get_image_comments(comments_list):
	"""search image comments and only reply to one yolo comment per image"""
	global yolo_amount
	for image in comments_list:
		try:
			comments_storage = image.get_comments()


			for ind_comments in comments_storage:
				#print ind_comments.text
				#just tracking all comments in separate list
				total_img_comments.append(ind_comments.text)

				#add comment to list only if it matches yolo, only one entry per image
				if yolo.search(ind_comments.text):
					img_comments.append(ind_comments)
					yolo_amount += 1
					break
				else:
					continue
		except ValueError:
					print "ValueError. It happens. \n"

def activate_bot(targets):
	"""bot replies to top yolo comments"""
	global yolo_amount
	for comment in targets:
		try:
			#you might have to use the decode function on comment.text
			print str(comment.id) + ": " + str(comment.text) + "\n"
		except UnicodeEncodeError:
				print "There was an unicode error."
				continue
		except AttributeError:
			print "AttributeError. Skipping it."	

def tonto_sleep():
	"""Clear out all global variables and restart in an hour"""
	if yolo_amount < 1:
		print "Tonto no find " + match_word + " out in wild. Tonto go sleep, try again in hour."
	else:
		print str(yolo_amount) + " " + match_word + " found, Lone Ranger. Must wait hour, find new " + match_word + "."
	clean_slate()
	# start program again in an hour
	time.sleep(60*60)
	print "Tonto go look for Yolo tracks again, Lone Ranger."
	yolo_again()

def clean_slate():
	"""clear out data in global variables"""
	total_img_comments = []
	img_comments = []
	yolo_amount = 0


def yolo_again():
	"""imgur access tokens only last an hour, so we need to refresh it"""
	im.refresh_access_token()
	yolo_police()

def monitoring(entire_gallery):
	"""print statements for monitoring purposes"""
	print str(len(entire_gallery)) + " pictures in your gallery."
	print str(len(total_img_comments)) + " total comments."
	print str(len(img_comments)) + " items in img_comments."



########## Please welcome the main function ##########

def yolo_police():
	"""the big Kahuna function."""

	print "Tonto go look for " + match_word + " out in wild. Do not follow Tonto. Much danger to Lone Ranger. \n"

	#get all the gallery objects that fit the sorting criteria
	gallery = im.get_gallery(section=img_section, sort=img_sort, window=window, show_viral=True, limit=limit_requests)
	
	get_image_comments(gallery)

	monitoring(gallery)

	activate_bot(img_comments)

	tonto_sleep()

if __name__ == '__main__':
	# authorisation()
	yolo_police()