'''
Python Code Scanner(Lexical Parser)
description: convert string to WORD list
'''

import ply.lex as lex

# > Token list:
tokens=(
#\s
	'IGNORE',
	'TAB',
	'newline',
#reserved words
	'ASSIGN',
	'DEF',
	'RETURN',
	'IF',
	'ELSE',
	'ELIF',
	'WHILE',
#name
	'ID',
#const
	'NUMBER',
	'STRING',
#sign
	'COLON',
	'LBRACKET',
	'RBRACKET',
	'COMMA',
#opcode
	##BINARY BOOL
	'BOOL',
	##LOGIC OP
	'LOGIC',
	##BINARY OP
	'TERMOP',
	'FACTOROP'
)

def t_error(token):
	raise Error('can\'t recogenize key word')
	pass
##SPACEs
def t_newline(token):
	r'\n'
	return token
def t_TAB(token):
	r'\t'
	return token
def t_IGNORE(token):
	r'\s'
	pass

##SYMBOLs
def t_COLON(token):
	':'
	return token
def t_LBRACKET(token):
	'\('
	return token
def t_RBRACKET(token):
	'\)'
	return token
def t_COMMA(token):
	','
	return token
##BOOL
def t_BOOL(token):
	r'[><]|=='
	return token

##LOGIC
def t_LOGIC(token):
	r'NOT|AND|OR'
	return token

##OPERATION
def t_TERMOP(token):
	r'[+-]'
	return token
def t_FACTOROP(token):
	r'[*/%]'
	return token

##RESERVED WORDS
def t_RETURN(token):
	'return'
	return token
def t_ASSIGN(token):
	'='
	return token
def t_DEF(token):
	'def'
	return token
def t_IF(token):
	'if'
	return token
def t_ELSE(token):
	'else'
	return token
def t_ELIF(token):
	'elif'
	return token
def t_WHILE(token):
	'while'
	return token

##name
def t_ID(token):
	r'[a-zA-Z][0-9a-zA-Z]*'
	return token
def t_NUMBER(token):
	r'[0-9]+'
	token.value=int(token.value)
	return token
def t_STRING(token):
	r'"[^"]*"'
	token.value=token.value[1:-1]
	return token


class Lexer(object):
	def __init__(self, data):
		self._lexer=lex.lex()
		self._data=data
	def lexerNewInput(self, data):
		self._data=data
	def lexerStart(self):
		self._lexer.input(self._data)
		tokenList=[]
		while True:
			tok=self._lexer.token()
			if not tok:
				break
			tokenInfo=(tok.__dict__['type'],tok.__dict__['value'])
			tokenList.append(tokenInfo)
		tokenList.append(('END','$$'))
		return tokenList

def tokenOf(data):
	lexer=Lexer(data)
	log=lexer.lexerStart()
	#print(log)
	return log

