import facebook
import time
import datetime
import requests
import csv

from configuration_file import facebook_sources, facebook_access_token


def get_since_parameter(days = 7):

	dt_now = datetime.datetime.now()
	dt_now_unix = time.mktime(dt_now.timetuple())

	# print 'obtenido con datetime y mktime: ' + str(int(dt_now_unix))

	t_unix = time.time()
	# print 'obtenido con time.time() nomas: ' + str(int(t_unix))

	# delta = datetime.timedelta(days = 30)
	delta = datetime.timedelta(days)
	print 'diferencia de tiempo = ' + str(delta)

	dt_since = dt_now - delta
	dt_since_unix = time.mktime(dt_since.timetuple())
	print "La valor de since para " + str(dt_since) + ' en unix es = ' + str(int(dt_since_unix))
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

	return int(dt_since_unix)


def get_post_data(post):
	text = ''
	likes = 0
	shares = 0
	comments = 0
	url = ''

	try:
		if "type" in post.keys():
			# print 'type: ' + post['type']
			pass
		else:
			# print "NO TIENE type"
			pass
		#################################################################################################################
		if "created_time" in post.keys():
			# print 'created_time: ' + post['created_time']
			pass
		else:
			# print "NO TIENE created_time"
			pass
		#################################################################################################################
		if "name" in post.keys():
			# print 'name: ' + post['name'].encode('utf-8')
			text = text + post['name'].encode('utf-8')
		else:
			# print "NO TIENE name"
			pass
		#################################################################################################################
		if "message" in post.keys():
			# print "message: " + post['message'].encode('utf-8').replace('\n',' ').replace('\r',' ').replace('\t','')
			text = text + ' ' + post['message'].encode('utf-8').replace('\n',' ').replace('\r',' ').replace('\t','')
		else:
			# print "NO TIENE message"
			pass
		#################################################################################################################
		if "link" in post.keys():
			# print 'link: ' + post['link']
			pass
		else:
			# print "NO TIENE link"
			pass
		#################################################################################################################
		if "shares" in post.keys():
			# print 'shares: ' + str(post['shares']['count'])
			shares = post['shares']['count']
		else:
			# print "NO TIENE shares"
			pass
		#################################################################################################################
		if "likes" in post.keys():
			# print 'likes: ' + str(post['likes']['summary']['total_count'])
			likes = post['likes']['summary']['total_count']
		else:
			# print "NO TIENE likes"
			pass
		#################################################################################################################
		if "comments" in post.keys():
			# print 'comments: ' + str(post['comments']['summary']['total_count'])
			comments = post['comments']['summary']['total_count']
		else:
			# print "NO TIENE comments"
			pass
		#################################################################################################################
		if "description" in post.keys():
			# print 'description: ' + post['description'].encode('utf-8').replace('\n',' ').replace('\r',' ').replace('\t','')
			text = text + post['description'].encode('utf-8').replace('\n',' ').replace('\r',' ').replace('\t','')
		else:
			# print "NO TIENE description"
			pass
		#################################################################################################################
		# if "from" in post.keys():
			# print 'from: ' + str(post['from']['name'])
		# else:
			# print "NO TIENE from"
		#################################################################################################################
		if "id" in post.keys():
			# print 'id: ' + str(post['id'])
			url = "www.facebook.com/" + str(post["id"])
			# print url
		else:
			# print "NO TIENE id"
			pass

		print ' ----------------------------------------------------------------------------------------------------- '

		# #################################################################################################################
		# if post['type'] == "link":
		# 	text = post['name'].encode('utf-8') + post['message'].encode('utf-8').replace('\n',' ').replace('\r',' ').replace('\t','')
		# elif post['type'] == "photo":
		# 	text = post['message'].encode('utf-8').replace('\n',' ').replace('\r',' ').replace('\t','')
		# elif post['type'] == 'video' and 'description' in posts.keys():
		# 	text = post['description'].encode('utf-8').replace('\n',' ').replace('\r',' ').replace('\t','')
		# elif post['type'] == "status":
		# 	return None
		# #################################################################################################################
		return ({"text": text, "url": url, "likes": likes, "shares": shares, "comments": comments})

	except Exception, e:
		print str(e)
		print 'FALTA ALGUNO DE ESOS CAMPOS: ' + str(post)
		print ' ----------------------------------------------------------------------------------------------------- '
		return None

def save_post_data(data, source, writer):
	if data != None:
			writer.writerow([source, data["text"], data["url"], data["likes"], data["shares"], data["comments"]])

def get_facebook_posts():
	start_time = datetime.datetime.now()
	posts_counter = {} # a dict that counts how many post of each kind are found
	api_calls_counter = 1 # a counter who keep tracks of how many calls to tha api have benn done
	graph = facebook.GraphAPI(facebook_access_token)
	output_file = open("FacebookResults.csv", "wb")
	writer = csv.writer(output_file)
	writer.writerow(["source", "text", "url", "likes", "shares","comments"])


	for source, page_id in facebook_sources.iteritems():
		profile = graph.get_object(page_id)
		posts = graph.get_connections(profile['id'], 'posts', fields="type, name, from, shares, created_time, link, message, description, caption, likes.limit(0).summary(True), comments.limit(0).summary(True)", since=get_since_parameter(days=30))
		
		while True:
			try:
				for post in posts['data']:
					# try:
					# 	data = get_post_data(post)
					# 	save_post_data(data, source, writer)
					# 	if post['type'] not in contador.keys():
					# 		posts_counter[post['type']] = 1
					# 	else:
					# 		posts_counter[post['type']] = posts_counter[post['type']] + 1
					# except:
					# 	print 'FALTA ALGUNO DE ESOS CAMPOS: ' + str(post)
					
					data = get_post_data(post)
					save_post_data(data, source, writer)
					if post['type'] not in posts_counter.keys():
						posts_counter[post['type']] = 1
					else:
						posts_counter[post['type']] = posts_counter[post['type']] + 1
			
				
				time.sleep(5)
				posts = requests.get(posts['paging']['next']).json()
				api_calls_counter = api_calls_counter + 1

			except KeyError:
				# When there are no more pages (['paging']['next']), break from the
				# loop and end the script.
				break

	output_file.close()
	end_time = start_time = datetime.datetime.now()
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


def debug_failed():
	graph = facebook.GraphAPI(facebook_access_token)
	failed_list = ['303614086512550_484797811727509', '313024308746037_991170607598067', '313024308746037_991170514264743', '313024308746037_991167727598355', '313024308746037_991166280931833', '313024308746037_991165470931914', '313024308746037_991165277598600', '313024308746037_990863947628733', '313024308746037_990835270964934', '313024308746037_990188641029597', '313024308746037_990148337700294', '313024308746037_990148134366981', '313024308746037_988782664503528', '313024308746037_988522584529536', '313024308746037_988471321201329', '313024308746037_988465114535283', '313024308746037_988074047907723', '313024308746037_988001884581606', '313024308746037_987996804582114']
	for post_id in failed_list:
		post = graph.get_object(post_id, fields="type, name, from, shares, created_time, link, message, description, caption, likes.limit(0).summary(True), comments.limit(0).summary(True)")
		data = get_post_data(post)


if __name__ == "__main__":
	get_facebook_posts()
	# debug_failed()

