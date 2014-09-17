import os

cache_dir = 'cache/'

def is_cached(query_id):
	if os.path.isfile(cache_dir+query_id):
		return True
	return False

def cache_result(query_id, rank_list):
	fp = open(cache_dir+query_id,'w')
	for (doc_id, score) in rank_list:
		line = str(doc_id) + ' ' + str(score)+'\n'
		fp.write(line)
	fp.close()

def get_cached(query_id, start_rank, num_results):
	if os.path.isfile(cache_dir+query_id):
		results_list = []
		fp = open(cache_dir+query_id)
		for i, line in enumerate(fp):
			if i > start_rank and i <= (start_rank + num_results):
				line_parts = line.split()
				results_list.append((line_parts[0],line_parts[1]))
			elif i > (start_rank + num_results):
				break
		fp.close()
		return results_list
	return None

def cache_result_stats(query_id, results_length, processing_time):
	fp = open(cache_dir+query_id+'.stats','w')
	line = str(results_length) + ' ' + str(processing_time)+'\n'
	fp.write(line)
	fp.close()

def get_cached_stats(query_id):
	if os.path.isfile(cache_dir+query_id+'.stats'):
		result = {}
		with open(cache_dir+query_id+'.stats', 'r') as content_file:
			content = content_file.read()
		content = content.split()
		result['results_length'] = content[0]
		result['processing_time'] = content[1]
		return result
	return None