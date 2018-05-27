import csv
from datetime import datetime
import json

'''
This script is to generate a json file to summarize Wiki talk page data for biography samples.

'''

input_file = "" # Enter a json file name of grouped talk page info. E.g: "wiki_talk_groups_sample.json" under "data/Biography"


output_file = "" #Enter desired output file name or path here (.json)
				# one example of desired output is "data/Biography/wiki_talk_stats_sample.json"


month = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
def get_date(date):
	day = date.split()[1]
	mon = date.split()[2][:3]
	year = date.split()[3]
	return year + "-" + month[mon] + "-" + day

def convert_date(date):
	date = datetime.strptime(date, "%Y-%m-%d")
	return date



f1 = open(output_file,"w")

def write_files(final_output):
	for article_id in final_output:
		for relweek in final_output[article_id]:
			num_newedtiors = final_output[article_id][relweek]["#neweditors"]
			num_newedtiors_comment = final_output[article_id][relweek]["#neweditors_comment"]
			if num_newedtiors != 0 :
				final_output[article_id][relweek]["#editis_per_neweditor"] = 1.0*num_newedtiors_comment/num_newedtiors
			else:
				final_output[article_id][relweek]["#editis_per_neweditor"] = "NA"

	f1.write(json.dumps(final_output) + "\n")

selected_lst = [line.strip() for line in open("../data/Biography/matched_control_article_id_part1.csv","r").readlines()]

treated_newcommers_dict = {}

with open("../data/Biography/biography_main_metric.csv") as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		if row["ArticleId"] not in selected_lst:
			article_id = int(row["ArticleId"])
			relweek = row["RelWeek"]
			if article_id not in treated_newcommers_dict:
				treated_newcommers_dict[article_id] = {}
			if relweek not in treated_newcommers_dict[article_id]:
				treated_newcommers_dict[article_id][relweek] = {}
			treated_newcommers_dict[article_id][relweek]["startdate"] = row["StartDate"]
			treated_newcommers_dict[article_id][relweek]["enddate"] = row["EndDate"]
			treated_newcommers_dict[article_id][relweek]["neweditors"] = json.loads(row["NewEditorSet"])
			treated_newcommers_dict[article_id][relweek]["retentiondate"] = row["RetentionEndDate"]
print "======Loading treated_main_metric completed.======"
#print treated_newcommers_dict[24397]


f = open("wiki_talk_groups_sample.json","r")

final_output = {}
exist_id = []




for line in f.readlines():

	talk_data = json.loads(line)
	article_id = talk_data["article_id"]
	if article_id in treated_newcommers_dict:
		topic_id = talk_data["topic_id"]
		article_name = talk_data["article"]
		date = get_date(talk_data["time"])
		user = talk_data["user"]
		newcomer_info = treated_newcommers_dict[article_id]

		if article_id not in exist_id:
			exist_id.append(article_id)
			print len(exist_id)
		#	print final_output
			if len(final_output)>0:
				write_files(final_output)
			final_output = {}


		if article_id not in final_output:
			final_output[article_id] = {}

		for week in newcomer_info:
			startdate = newcomer_info[week]["startdate"]
			enddate  = newcomer_info[week]["enddate"]
			retentiondate = newcomer_info[week]["retentiondate"]
			if week not in final_output[article_id]:
				final_output[article_id][week] = {}
				final_output[article_id][week]["#total_comment"] = 0
				final_output[article_id][week]["#neweditors"] = len(newcomer_info[week]["neweditors"])
				final_output[article_id][week]["#reply_neweditors"] = 0
				final_output[article_id][week]["#neweditors_comment"] = 0
				final_output[article_id][week]["newcomer_posts"]= []

			if convert_date(date) >= convert_date(startdate) and convert_date(date)<=convert_date(enddate):

				# Count #total_comment
				final_output[article_id][week]["#total_comment"] += 1

				# Count #new editors comment and record the newcommers post
				if user in newcomer_info[week]["neweditors"]:
					final_output[article_id][week]["#neweditors_comment"] += 1
					final_output[article_id][week]["newcomer_posts"].append((user,date,topic_id,retentiondate))
write_files(final_output)









			
