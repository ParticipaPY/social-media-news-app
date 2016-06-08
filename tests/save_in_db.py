import sqlite3
import os
import csv
import datetime
import json

def save_facebook_posts():
	# create the connection object that represents de db
	conn = sqlite3.connect('social_network_posts.db')
	c = conn.cursor()
	# conn.close()
	# c.execute("DROP TABLE IF EXISTS facebook_results;")
	c.execute("CREATE TABLE facebook_result (id INTEGER PRIMARY KEY, source TEXT, timestamp DATETIME, content TEXT, url TEXT, likes INTEGER, shares INTEGER, comments INTEGER, category TEXT);")
	results = os.listdir('../results/facebook_results')
	current_id = 0
	for result in results:
		f = open('../results/facebook_results/' + result, 'rb')
		reader = csv.reader(f)
		first = True
		for row in reader:
			if first:
				first = False
				continue
			timestamp = datetime.datetime.strptime(row[1].replace('+0000', ''), "%Y-%m-%dT%H:%M:%S")
			content = row[2].replace('\"', '\'')
			query = "INSERT INTO facebook_result (id, source, timestamp, content, url, likes, shares, comments) VALUES (" + str(current_id) + ",\"" + row[0] + " (Facebook)\",\"" + str(timestamp) + "\",\"" + content + "\",\"" + row[3] + "\"," + row[4] + "," + row[5] + "," +  row[6] + ");"
			try:
				c.execute(query)
				current_id = current_id + 1
				# print query
			except Exception, e:
				print '----------------------------------------------------------------------------------------------------------------'
				print query
				print str(e)
				print '----------------------------------------------------------------------------------------------------------------'
		f.close()
	conn.commit()
	conn.close()

def save_twitter_posts():
	# create the connection object that represents de db
	conn = sqlite3.connect('social_network_posts.db')
	c = conn.cursor()
	# conn.close()
	# c.execute("DROP TABLE IF EXISTS facebook_results;")
	c.execute("CREATE TABLE twitter_result (id INTEGER PRIMARY KEY, source TEXT, timestamp DATETIME, content TEXT, url TEXT, favs INTEGER, retweets INTEGER, comments INTEGER, category TEXT);")
	results = os.listdir('../results/twitter_results')
	current_id = 0
	for result in results:
		f = open('../results/twitter_results/' + result, 'rb')
		reader = csv.reader(f)
		first = True
		for row in reader:
			if first:
				first = False
				continue
			timestamp = row[1]
			content = row[2].replace('\"', '\'')
			query = "INSERT INTO twitter_result (id, source, timestamp, content, url, favs, retweets, comments) VALUES (" + str(current_id) + ",\"" + row[0] + " (Twitter)\",\"" + str(timestamp) + "\",\"" + content + "\",\"" + row[3] + "\"," + row[4] + "," + row[5] + "," +  row[6] + ");"
			try:
				c.execute(query)
				current_id = current_id + 1
				# print query
			except Exception, e:
				print '----------------------------------------------------------------------------------------------------------------'
				print query
				print str(e)
				print '----------------------------------------------------------------------------------------------------------------'
		f.close()
	conn.commit()
	conn.close()

if __name__ == '__main__':
	save_facebook_posts()
	save_twitter_posts()