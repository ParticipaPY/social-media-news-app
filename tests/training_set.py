import sqlite3
import json

# EJEMPLO DE COMO TIENE QUE SER EL JSON DE SALIDA
# {
#    "document" : [
#           {
#             "source":"Ejempla",
#             "created_time":"2016-05-16T14:02:54+0000",
#             "content":""
#             "reference":"www.facebook.com/726622947351359_1322914011055580",
#             "likes":272,
#             "shares":48,
#             "comments":53
#           }
#     ]
# }

def create_training_set_json():
	f_out = open("trainingset.json", "w")

	f_out.write('{ "document" : [ \n')

	conn = sqlite3.connect('social_network_posts.db')
	c = conn.cursor()
	# c.execute("select * from facebook_result where category NOT NULL order by category;")
	c.execute("select * from facebook_result order by comments DESC limit 1000")
	i = 0
	for row in c:
		f_out.write('{')
		f_out.write('"source" : "' + row[1].encode("utf8") + '",\n')
		f_out.write('"created_time" : "' + row[2].encode("utf8") + '",\n')
		f_out.write('"content" : "' + row[3].encode("utf8") + '",\n')
		f_out.write('"reference" : ' + str(row[0]) + ",\n")
		f_out.write('"likes" : ' + str(row[5]) + ",\n")
		f_out.write('"shares" : ' + str(row[6]) + ",\n")
		f_out.write('"comments" : ' + str(row[7]) + ",\n")
		if row[8]:
			f_out.write('"category" : "' + row[8].encode("utf8") + '"\n')
		else:
			f_out.write('"category" : "' + '"\n')
		i = i + 1
		f_out.write("},\n")

	f_out.write(']}\n')
	f_out.close()

if __name__ == '__main__':
	create_training_set_json()