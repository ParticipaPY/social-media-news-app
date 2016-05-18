import tweepy
import datetime
import time
import sys
import requests
import csv
import urllib

from tweepy import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from bs4 import BeautifulSoup
from configuration_file import tw_access_token, tw_access_secret, tw_consumer_key, tw_consumer_secret, tw_sources
from lxml import html


# def get_num_comments(url_tweet):
# 	try:
# 		req = requests.get(url_tweet)
# 		# Comprobamos que la peticion nos devuelve un Status Code = 200
# 		statusCode = req.status_code

# 		if statusCode == 200:
# 			# Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
# 			t0 = datetime.datetime.now()
# 			html = BeautifulSoup(req.text, 'lxml')
# 			# Obtenemos todos los divs donde estan las entradas
# 			t1 = datetime.datetime.now()
# 			print 'el tiempo del soup es ' + str(t1- t0)
# 			entradas     = html.find('ol',{'id':'stream-items-id'})
# 			t2 = datetime.datetime.now()
# 			print 'el tiempo de find es ' + str(t2-t1)
# 			replies_list = entradas.find_all('li', {'class' : 'js-stream-item stream-item stream-item expanding-stream-item\n'})
# 			t3 = datetime.datetime.now()
# 			print 'el tiempo del find all es ' + str(t3-t2)

# 			return len(replies_list)		
# 		else:
# 			return 0	
# 	except:
# 		return 0

def get_num_comments(url_tweet):
    try:
        page = requests.get(url_tweet)
        doc = html.fromstring(page.content)
        replies_list = doc.xpath('//li[@class="js-stream-item stream-item stream-item expanding-stream-item\n"]')
        return len(replies_list)
    except Exception:
        return 0
	

def get_tweet_data(tweet, url):
	return ({"text": tweet.text.encode('utf-8').replace('\n', ' ').replace('\r',' ').replace('\t',''),
			 "url": url,
			 "created_at": tweet.created_at,
			 "favorite": tweet.favorite_count, 
			 "retweet": tweet.retweet_count, 
			 "replies": get_num_comments(url)})

def save_tweet_data(data, source, writer):
	if data != None:
		writer.writerow([source, data['created_at'], data["text"], data["url"], data["favorite"], data["retweet"], data["replies"]])

def get_twitter_tweets():
	max_id    = -1
	count_180 = 0
	ban       = 0
	max_tweet = 0
	now_UTC   = datetime.datetime.utcnow()
	max_delta = datetime.timedelta(days=180)

	auth      = tweepy.OAuthHandler(tw_consumer_key, tw_consumer_secret)
	auth.set_access_token(tw_access_token, tw_access_secret)
	api       = tweepy.API(auth)



	for source, page_id in tw_sources.iteritems():
		output_file = open("TwitterResults_" + source  + '_(' + str(186) + ' days)_' + str(datetime.datetime.now()).replace(":", "_") + ".csv", "wb")
		writer 		= csv.writer(output_file)
		writer.writerow(['Source', 'Date', 'Text', 'URL', 'Favorites', 'Retweets', 'Replies'])
		while(True):
			if(ban == 1 or max_tweet > 3200):
				break
			t0 = datetime.datetime.now()
			if(max_id == -1):
				timeline = api.user_timeline(user_id=page_id, count = 190)
			else:
				timeline = api.user_timeline(user_id=page_id, count = 190, max_id= max_id)
			print 'tiepo de respuesta de la api ' + str(datetime.datetime.now() - t0)
			count_180 = count_180 + 1
			# sys.stderr.write(str(count_180))
			for t in timeline:
				max_tweet = max_tweet + 1
				delta 	  = now_UTC - t.created_at

				if( delta <= max_delta ):
					url_tweet = "http://www.twitter.com/" + t.author.screen_name + "/status/" + t.id_str
					data 	  = get_tweet_data(t, url_tweet)
					save_tweet_data(data, source, writer)
				else:
					ban = 1
					break
					
				max_id = t.id

			# if (count_180 >= 180):
			# 	time.sleep(2)

		max_id    = -1
		ban       = 0
		max_tweet = 0
	output_file.close()
	print 'elapsed time ' + str(datetime.datetime.utcnow() - now_UTC)



if __name__ == '__main__':
	get_twitter_tweets()