import ply.lex as lex
import ply.yacc as yacc
import queryeval

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
	query.getRanking(t[1])
	t[0] = t[1]

def p_statement_end(t):
	'words : NAME'
	t[0] = t[1]

def p_statement_words(t):
	'words : NAME words'              
	t[0] = t[1] + " " + t[2]

def p_expression_phrase(t):
	'expression : QUOTE words QUOTE'
	if mode==1:
		res1 = query.get_tfscore_phrase(t[2])
	elif mode==2:
		res1 = query.get_tfidfscore_phrase(t[2])
	elif mode==3:
		res1 = query.get_bm25score_phrase(t[2])
	t[0] = res1

def p_expression_or(t):
	'expression : expression DIVIDE expression'
	print "Evaluation OR " 
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
	print "Evaluation AND  " 
	res1 = t[1]
	res2 = t[3]
	res3 = dict()

	for document in res1:
		if res2.has_key(document):
			res3[document] = res1[document] + res2[document]

	t[0] = res3

def p_expression_not(t):
	'expression : expression MINUS expression'
	print "Evaluation NOT  " 
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

def p_expression_name(t):
	'expression : NAME'
	if mode==1:
		t[0] =query.get_tfscore(t[1])
	elif mode==2:
		t[0] =query.get_tfidfscore(t[1])
	elif mode==3:
		t[0] =query.get_bm25score(t[1])

def p_error(t):
	print("Syntax error at '%s'" % t.value)

yacc.yacc()

class QueryParser:
	def __init__(self, stop_words_file, total_number_of_documents, average_length, k, b):
		self.query_evaluator = queryeval.QueryEvaluator(stop_words_file, total_number_of_documents, average_length, k, b)
		self.query_evaluator.load_indices()

	def get_rank(self, query_string, mode):
		return