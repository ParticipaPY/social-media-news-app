import requests
import sqlite3
import datetime
import json
import time
from havenondemand.hodclient import *


# API_KEY = '366a4602-d8f6-4716-8cc6-b65036fb26a2'
API_KEY = 'd9cc78bd-b6a9-4bb6-84bc-cfb64d56fead'

def categorize(text, client):
	# if text is False:
	# 	raise ValueError('No text given to categorize')
	response = client.get_request({'text': text, "index": "categorization"}, HODApps.CATEGORIZE_DOCUMENT, async=False)
	
	category = "NO CATEGORY"
	try: 
		category = response["documents"][0]["title"]
	except Exception, e:
		print str(e)

	return category


def temporary_master():
	conn = sqlite3.connect('social_network_posts.db')
	# c = conn.cursor()

	f = open("identified_facebook_posts_url.txt")
	urls = f.readlines()
	f.close()

	client = HODClient(API_KEY, version="v1")

	for url in urls:
		url = url.replace("\n","")
		print url
		cursor = conn.cursor()
		cursor2 = conn.cursor()
		cursor.execute("select content from facebook_result where url = '" + url + "';")
		for row in cursor:
			# print row[0]
			response = categorize(row[0], client)
			print response
			cursor2.execute("update facebook_result set category = '" + response + "' where url = '" + url + "';")
			# for row in cursor2:
			# 	print row
			print "---------------------------------------------------------------------------"

		time.sleep(1)

	conn.commit()
	conn.close()


if __name__ == "__main__":
	temporary_master()