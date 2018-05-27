import wikipedia
import re
from bs4 import BeautifulSoup
import requests
import json
import sys


input_file = "" # Enter "scientist_shock_tf.tsv" for academics or "politician_shock_tf.tsv" for politicians.

output_file = "" # Enter name or path of output file (.json)


def has_title_and_user(tag):
	return tag.has_attr("title") and tag["title"].startswith("User:")

def has_title_and_archive(tag):
	return tag.has_attr("title") and tag["title"].startswith("Talk:") and "Archive" in tag["title"] and "index" not in tag["title"]

def has_page_info(tag):
	return tag.has_attr("title") and tag["title"] == "More information about this page"

def has_pageid(tag):
	return tag.has_attr("id") and tag["id"] == "mw-pageinfo-article-id"

def get_talk_page_id(talk_page):
	try:
		page_info_url = "https://en.wikipedia.org/" + talk_page.find_all(has_page_info)[0]["href"]
		page_info_html = requests.get(page_info_url).text
		page_info = BeautifulSoup(page_info_html,"html.parser")
		talk_page_id = int(page_info.find_all(has_pageid)[0].find_all("td")[-1].get_text())
	except:
		talk_page_id = ""
	return talk_page_id

f = open("../data/trends" + input_file,"r")
f1 = open(output_file,"w")
f2 = open("error.tsv","w")

acc = 1
talk_count = 0
for line in f.readlines()[1:]:
	print "=====Processing {} /1078 articles ======".format(acc)
	try:
		pageid = int(line.strip().split("\t")[0])
		article_name = line.strip().split("\t")[1]
		page = wikipedia.page(pageid=pageid)
		article_url = page.url
		talk_url = "https://en.wikipedia.org/wiki/Talk:" + article_url.split("/")[-1]
		talk_page = BeautifulSoup(requests.get(talk_url).text,"html.parser")
	except:
		f2.write(line)
		continue

	archives_lst = ["https://en.wikipedia.org" + el["href"] for el in talk_page.find_all(has_title_and_archive)]
	url_lst = [talk_url] + archives_lst

	topic_id = 0
	for url in url_lst:
		res = requests.get(url)
		talk_html = res.text
		talk_page = BeautifulSoup(res.text,"html.parser")
		pattern = re.compile(r"[0-9]{2}:[0-9]{2}, [0-9]{1,2} (?:January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec) [0-9]{4} (?:\(UTC\))*")
		time_stamps = re.findall(pattern,talk_html)
		talk_segments = re.split(pattern,talk_html)
		talk_page_id = get_talk_page_id(talk_page)


		#for ts in time_stamps:
		for i in range(len(time_stamps)):
			talk_data = {}
			talk_data["article"] = article_name
			talk_data["time"] = time_stamps[i]
			talk_data["article_id"] = pageid
			talk_data["talk_page_id"] = talk_page_id
			html_segment = talk_segments[i]
			#for html_segment in talk_segments:
			try:
				if "</h2>" in html_segment:
					topic_id+=1
					soup = BeautifulSoup(html_segment.split("</h2>")[-1],"html.parser")
				else:
					soup = BeautifulSoup(html_segment,"html.parser")
				contents = soup.get_text().strip()
				if contents.startswith("."):
					contents = contents[1:].strip()
				talk_data["contents"] = contents
				talk_data["topic_id"] = topic_id
				talk_data["user"] = soup.find_all(has_title_and_user)[0].get_text()
				f1.write(json.dumps(talk_data) + "\n")

			except:
				continue
	acc += 1








		