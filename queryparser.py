
# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------

tokens = (
    'NAME',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN', 'QUOTE', 
    )

# Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_QUOTE   = r'"'
t_NAME    = r'[a-zA-Z0-9_]  [a-zA-Z0-9_]*'

mode = 1


# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import queryeval
import ply.lex as lex
lex.lex()



# Parsing rules

precedence = (
    ('left', 'DIVIDE'),
    ('left','PLUS'),
    ('left', 'MINUS'),
    ('left','TIMES'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]

def p_statement_end(t):
    'words : NAME'
    t[0] = t[1]

def p_statement_words(t):
    'words : NAME words'
              
    t[0] = t[1] + " " + t[2]
    print t[0]



def p_statement_expr(t):
    'statement : expression'
    #print(t[1])
    queryeval.getRanking(t[1])
    t[0] = t[1]

def p_expression_phrase(t):
    'expression : QUOTE words QUOTE'
    if mode==1:
	res1 = queryeval.get_tfscore_phrase(t[2])
    elif mode==2:
	res1 = queryeval.get_tfidfscore_phrase(t[2])
    elif mode==3:
	res1 = queryeval.get_bm25score_phrase(t[2])
	
    t[0] = res1
    

def p_expression_or(t):
    'expression : expression DIVIDE expression'

    print "Evaluation OR  " 
    
    
    res1 = t[1]
    res2 = t[3]
    
    res3 = {}

    for document in res1:
        #print tup

        res3[document] = res1[document]
    for document in res2:
        if res1.has_key(document):
            res3[document] += res2[document]
        else:
            res3[document] = res2[document]

    #print res1
    #print res2
    #print res3    
    t[0] = res3
    print t[0]
    print len(t[0]) 

def p_expression_and(t):
    'expression : expression PLUS expression'

    print "Evaluation AND  " 
    
    
    res1 = t[1]
    res2 = t[3]
    
    res3 = {}

    for document in res1:
        if res2.has_key(document):
            res3[document] = res1[document] + res2[document]

   
    #print res2
    #print res3    
    t[0] = res3
    print t[0]
    print len(t[0]) 

def p_expression_not(t):
    'expression : expression MINUS expression'

    print "Evaluation NOT  " 
    
    
    res1 = t[1]
    res2 = t[3]
    
    res3 = {}

    for document in res1:
        if not(res2.has_key(document)):
            res3[document] = res1[document]

   
    #print res2
    #print res3    
    t[0] = res3
    print t[0]
    print len(t[0]) 






def p_expression_binop(t):
    '''expression : expression TIMES expression'''
    if t[2] == '+'  : print "evaluating " + str(t[1]) + " + " + str(t[3])
    elif t[2] == '-': print "evaluating " + str(t[1]) + " - "  +str(t[3])
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_name(t):
    'expression : NAME'
    if mode==1:
	t[0] =queryeval.get_tfscore(t[1])
    elif mode==2:
	t[0] =queryeval.get_tfidfscore(t[1])
    elif mode==3:
	t[0] =queryeval.get_bm25score(t[1])
		
    print len(t[0])
    
# def p_expression_name(t):
#     'expression : NAME's
#     try:
#         t[0] = names[t[1]]
#     except LookupError:
#         print("Undefined name '%s'" % t[1])
#         t[0] = 0

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
	mode = int(raw_input("Enter mode 1(tf) 2(tfidf) 3(bm25)"))    
        s = raw_input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    yacc.parse(s)