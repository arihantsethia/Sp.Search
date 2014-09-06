import urllib, re
from nltk import PorterStemmer
from nltk.corpus import stopwords
from lxml import html
from lxml.html.clean import clean_html
from bs4 import BeautifulSoup, Comment

porter = PorterStemmer()

class HtmlParser:
    containsStopWords = None
    stopWordsFile = None
    stopWords = None

    def getStopwords(self):
        '''get stopwords from the stopwords file'''
        f=open(self.stopWordsFile, 'r')
        stopWords=[line.rstrip() for line in f]
        self.stopWords=dict.fromkeys(stopWords)
        f.close()

    def getTerms(self):
        htmlString = self.htmlString.lower()
        htmlString = re.sub(r'[^a-z0-9 ]',' ',htmlString) #put spaces instead of non-alphanumeric characters
        htmlString = htmlString.split()
        if(not self.containsStopWords) :
            htmlString = [x for x in htmlString if x not in self.stopWords]  #eliminate the stopwords
        htmlString = [ porter.stem(word) for word in htmlString]
        return htmlString

    def parseHtml(self, htmlString):
        htmlTree = clean_html(html.fromstring(htmlString.replace("<br>","")))
        self.htmlString = htmlTree.text_content()

    def parseHtmlBeautifulSoup(self, htmlString):
        soup = BeautifulSoup(htmlString)
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        self.htmlString = soup.getText()

    def __init__ (self, _stopWordsFile = "stopWords.txt", _containsStopWords=False):
        self.containsStopWords = _containsStopWords
        self.htmlString = ""
        self.stopWordsFile = _stopWordsFile;
        self.getStopwords()
        return
