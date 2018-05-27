import time
import csv
from pytrends.request import TrendReq
import pandas
import sys
from multiprocessing import Pool as ThreadPool 
import random
import json

'''
This script is to collect sugeestions from Google Trends API
'''
def time_convert(json_ts):
	t = time.strftime("%D %H:%M", time.localtime(int(json_ts)))
	year = '20' + t[6:8]
	month = t[:2]
	day = t[3:5]
	return year +'-'+ month +'-'+ day

def trends_session(google_username, google_password):
	path = ""
	pytrend = TrendReq(google_username, google_password, custom_useragent='My Pytrends Script' )
	return pytrend

def get_trends(session, kw, tf=False):
	if tf == False:
		session.build_payload(kw_list=[kw])
	else:	
		session.build_payload(kw_list=[kw],timeframe = tf)

	interest_over_time_df = session.interest_over_time()
	interest_over_time_json =  pandas.DataFrame.to_json(interest_over_time_df)
	return interest_over_time_json

def get_suggestions(session, kw):
	suggest = session.suggestions(kw)
	return json.dumps(suggest)

def save_data(tup):
	# google_username, google_password
	# input_article_file: a tsv file with "article_name" column
	# output_file: name of output file

	google_username, google_password, input_article_file, output_file = tup
	s = trends_session(google_username = google_username, google_password = google_password)

	f = open(output_file,'a')
	file = open("suggest1_log.txt",'a')
	with open(input_article_file) as tsvfile:
		reader = csv.DictReader(tsvfile, delimiter='\t')
		for row in reader:
			i = 1
			while i <= 5:
				try:
					tf = "2004-01-01 2017-05-31"
					# if int(row['from_timestamp']) < 1072933200:
					# 	tf =  "2004-01-01 " + time_convert(row['to_timestamp']) 
					# else:
					# 	tf = time_convert(row['from_timestamp']) + " " + time_convert(row['to_timestamp'])
					# trends_data = get_trends(s, row['article_name'], tf )
					suggest_data = get_suggestions(s,row['article_name'])
					f.write(row['article_name'] + '\t' + suggest_data + '\n')
					time.sleep(random.randint(1,3))
					j = 0
					break
			#		i += 1
				except KeyError:
					# try:
					# 	trends_data = get_trends(s, row['article_name'])
					# 	f.write(row['article_id'] + '\t' + row['article_name'] + '\t' + trends_data + '\n')
					# except:
					f.write(row['article_name'] + '\t' + str(sys.exc_info()[0]) + '\n')
					time.sleep(random.randint(1,3))
					j = 0
					break
				#	i += 1
				except ValueError:

					if j >=5:
						file.write("----------------------------------\n") 
						print "----------------------------------"
						file.write(time.strftime("%D %H:%M", time.localtime(int(time.time())))+'\n')
						print time.strftime("%D %H:%M", time.localtime(int(time.time())))
						file.write("-------Sleep for 30 minutes-------\n") 
						print "-------Sleep for 30 minutes-------"
						time.sleep(1800)
						i = 1
						continue
					else:
						if i < 5:
							s = trends_session(google_username, google_password)
							i+=1
							continue
						if i >= 5:
							f.write(row['article_name'] + '\t' + str(sys.exc_info()[0]) + '\n')
							j+=1
							break
						

start_time = time.time()


google_username = # Enter your Google username here
google_password = # Enter your Google password here
input_article_file = #Enter a file name of a tsv with a column of article_name. You can type in any file name under "data/articles" directory.
output_file = # Enter your desired output file name
save_data((google_username,google_password,"../data/articles/" + input_article_file,output_file))

print "--- %s seconds ---" % (time.time() - start_time)



		