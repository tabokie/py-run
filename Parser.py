'''
Python Syntax Parser
description: convert WORD list to a syntax tree
'''


class treeNode:
	def __init__(self,value):
		self.value=value
		self.sons=[]
		self.father=None
	def attach(self,codeList):
		#self.sons=nodeList
		for code in codeList:
			node=treeNode(code)
			self.sons.append(node)
			node.father=self
	def expand(self):
		if self.sons==[]:
			return self
		return [self.value,map(self.sons,expand)]
		
class Tree:
	
	def __init__(self,code="Tree"):
		self.root=treeNode(code)
	def append(self,node,value):
		value=treeNode(value)
		value.father=node
		node.sons.append(value)
	def print(self):
		full_list=self.root.expand
		print(full_list)

class SyntaxTree(Tree):

	def analyse(self,tokenlist):

		#syntax init
		ruleList=[["stmt_list"],#program[0]
		["stmt","stmt_list"],["None"],#stmt_list[1:2]
		["define_clause"],["function_clause"],["call_func"],["if_clause","else_clause"],["while_clause"],["return"],#stmt[3:8]
		["ID","ASSIGN","expr"],#define_clause[9]
		["DEF","ID","LBRACKET","id_list","RBRACKET","COLON","stmt_list"],#function_clause[10]
		["ID","LBRACKET","expr_list","RBRACKET"],#call_function[11]
		["IF","bool_expr","COLON","stmt_list"],#if_clause[12]
		["ELSE","COLON","stmt_list"],["ELIF","bool_expr","COLON","stmt_list","else_clause"],["None"],#else_clause[13:15]
		["WHILE","bool_expr","COLON","stmt_list"],#while_clause[16]
		["RETURN","expr"],#return[17]
		["bool_expr"],["value_expr"],#expr[18:19]
		["bool_single","bool_single_tail"],#bool_expr[20]
		["LOGIC","bool_single","bool_single_tail"],["None"],#bool_single_tail[21:22]
		["value_expr","BOOL","value_expr"],#bool_single[23]
		["term","term_tail"],#value_expr[24]
		["TERMOP","term","term_tail"],["None"],#term_tail[25:26]
		["LBRACKET","value_expr","RBRACKET"],["factor","factor_tail"],#term[27:28]
		["FACTOROP","factor","factor_tail"],["None"],#factor_tail[29:30]
		["LBRACKET","value_expr","RBRACKET"],["NUMBER"],["STRING"],["ID"],#factor[31:34]
		["COMMA","ID","id_list_tail"],["None"],["ID","id_list_tail"],#id_list(_tail)[35:37]
		["COMMA","expr","expr_list_tail"],["None"],["expr","expr_list_tail"]#expr_list(_tail)[38:40]
		]

		blockList=['program','stmt_list','stmt','expr','bool_expr',
		'bool_single_tail','bool_single','value_expr','term_tail',
		'term','factor_tail','factor','define_clause','function_clause',
		'call_func','if_clause','else_clause','while_clause','return','id_list_tail','id_list','expr_list_tail','expr_list']
		#encode blocklist
		blockDict={blockList[i]:i for i in range(len(blockList))}

		wordList=['ASSIGN','DEF','RETURN','IF','ELSE','ELIF','WHILE',
		'ID','NUMBER','STRING','END','BOOL','LOGIC','TERMOP','FACTOROP',
		'LBRACKET','RBRACKET','COLON','COMMA']
		wordDict={wordList[i]:i for i in range(len(wordList))}

		#expansion matrix
		matrix=[
		[-1,0,0,0,-1,-1,0,0,-1,-1,0,-1,-1,-1,-1,-1,-1,-1,-1],
		[-1,1,1,1,2,2,1,1,-1,-1,2,-1,-1,-1,-1,-1,-1,-1,-1],
		[-1,4,8,6,-1,-1,7,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
		[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,18,18,-1,-1,-1,-1,-1,-1],
		[-1,-1,-1,-1,-1,-1,-1,20,20,20,-1,-1,-1,-1,-1,20,-1,-1,-1],
		[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,21,-1,-1,-1,22,22,-1],
		[-1,-1,-1,-1,-1,-1,-1,23,23,23,-1,-1,-1,-1,-1,23,-1,-1,-1],
		[-1,-1,-1,-1,-1,-1,-1,24,24,24,-1,-1,-1,-1,-1,24,-1,-1,-1],
		[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,26,26,25,-1,-1,26,26,-1],
		[-1,-1,-1,-1,-1,-1,-1,28,28,28,-1,-1,-1,-1,-1,28,-1,-1,-1],
		[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,30,30,30,29,-1,30,30,-1],
		[-1,-1,-1,-1,-1,-1,-1,34,32,33,-1,-1,-1,-1,-1,31,-1,-1,-1],
		[-1,-1,-1,-1,-1,-1,-1,9,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
		[-1,10,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
		[-1,-1,-1,-1,-1,-1,-1,11,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
		[-1,-1,-1,12,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
		[-1,15,15,15,13,14,15,15,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
		[-1,-1,-1,-1,-1,-1,16,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
		[-1,-1,17,-1,-1,-1,17,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
		[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,36,-1,35],
		[-1,-1,-1,-1,-1,-1,-1,37,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
		[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,39,-1,38],
		[-1,-1,-1,-1,-1,-1,-1,40,40,40,-1,-1,-1,-1,-1,-1,-1,-1,-1]]


		clause_block=['stmt_list','function_clause','if_clause','else_clause','while_clause']
		line_end=['bool_single_tail','term_tail','factor_tail']
		stmt_follow={'ASSIGN':3,'LBRACKET':5}
		expr_follow={'BOOL':18,'newline':19}
		constList=['NUMBER','STRING','ID','BOOL','LOGIC','TERMOP','FACTOROP']

		noneNode=treeNode("None")

		#predict stmt_list as initial condition
		self.root.attach(['stmt_list'])
		curNode=self.root.sons[0]
		predict=[]
		predict+=self.root.sons

		#recording indentation
		tabStack=[0]
		curTab=0

		idx=-1 #track current token

		# > main scan
		for words in tokenlist:
			idx+=1
			name=words[0]
			while True:#match this word
				
				#handle end of clause
				if curNode.value=='None':
					predict.pop(0)
					if len(predict)>0:
						curNode=predict[0]
					else:
						break
				'''
				print('curNode:',curNode.value,curNode.father.value)
				for x in predict:
					print(x.value)
				print(words)
				'''
				#newline
				if name=='newline':
					if curNode.value in line_end:
						curNode.attach(['None'])
						predict.pop(0)
						curNode=predict[0]
					elif curNode.value=='stmt_list':
						curTab=0
						break
					continue

				#handle end of clause
				if curNode.value=='None':
					predict.pop(0)
					if len(predict)>0:
						curNode=predict[0]
					else:
						break

				#switch indentation
				if name == 'TAB':
					curTab+=1
					break
				if curTab > tabStack[-1]:
					#print('newTab',curTab)
					if curNode.value in clause_block:
						tabStack.append(curTab)
					else:
						raise Error("No Indentation match.(out)")

				while curTab < tabStack[-1]:
					tabStack.pop()
					if curNode.value=="stmt_list":
						curNode.attach(ruleList[2])
						predict.pop(0)
						predict=curNode.sons+predict
					if len(tabStack)<1:
						raise Error("Environment switch error")
				if curTab>tabStack[-1]:
					raise Error("No environment match")
				curNode=predict[0]

				#handle end of clause
				if curNode.value=='None':
					predict.pop(0)
					if len(predict)>0:
						curNode=predict[0]
					else:
						break

				#direct match
				if name==curNode.value:
					if name in constList:
						curNode.attach([words[1]])
					predict.pop(0)
					curNode=predict[0]
					break

				#handle end of clause
				if curNode.value=='None':
					predict.pop(0)
					if len(predict)>0:
						curNode=predict[0]
					else:
						break

				#matrix match
				code=matrix[blockDict[curNode.value]][wordDict[name]]
				if code>=0:
					curNode.attach(ruleList[code])
					predict.pop(0)
					predict=curNode.sons+predict
					curNode=predict[0]
					continue

				#handle end of clause
				if curNode.value=='None':
					predict.pop(0)
					if len(predict)>0:
						curNode=predict[0]
					else:
						break

				#no match
				#check follow
				j=idx+1
				while True:
					followWord=tokenlist[j][0]
					if curNode.value=='stmt':			
						if followWord in stmt_follow:
							followCode=stmt_follow[followWord]
							curNode.attach(ruleList[followCode])
							predict.pop(0)
							predict=curNode.sons+predict
							curNode=predict[0]
							break
					elif curNode.value=='expr':
						if followWord in expr_follow:
							followCode=expr_follow[followWord]
							curNode.attach(ruleList[followCode])
							predict.pop(0)
							predict=curNode.sons+predict
							curNode=predict[0]
							break
					j+=1
				continue


def syntaxOf(tokenList):
	syntaxTree=SyntaxTree("syntaxTree")
	syntaxTree.analyse(tokenList)
	return syntaxTree
