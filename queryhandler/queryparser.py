import ply.lex as lex
import ply.yacc as yacc
import queryeval
import re
from nltk import PorterStemmer



tokens = (
	'NAME',
	'PLUS','MINUS','DIVIDE',
	'LPAREN','RPAREN', 'QUOTE', 
	)

# Tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_QUOTE   = r'"'
t_NAME    = r'[a-zA-Z0-9_][a-zA-Z0-9_]*'

# Ignored characters
t_ignore = " \t"
gmode = 0
query_eval = None

def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")
	
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)
	
# Build the lexer
lex.lex()

# Parsing rules
precedence = (
	('left', 'DIVIDE'),
	('left','PLUS'),
	('left', 'MINUS')
	)

names = dict()

def p_statement_expr(t):
	'statement : expression'
	t[0] = query_eval.get_ranking(t[1])
	

def p_statement_end(t):
	'words : NAME'
	t[0] = t[1]

def p_statement_words(t):
	'words : NAME words'              
	t[0] = t[1] + " " + t[2]


def p_expression_phrase(t):
	'''expression : QUOTE words QUOTE
					| QUOTE QUOTE'''
	if t[2]=="\"":
		t[0]=dict()
	else:
		if gmode==1:
			res1 = query_eval.get_tf_score_phrase(t[2])
		elif gmode==2:
			res1 = query_eval.get_tfidf_score_phrase(t[2])
		elif gmode==3:
			res1 = query_eval.get_bm25_score_phrase(t[2])
		t[0] = res1

def p_expression_or(t):
	'expression : expression DIVIDE expression'
	res1 = t[1]
	res2 = t[3]    
	res3 = dict()

	for document in res1:
		res3[document] = res1[document]
	for document in res2:
		if res1.has_key(document):
			res3[document] += res2[document]
		else:
			res3[document] = res2[document]
	t[0] = res3

def p_expression_and(t):
	'expression : expression PLUS expression'
	res1 = t[1]
	res2 = t[3]
	res3 = dict()

	for document in res1:
		if res2.has_key(document):
			res3[document] = res1[document] + res2[document]

	t[0] = res3

def p_expression_not(t):
	'expression : expression MINUS expression'
	res1 = t[1]
	res2 = t[3]
	res3 = dict()

	for document in res1:
		if not(res2.has_key(document)):
			res3[document] = res1[document]

	t[0] = res3

def p_expression_group(t):
	'expression : LPAREN expression RPAREN'
	t[0] = t[2]
def p_expression_empty(t):
	'expression : '
	t[0]=dict()

def p_expression_name(t):
	'expression : NAME'
	if gmode==1:
		t[0] =query_eval.get_tf_score(t[1])
	elif gmode==2:
		t[0] =query_eval.get_tfidf_score(t[1])
	elif gmode==3:
		t[0] =query_eval.get_bm25_score(t[1])

def p_error(t):
	print("Syntax error at '%s'" % t.value)

yacc.yacc()

class QueryParser:
	def __init__(self, indices_list, stop_words_file, k, b):
		self.query_evaluator = queryeval.QueryEvaluator(stop_words_file, k, b)
		self.query_evaluator.load_indices(indices_list)
		self.query_evaluator.load_length_data()
		self.get_stopwords(stop_words_file)
		self.porter = PorterStemmer()

	def get_stopwords(self, stop_words_file):
		'''get stopwords from the stopwords file'''
		f=open(stop_words_file, 'r')
		stopWords=[line.rstrip() for line in f]
		self.stop_words=dict.fromkeys(stopWords)
		f.close()

	def get_terms(self, query_string, include_stop_words, include_stemming):
		lex.lex()
		lex.input(query_string)
		terms=[]
		new_string=""
		quote = False
		last_name = False
		
		while 1:
			tok = lex.token()
			if not tok: break
			if tok.type=="NAME":
				if last_name==True:
					if (not quote):
						new_string+="/"
				last_name=True
				word=tok.value
				if (not include_stop_words):
					if tok.value in  self.stop_words:
						continue
				if (include_stemming):
					tok.value = self.porter.stem(tok.value)
				terms.append(tok.value)
				
			elif tok.type=="QUOTE":
				if last_name==True:
					if (not quote):
						new_string+="/"
				if (not quote):
					last_name=False
					quote = True
				else:
					quote = False
				
				
			elif tok.type=="LPAREN":
				if last_name==True:
					if (not quote):
						new_string+="/"
				last_name=False
				
			elif tok.type=="RPAREN":
				last_name = True
				
			else:
				last_name = False
				
			
			new_string+=tok.value+" "

		return (new_string, terms)


	

	def get_rank(self, query_string, mode, include_stop_words, include_stemming):
		query_string = query_string.lower()
		tup = self.get_terms(query_string, include_stop_words, include_stemming)
		list_of_words = tup[1]
		self.query_evaluator.load_query_items(list_of_words, include_stop_words, include_stemming)
		query_string = tup[0]
		yacc.yacc()
		global gmode
		global query_eval
		query_eval = self.query_evaluator
		gmode = mode
		print query_string
		return yacc.parse(query_string)
	
		
		
