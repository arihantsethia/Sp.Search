import json, os
import re, nltk

dataset_dir = 'dataset/'

def highlight_relevant_text(html_string, query_string):
	content = nltk.clean_html(html_string)
	count = 0
	context = ''
	#rval = []
	for match in re.finditer(query_string, content):
		if count>2:
			break;
		
    	s = match.start()
    	e = match.end()
    	#too sleepy.this is a brute approach but shoudl work.avoiding splitting the whole document as that maybe slow
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
		#rval.append(context)
	return context#rval

def get_title(html_string):
	return re.search("<title>.*</title>",html_string).group(0)[7:-8]

def generate_json_rank_list(rank_list, query_string, start_rank):
	rank_list = '['
	rank = start_rank
	for doc_id, score in rank_list.items():
		folder_numer = int(doc_id)/10000
		with open(dataset_dir+str(folder_numer)+str(doc_id)) as content_file:
			html_content = content_file.read()
		data = {}
		
		data['title'] = get_title(html_content)
		data['url'] = ''
		data['score'] = str(score)
		data['rank'] = str(rank)
		data['snippet'] = highlight_relevant_text(html_string)
		rank += 1
		rank_list += json.dumps(data) + ','
	rank_list += ']'
	return rank_list

def generate_json(query_id, rank_list, query_string, scoring_method, processing_time, results_length, start_rank):
	result = dict()
	result['query_id'] = str(query_id)
	result['scoring_method'] = str(scoring_method)
	result['time'] = str(processing_time)
	result['number_of_result'] = str(results_length)
	result['rank_list'] = generate_json_rank_list(rank_list, query_string, start_rank)

