import json, os
dataset_dir = 'dataset/'

def highlight_relevant_text(html_string, query_string):
	return ''

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

