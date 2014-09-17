import json, os
import re, nltk

dataset_dir = '/home/arihant/Github/Sp.Search/static/dataset/'
titleRE = re.compile("<title>(.+?)</title>")

def clean_string(query_string):
	query_string = query_string.lower()
	query_string = re.sub(r'[^a-z0-9 ]',' ',query_string)
	return query_string

def clean_string(query_string):
	query_string = query_string.lower()
	query_string = re.sub(r'[^a-z0-9 ]',' ',query_string)
	return query_string

def highlight_relevant_text(html_string, query_string):
	content = nltk.clean_html(html_string)
	count = 0
	context = ''
	for match in re.finditer(query_string, content):
		if count>2:
			break;
		s = match.start()
		e = match.end()
		if (s-100>=0):
			if e+100<len(content):
				words = content[s-100:e+100].split()
			else:
				words = content[s-100:len(content)].split()
		else:
			if e+100<len(content):
				words = content[0:e+100].split()
			else:
				words = content[0:len(content)].split()

		i = words.index(query_string)
		if i-5>=0:
			if i+5<len(words):
				context += ' '.join(words[i-5:i+5])+'...'
			else:
				context += ' '.join(words[i-5:len(words)])+'...'
		else:
			if i+5<len(words):
				context += ' '.join(words[0:i+5])+'...'
			else:
				context += ' '.join(words[0:len(words)])+'...'
		count+=1
	return context

def get_title(html_string):
	if titleRE.search(html_string) is None:
		return "Title"
	data = titleRE.search(html_string).group(1)
	info = (data[:45] + '..') if len(data) > 45 else data
	return info

def generate_json_rank_list(rank_list, query_string, start_rank):
	rank_list_json = []
	rank = start_rank
	for (doc_id, score) in rank_list:
		folder_numer = int(doc_id)/10000
		with open(dataset_dir+str(folder_numer)+'/'+str(doc_id)) as content_file:
			html_content = content_file.read().lower()
		data = {}
		data['title'] = get_title(html_content).decode('utf8','replace').encode('utf8')
		data['url'] = 'http://172.16.27.36:5000/static/dataset/'+ str(int(doc_id)/10000)+'/'+str(doc_id)
		data['score'] = str(score)
		data['rank'] = str(rank)
		data['snippet'] = ' '
		#data['snippet'] = highlight_relevant_text(query_string, clean_string(query_string))
		rank += 1
		rank_list_json.append(data)
	return rank_list_json

def generate_json(query_id, rank_list, query_string, scoring_method, processing_time, results_length, start_rank):
	result = dict()
	result['query_id'] = str(query_id)
	result['scoring_method'] = str(scoring_method)
	result['start_rank'] = int(start_rank)
	result['time'] = str(processing_time)
	result['total_result'] = int(results_length)
	result['results'] = generate_json_rank_list(rank_list, query_string, start_rank)
	return json.dumps(result)