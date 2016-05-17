import facebook
import time
import datetime
import requests
import csv

from configuration_file import facebook_sources, facebook_access_token, days

# ___________________________________________________________________________________________________________________________________________________________
# Returns the 'since' date as a unix timestamp (seconds since epoch). Needed for the facebook api parameter to know what's the date lower bound of search
def get_since_parameter(days = 7):
	# get current timestamp as a python datetime object
	dt_now = datetime.datetime.now()
	dt_now_unix = time.mktime(dt_now.timetuple())

	# print 'obtenido con datetime y mktime: ' + str(int(dt_now_unix))

	t_unix = time.time()
	# print 'obtenido con time.time() nomas: ' + str(int(t_unix))

	# delta = datetime.timedelta(days = 30)
	# Converts de number of days in a python timedelta object
	delta = datetime.timedelta(days)
	print 'diferencia de tiempo = ' + str(delta)

	# Substracts the difference from the current timestamp to calculate the 'since' date
	dt_since = dt_now - delta
	# Converts de 'since' date (now a python datetime object) in a unix timestamp
	dt_since_unix = time.mktime(dt_since.timetuple())
	print "La valor de since para " + str(dt_since) + ' en unix es = ' + str(int(dt_since_unix))
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

	return int(dt_since_unix)

# _________________________________________________________________________________________________________________________
# returns the required information of a single post as a dictionary withe the following fields:
#		- text: the text of the post, concatenation of the name and/or message and/or description
#		- created_time: a string representing the date-time of creation of the post
#		- likes: the number of likes to that post
#		- shares: a number representing the times that the post has been shared
#		- comments: the count of comments on that post
def get_post_data(post):
	#initial values for return
	text = ''
	likes = 0
	shares = 0
	comments = 0
	url = ''
	created_time = 0

	try:
		# each 'if' verifies if a given field exists in the post (fields differs depending on the post's type)
		if "type" in post.keys():
			# print 'type: ' + post['type']
			pass
		else:
			# print "NO TIENE type"
			pass
		#################################################################################################################
		# date and time of creation of the post
		if "created_time" in post.keys():
			# print 'created_time: ' + post['created_time']
			created_time = str(post['created_time'])
			# pass
		else:
			# print "NO TIENE created_time"
			pass
		#################################################################################################################
		# a part of the 'text' return value
		if "name" in post.keys():
			# print 'name: ' + post['name'].encode('utf-8')
			text = text + post['name'].encode('utf-8')
		else:
			# print "NO TIENE name"
			pass
		#################################################################################################################
		# a part of the 'text' return value
		if "message" in post.keys():
			# print "message: " + post['message'].encode('utf-8').replace('\n',' ').replace('\r',' ').replace('\t','')
			text = text + ' ' + post['message'].encode('utf-8').replace('\n',' ').replace('\r',' ').replace('\t','')
		else:
			# print "NO TIENE message"
			pass
		#################################################################################################################
		# link inserted on 'link'-type posts. Currently unused
		if "link" in post.keys():
			# print 'link: ' + post['link']
			pass
		else:
			# print "NO TIENE link"
			pass
		#################################################################################################################
		# 'shares' return value
		if "shares" in post.keys():
			# print 'shares: ' + str(post['shares']['count'])
			shares = post['shares']['count']
		else:
			# print "NO TIENE shares"
			pass
		#################################################################################################################
		# 'likes' return value
		if "likes" in post.keys():
			# print 'likes: ' + str(post['likes']['summary']['total_count'])
			likes = post['likes']['summary']['total_count']
		else:
			# print "NO TIENE likes"
			pass
		#################################################################################################################
		# 'comments' return value
		if "comments" in post.keys():
			# print 'comments: ' + str(post['comments']['summary']['total_count'])
			comments = post['comments']['summary']['total_count']
		else:
			# print "NO TIENE comments"
			pass
		#################################################################################################################
		# a part of the 'text' return value
		if "description" in post.keys():
			# print 'description: ' + post['description'].encode('utf-8').replace('\n',' ').replace('\r',' ').replace('\t','')
			text = text + post['description'].encode('utf-8').replace('\n',' ').replace('\r',' ').replace('\t','')
		else:
			# print "NO TIENE description"
			pass
		#################################################################################################################
		# this field is used to create the 'url' return value
		if "id" in post.keys():
			# print 'id: ' + str(post['id'])
			url = "www.facebook.com/" + str(post["id"])
			# print url
		else:
			# print "NO TIENE id"
			pass

		# print ' ----------------------------------------------------------------------------------------------------- '

		# returns a dict with the required data
		return ({"text": text, "url": url, "likes": likes, "shares": shares, "comments": comments, 'created_time': created_time})

	except Exception, e:
		print str(e)
		print 'FALTA ALGUNO DE ESOS CAMPOS: ' + str(post)
		print ' ----------------------------------------------------------------------------------------------------- '
		return None

