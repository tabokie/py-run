'''
Assembly Code Generator
description: convert syntax tree to instruction code
'''


class Asm:
	def __init__(self):
		self.func_dict={}
		self.reserved_name_dict={'RET':0}
		self.reserved_const_dict={'True':1,'False':0}
		self.opname_dict={'+':'ADD','-':'SUB','*':'MUL','/':'DIV','NOT':'NOT','AND':'AND','OR':'OR'}
		self.bool_dict={'>':1,'<':-1,'==':0}
		self.trap_list=["print","input"]
		self.asm={
			"instruction":[('JSR',0)],
			"const":[0,1],
			"name":['__RET__'],
			"environment":[(1,[])]
		}
	def run_tree(self,tree):
		def run_node(asmler,Node):
			'''
			print('>>>>>head:',Node.value)
			for i in Node.sons:
				print(i.value)
			'''
			ignore_list=['expr','stmt','stmt_list']
			name=Node.value
			if name in ignore_list:
				for subNode in Node.sons:
					run_node(asmler,subNode)
			elif name=='define_clause':
				if len(Node.sons)==3:
					idName=Node.sons[0].sons[0].value
					run_node(asmler,Node.sons[2])##expr
					if idName in asmler.asm['name']:
						opcode=asmler.asm['name'].index(idName) 
					else:
						asmler.asm['name'].append(idName)
						opcode=len(asmler.asm['name'])-1
					asmler.asm['instruction'].append(('STORE_NAME',opcode))
					return
				else:
					raise Error('define_clause subnode number error')
			elif name=='if_clause':
				if len(Node.sons)==4:
					run_node(asmler,Node.sons[1])##bool_expr
					BRaddr=len(asmler.asm['instruction'])
					asmler.asm['instruction'].append(('BR',0,-1))##uncertain addr
					run_node(asmler,Node.sons[3])##stmt_list
					ELSEaddr=len(asmler.asm['instruction'])
					asmler.asm['instruction'][BRaddr]=('BR',0,ELSEaddr)
					return
				else:
					raise Error('if_clause subnode number error')
			elif name=='else_clause':
				clauseName=Node.sons[0].value
				if clauseName=='ELIF':
					run_node(asmler,Node.sons[1])##bool_expr
					BRaddr=len(asmler.asm['instruction'])
					asmler.asm['instruction'].append(('BR',0,-1))##uncertain addr
					run_node(asmler,Node.sons[3])##stmt_list
					ELSEaddr=len(asmler.asm['instruction'])
					asmler.asm['instruction'][BRaddr]=('BR',0,ELSEaddr)
					run_node(asmler,Node.sons[4])
					return
				elif clauseName=='ELSE':
					run_node(asmler,Node.sons[2])
					return
				else:
					raise Error('else_clause subnode name error')
			elif name=='while_clause':
				if len(Node.sons)==4:
					WHILEaddr=len(asmler.asm['instruction'])
					run_node(asmler,Node.sons[1])##bool_expr
					BRaddr=len(asmler.asm['instruction'])
					asmler.asm['instruction'].append(('BR',-1,-1))##uncertain addr
					run_node(asmler,Node.sons[3])##stmt_list
					asmler.asm['instruction'].append(('JUMP',WHILEaddr))
					opcode=len(asmler.asm['instruction'])
					asmler.asm['instruction'][BEaddr]=('BR',-1,opcode)
					return
				else:
					raise Error('while_clause subnode number error')
			elif name=='function_clause':
				if len(Node.sons)==7:
					JUMPaddr=len(asmler.asm['instruction'])
					asmler.asm['instruction'].append(('JUMP',-1))##uncertain addr
					##
					FUNCname=Node.sons[1].sons[0].value
					asmler.func_dict[FUNCname]=len(asmler.asm['environment'])
					FUNCaddr=len(asmler.asm['instruction'])
					FUNCargs=[]
					curNode=Node.sons[3]
					while curNode!=None:
						if curNode.value=='id_list':
							FUNCargs.append(curNode.sons[0].sons[0].value)
							curNode=curNode.sons[1]
							continue
						elif curNode.value=='id_list_tail':
							if len(curNode.sons)>2:
								FUNCargs.append(curNode.sons[1].sons[0].value)
								curNode=curNode.sons[2]
								continue
							else:
								break
					FUNCinfo=(FUNCaddr,FUNCargs)
					asmler.asm['environment'].append(FUNCinfo)
					run_node(asmler,Node.sons[6])
					##
					opcode=len(asmler.asm['instruction'])
					asmler.asm['instruction'][JUMPaddr]=('JUMP',opcode)
				else: raise Error('function_clause subnode number error')
			elif name=='call_func':
				if len(Node.sons)==4:
					#load args (inversely)
					curNode=Node.sons[2]
					nodeBuffer=[]
					while curNode!=None:
						if curNode.value=='expr_list':
							nodeBuffer.append(curNode.sons[0])
							curNode=curNode.sons[1]
							continue
						elif curNode.value=='expr_list_tail':
							if len(curNode.sons)>2:
								FUNCargs.append(curNode.sons[1])
								curNode=curNode.sons[2]
								continue
							else:
								break
					nodeBuffer=nodeBuffer[::-1]
					for exprNode in nodeBuffer:
						run_node(asmler,exprNode)
					#call func
					FUNCname=Node.sons[0].sons[0].value
					#print(FUNCname)
					if FUNCname in asmler.trap_list:
						opcode=asmler.trap_list.index(FUNCname)
						asmler.asm['instruction'].append(('TRAP',opcode))
					else:
						opcode=asmler.func_dict[FUNCname]
						asmler.asm['instruction'].append(('JSR',opcode))
			elif name=='return':
				##XRET
				if len(Node.sons)==2:
					run_node(asmler,Node.sons[1])##expr
					asmler.asm['instruction'].append(('STORE_NAME',asmler.reserved_name_dict['RET']))
					asmler.asm['instruction'].append(('XRET',None))
			elif name=='bool_expr':
				run_node(asmler,Node.sons[0])
				Node=Node.sons[1]
				if len(Node.sons)==1:
					return
				elif len(Node.sons)==3:
					while len(Node.sons==3):
						run_node(asmler,Node.sons[1])
						opname=asmler.opname_dict[Node.sons[0].sons[0].value]
						asmler.asm['instruction'].append((opname,None))
						Node=Node.sons[2]
			elif name=='bool_single':
				run_node(asmler,Node.sons[0])
				run_node(asmler,Node.sons[2])
				asmler.asm['instruction'].append(('SUB',None))
				asmler.asm['instruction'].append(('LOAD_CONST',asmler.reserved_const_dict['True']))
				opcode=asmler.bool_dict[Node.sons[1].sons[0].value]
				asmler.asm['instruction'].append(('BR',opcode,len(asmler.asm['instruction'])))
				asmler.asm['instruction'].append(('LOAD_CONST',asmler.reserved_const_dict['False']))
			elif name=='value_expr':
				run_node(asmler,Node.sons[0])
				Node=Node.sons[1]
				if len(Node.sons)==1:
					return
				elif len(Node.sons)==3:
					while len(Node.sons==3):
						run_node(asmler,Node.sons[1])
						opname=asmler.opname_dict[Node.sons[0].sons[0].value]
						asmler.asm['instruction'].append((opname,None))
						Node=Node.sons[2]
			elif name=='term':
				run_node(asmler,Node.sons[0])
				Node=Node.sons[1]
				if len(Node.sons)==1:
					return
				elif len(Node.sons)==3:
					while len(Node.sons==3):
						run_node(asmler,Node.sons[1])
						opname=asmler.opname_dict[Node.sons[0].sons[0].value]
						asmler.asm['instruction'].append((opname,None))
						Node=Node.sons[2]
			elif name=='factor':
				if len(Node.sons)==3:
					run_node(asmler,Node.sons[1])
				elif len(Node.sons)==1:
					val=Node.sons[0].sons[0].value
					if val in asmler.asm['name']:
						opcode=asmler.asm['name'].index(val)
						asmler.asm['instruction'].append(('LOAD_NAME',opcode))
					elif val in asmler.asm['const']:
						asmler.asm['instruction'].append(('LOAD_CONST',asmler.asm['const'].index(val)))
					else:
						opcode=len(asmler.asm['const'])
						asmler.asm['const'].append(val)
						asmler.asm['instruction'].append(('LOAD_CONST',opcode))
				else:
					raise Error('factor subnode number error')
		if type(tree.root.value)==tuple:
			args=tree.root.value[1]
			if type(args)==list:
				for key in args:
					self.asm['environment'][0][1].append(key)
		for node in tree.root.sons:
			#print(node.value)
			run_node(self,node)
		self.asm['instruction'].append(('HALT',None))


def codeOf(syntaxTree):
	assembler=Asm()
	assembler.run_tree(syntaxTree)
	return assembler.asm

