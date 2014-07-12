import sys
import re

import webbrowser
import pyimgur

CLIENT_ID = "be44c44205bb5a2"

im = pyimgur.Imgur(CLIENT_ID)

gallery = im.get_gallery(section='hot', sort='viral', window='week', show_viral=True, limit=20)

for image in gallery:
	print image.title