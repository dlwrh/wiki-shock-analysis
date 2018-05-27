import time
import csv
from pytrends.request import TrendReq
import pandas
import sys
from multiprocessing import Pool as ThreadPool 
import random
import wikipedia

'''
This script is to collect trends data and wiki summary of articles.

'''

def time_convert(json_ts):
	t = time.strftime("%D %H:%M", time.localtime(int(json_ts)))
	year = '20' + t[6:8]
	month = t[:2]
	day = t[3:5]
	return year +'-'+ month +'-'+ day

def trends_session(google_username , google_password ):
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

def get_summary(article_id)
	pageid = int(article_id)
	contents = []
	try:
		content = wikipedia.page(pageid=pageid).content.encode('utf8')
		summary = content.strip().split('\n')[0]
		contents.append(summary)
	except:
		contents.append("")
	return contents

def save_data(tup):
	google_username, google_password, input_article_file, output_file = tup
	s = trends_session(google_username = google_username, google_password = google_password)

	f = open(output_file,'a')
	file = open("trend1_log.txt",'a')
	with open(input_article_file) as tsvfile:
		reader = csv.DictReader(tsvfile, delimiter='\t')
		for row in reader:
			i = 1
			while i <= 5:
				try:
					tf = "2004-01-01 2017-07-31" # Timeframe for GT data. Currently it will return monthly data; Narrow the time frame can get weekly or daily data.

					trends_data = get_trends(s, row['mid'], tf )
					contents = get_summary(row["article_id"])
					f.write(row['article_id']+'\t'+row['article_name'] + '\t' + row['article_type'] + '\t' + trends_data + json.dumps(contents) + '\n')
					time.sleep(random.randint(1,3))
					j = 0
					break

				except KeyError:

					f.write(row['article_id'] +'\t'+ row['article_name'] + '\t' + row['article_type'] + '\t' + str(sys.exc_info()[0]) + '\n')
					time.sleep(random.randint(1,3))
					j = 0
					break

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
							f.write(row['article_id'] + '\t' + row['article_name'] + '\t' + row['article_type'] + '\t' + str(sys.exc_info()[0]) + '\n')
							j+=1
							break
						

start_time = time.time()

google_username = # Enter your Google username here
google_password = # Enter your Google password here
input_article_file = #Enter the file name of a tsv under "data/trends" directory with columns of article_id, article_name, article_type and mid. E.g: "politician_match_data_merged_mid.tsv".
output_file = # Enter your desired output file name or path

save_data((google_username,google_password,"../data/trends/" + input_article_file,output_file))


print "--- %s seconds ---" % (time.time() - start_time)



		