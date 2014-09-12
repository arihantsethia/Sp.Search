import urllib, re, os
from nltk import PorterStemmer
from lxml import html
from lxml.html.clean import clean_html
from bs4 import BeautifulSoup, Comment


class HtmlParser:
	contains_stop_words = None
	stop_words_file = None
	stop_words = None
	to_stem = None
	porter = None

	def get_stop_words(self):
		'''get stop_words from the stop_words file'''
		f=open(os.path.join(os.path.dirname(__file__), self.stop_words_file), 'r')
		stop_words=[line.rstrip() for line in f]
		self.stop_words=dict.fromkeys(stop_words)
		f.close()

	def get_terms(self):
		html_string = self.html_string.lower()
		html_string = re.sub(r'[^a-z0-9 ]',' ',html_string)
		html_string = html_string.split()
		if(not self.contains_stop_words) :
			html_string = [x for x in html_string if x not in self.stop_words]
		if self.to_stem:
			htmlString = [ porter.stem(word) for word in htmlString]
		return html_string

	def parse_html(self, html_string):
		html_tree = clean_html(html.fromstring(html_string.replace("<br>","")))
		self.html_string = html_tree.text_content()

	def parse_html_BeautifulSoup(self, html_string):
		soup = BeautifulSoup(html_string)
		[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
		self.html_string = soup.getText()

	def __init__ (self, stop_words_file = "stopWords.txt", contains_stop_words=False, to_stem = True):
		self.contains_stop_words = contains_stop_words
		self.html_string = ""
		self.stop_words_file = stop_words_file
		self.to_stem = to_stem
		self.get_stop_words()
		self.porter = PorterStemmer()
		return