# ____________________________________________________________________________________________________________________________________________________
# Saves a single post in a persistent file or database. Currently a CSV. Adds the 'source' field to the post data
def save_post_data(data, source, writer):
	if data != None:
			print source
			writer.writerow([source, data['created_time'] ,data["text"], data["url"], data["likes"], data["shares"], data["comments"]])

# _____________________________________________________________________________________________________________________________________________________
# For each source it retrieves all the posts from the las period of time that is specified by the 'days' variable in configuration_file.py
def get_facebook_posts():
	start_time = datetime.datetime.now() # a timestamp to measure how long does it take process all sources
	posts_counter = {} # a dict that counts how many post of each kind are found
	api_calls_counter = 1 # a counter who keep tracks of how many calls to tha api have been done
	graph = facebook.GraphAPI(facebook_access_token) # access to facebook api with the access token


	for source, page_id in facebook_sources.iteritems():
		# each source has its own csv file indicating the name of the source, how many days were fetched, and the timestamp
		output_file = open("FacebookResults_" + source  + '_(' + str(days) + ' dias)_' + str(datetime.datetime.now()).replace(":", "_") + ".csv", "wb")
		# initialize the csv writer object and write the column headers
		writer = csv.writer(output_file)
		writer.writerow(["source", "created_time", "text", "url", "likes", "shares","comments"])
		# get the first 100 post
		posts = graph.get_connections(page_id, 'posts', fields="type, name, from, shares, created_time, link, message, description, caption, likes.limit(0).summary(True), comments.limit(0).summary(True)", since=get_since_parameter(days), limit=100)
		# this loops through the different pages of post until there are no more results (the 'since' date is reached)
		while True:
			try:
				for post in posts['data']:
					try:
						data = get_post_data(post)
						save_post_data(data, source, writer)
						# increase the counter of post according to the post type
						if post['type'] not in posts_counter.keys():
							# the first time a new type of post if found its respective counter
							posts_counter[post['type']] = 1
						else:
							# if it's not the fist time, the counter must be increased
							posts_counter[post['type']] = posts_counter[post['type']] + 1
					except Exception, e:
						print str(e)
				
				# sleep for a little time for not overloading the api
				time.sleep(2)
				# request the next page of posts
				posts = requests.get(posts['paging']['next']).json()
				api_calls_counter = api_calls_counter + 1

			except KeyError:
				# When there are no more pages (['paging']['next']), break from the
				# loop and end the script.
				break
		output_file.close()
	
	end_time = datetime.datetime.now() # timestamp when the program ended
	elapsed_time = end_time - start_time
	# print contador
	print '>>> RESULTADOS <<<'
	total = 0
	for key, value in posts_counter.iteritems():
		print key.encode('utf-8') + ': ' + str(value)
		total = total + value
	print 'TOTAL = ' + str(total)
	print 'LLAMADAS = ' + str(api_calls_counter)
	print 'ELAPSED TIME = ' + str(elapsed_time)





if __name__ == "__main__":
	get_facebook_posts()
	# debug_failed()

