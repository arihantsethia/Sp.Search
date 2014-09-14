#!/usr/bin/python
import os, chardet, urllib, string
from indexer import indexbuilder, htmlparser, indexmerger

root_dir = '/home/simrat/Documents/IRProject/Sp.Search/'
datset_dir = root_dir+ 'dataset/'
index_dir = root_dir + 'indices/'
error_dir = root_dir + 'errors/'
errorLogFile =error_dir + 'error.log'

parser = htmlparser.HtmlParser()

def setup():
	if not os.path.exists(index_dir):
		os.makedirs(index_dir)
	if not os.path.exists(error_dir):
		os.makedirs(error_dir)

def merge_error_files(folder_name, new_file_name):
	new_file = open(new_file_name,'a')
	curr_dir = folder_name
	dir_lists=os.listdir(curr_dir)
	dir_lists.sort()
	for file_name in dir_lists:
		file_path = os.path.join(curr_dir,file_name)
		file_content = ""
		with open(file_path, 'r') as content_file:
			file_content = content_file.read().strip()
		if(len(file_content) > 0 and file_content[-1]!= '\n'):
			file_content+='\n'
		new_file.write(file_content)
	new_file.close()

def merge_index_files():
	indexMerger = indexmerger.IndexMerger(index_dir)
	while(len(os.listdir(index_dir))>1):
		indexMerger.merge_all()

def iterate_over_folders(startFolder, endFolder):
	for folderNumber in xrange(startFolder,endFolder):
		indexBuilder = indexbuilder.IndexBuilder()
		errorLog = open(errorLogFile+str(folderNumber), 'w')
		curr_dir = datset_dir + str(folderNumber)
		print curr_dir
		dir_lists=os.listdir(curr_dir)
		dir_lists.sort()
		for file_name in dir_lists:
			file_path = os.path.join(curr_dir,file_name)
			file_content = ""
			with open(file_path, 'r') as content_file:
				file_content = content_file.read().strip()
			try:
				if(len(file_content)>0):
					parser.parse_html(file_content.decode('utf-8','replace').encode('utf-8'))
					wordList = parser.get_terms()
					indexBuilder.build_index(int(file_name), wordList)
			except:
				errorLog.write(file_path+"\n")
		indexBuilder.write_index(index_dir+('%03d' % folderNumber))
		indexBuilder.delete_index()
		errorLog.close()

startFolder = int(input("Enter start folder : "))
endFolder = int(input("Enter end folder : "))

setup()
iterate_over_folders(startFolder, endFolder)
merge_index_files()
merge_error_files(root_dir+'errors', errorLogFile)
