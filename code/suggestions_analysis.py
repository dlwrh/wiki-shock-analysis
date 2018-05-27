import json

'''
This script is to analyze the suggestion data returned by Google Trends API and filter out the mid of good articles.

A good article is: the suggestion title matches article's name; AND the suggestions' type is in the selected profession list.

Selected profession lists are the two txt files under "data/suggestion" directory.

'''


def write_type_frequency(f,output_name):
	type_freq = {}
	valid_count = 0
	for line in f.readlines():
		suggest_str = line.strip().split('\t')[1]
		try:
			suggest_lst = json.loads(suggest_str)
			query = line.strip().split('\t')[0]
			types = [el['type'] for el in suggest_lst if query == el['title']]
			if len(types)>0:
				valid_count += 1
			for t in types:
				if t not in type_freq:
					type_freq[t] = 0
				type_freq[t] += 1

		except:
			continue


	f1 = open(output_name,"w")
	for ty in sorted(type_freq, key = lambda x: type_freq[x], reverse = True):
		f1.write((ty).encode('utf8')+'\t'+str(type_freq[ty])+'\n')
	f1.close()
	print "valid_count: ", valid_count
	print "types_count: ", len(type_freq)

def remove_duplicated(f,output):
	f7 = open(output,"w")
	count = 0
	data = f.readlines()
	unique_data = list(set(data))
	for line in unique_data:
		f7.write(line)
		count += 1
	print count

def find_query_match_title(f, output = None):
	count = 0 
	match_count = {} # {query: [types that match query] }
	count_summary = {} # {count: [query + suggestions]}
	
	for line in f.readlines():

		try:
			query = line.strip().split('\t')[0]
			suggest_lst = json.loads(line.strip().split('\t')[1])
			matchlist = []
			for suggest in suggest_lst:
				# if suggest['type'] != 'Topic'and suggest['title'] == query.encode('utf8'):
				if suggest['title'] == query.encode('utf8') and suggest['type'] != 'Topic':
					matchlist.append(suggest['type'])
			
			if len(matchlist) > 0 :				
				if list(set(matchlist)) != ['Topic']:
					count += 1
					match_count[query] = matchlist
					if len(matchlist) not in count_summary:
						count_summary[len(matchlist)] = []
					count_summary[len(matchlist)].append(line)
		except:
			continue
	if output != None:
		f9 = open(output, "w")
		for i in sorted(count_summary):
			for line in count_summary[i]:
				f9.write(line)

	print count
	print len(match_count)
	print {i:len(count_summary[i]) for i in count_summary.keys()}

# Function to detect whether there is a keyword of profession in a "type" string 
def common_profession(typestr,suggestion_file):
	f12 = open(suggestion_file.split("_")[0]+"_profession_lst.txt","r")
	prof_lst = [line.strip().lower() for line in f12.readlines()]

	for word in prof_lst:
		if word in typestr.lower():
			return True,word
	return False,False

# Generate file with a list of "query profession_keyword mid"
def extract_profession(f,output,suggestion_file):
	f11 = open(output,"w")
	for line in f.readlines():
		query = line.strip().split('\t')[0]
		suggest_lst = json.loads(line.strip().split('\t')[1])
		for suggest in suggest_lst:
			if query.encode('utf8') == suggest['title']:
				match,word = common_profession(suggest['type'],suggestion_file)
				if match:
					f11.write(suggest['title'].encode('utf8') + '\t' + suggest['type'].encode('utf8') +'\t' + suggest['mid'].encode('utf8') +'\n')

suggestion_file = # Enter the suggestion file name. E.g: "politician_suggestions.tsv"

f = open ("../data/suggestions/" + suggestion_file,"r")
find_query_match_title(f,"query_match_title.tsv")

f1 = open("query_match_title.tsv","r")
remove_duplicated(f1,suggestion_file[:-4]+ "_with_GT_topic.tsv")

f2 = open("match_data_without_dup.tsv","r")
extract_profession(f2,suggestion_file.split("_")[0] + "match_data_mid.tsv",suggestion_file)

