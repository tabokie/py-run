'''
Python Virtual Machine
description: run instructions on a stack-based machine
'''

import time

class Interpreter:
	def __init__(self):
		#value stack
		self.stack=[]
		self.pstack=-1
		#run-time stack
		self.frame_stack=[]
		self.pfstack=-1
		self.pframe=-1
		#registers
		self.PC=0
		self.TEMP=None

	##instruction function
	def JUMP(self,value):
		self.PC=value-1
		return
	def BR(self,code,value):
		if code==0 and self.stack[-1]==0:
			self.JUMP(value)
		elif code*self.stack[-1]>0:
			self.JUMP(value)
		return
	def JSR(self,funcInfo):
		addr=funcInfo[0]
		paraNameList=funcInfo[1]
		self.TEMP=self.PC
		self.PC=addr-1
		for i in range(len(paraNameList)):
			parameter=(paraNameList[i],self.stack.pop())
			self.pfstack+=1
			self.frame_stack.append(parameter)
		self.frame_stack.append(len(paraNameList))#
		self.frame_stack.append(None)#return value
		self.frame_stack.append(self.TEMP)#return address
		self.frame_stack.append(self.pframe)#frame pointer
		self.pfstack+=4
		self.pframe=self.pfstack+1
		return
	def RET(self):
		self.PC=self.frame_stack[self.pframe-2]
		paraNum=self.frame_stack[self.pframe-4]
		self.pfstack=self.pframe-4-paraNum-1
		self.pframe=self.frame_stack[self.pframe-1]
		i=self.pfstack+1
		while i<len(self.frame_stack):
			self.frame_stack.pop(i)
			i+=1
		return
	def XRET(self):#return with value
		self.PC=self.frame_stack[self.pframe-2]
		ret=self.frame_stack[self.pframe-3]
		self.stack.append(ret)
		paraNum=self.frame_stack[self.pframe-4]
		self.pfstack=self.pframe-4-paraNum-1
		self.pframe=self.frame_stack[self.pframe-1]
		#waste
		i=self.pfstack+1
		j=len(self.frame_stack)
		while i<j:
			self.frame_stack.pop()
			i+=1
		return
	def HALT(self):
		self.PC=-1
		return
	def LOAD_CONST(self,value):
		self.stack.append(value)
		return
	def STORE_NAME(self,name):
		'''
		for x in range(self.pfstack+1):
			print(self.frame_stack[x])
		print('store:',name)
		'''
		val=self.stack.pop()
		if name=="__RET__":
			self.frame_stack[self.pframe-3]=val
			return
		self.pfstack+=1
		self.frame_stack.append((name,val))
		'''
		print('====')
		#for x in range(self.pfstack+1):
		print(self.frame_stack)
		'''
		return
	def LOAD_NAME(self,name):
		def search(stack,p1,p2,target):
			for i in range(p2-p1+1):
				if stack[p1+i][0]==target:
					return stack[p1+i][1]
			return None
		'''
		for x in range(self.pfstack+1):
			print(self.frame_stack[x])
		'''
		p1=self.pframe
		p2=self.pfstack
		while True:
			paraNum=self.frame_stack[p1-4]
			#search local var
			res=search(self.frame_stack,p1,p2,name)
			if res!=None:
				self.stack.append(res)
				return
			#search parameter
			p2=p1-5
			p1=p1-4-paraNum
			res=search(self.frame_stack,p1,p2,name)
			if res!=None:
				self.stack.append(res)
				return
			#switch environment
			temp=p1-1
			p1=self.frame_stack[p2+4]
			p2=temp
			if p1<0:
				break
		raise ErrorNotFoundVar("%s can't found"%name)
		return
	def ADD(self):
		val1=self.stack.pop()
		val2=self.stack.pop()
		self.stack.append(val1+val2)
		return
	def AND(self):
		val1=self.stack.pop()
		val2=self.stack.pop()
		self.stack.append(val1 and val2)
		return
	def OR(self):
		val1=self.stack.pop()
		val2=self.stack.pop()
		self.stack.append(val1 or val2)
		return
	def SUB(self):
		val1=self.stack.pop()
		val2=self.stack.pop()
		self.stack.append(val1-val2)
		return
	def MUL(self):
		val1=self.stack.pop()
		val2=self.stack.pop()
		self.stack.append(val1*val2)
		return
	def DIV(self):
		val1=self.stack.pop()
		val2=self.stack.pop()
		self.stack.append(val1/val2)
		return
	def TRAP(self,code):
		func_name=["PRINT","INPUT"]
		val=self.stack[-1]
		opname=func_name[code]
		method=getattr(self,opname)
		self.stack.append(method(val))
		return
	def PRINT(self,data):
		print('>>>',data)
		return True
	def INPUT(self,prompt):
		IN=input('>>>',prompt)
		return IN

	##main runner
	def run_code(self,what_to_execute,args=[]):
		instructions=what_to_execute["instruction"]
		if what_to_execute['environment'][0][1]!=[] and args==[]:
			raise Error('no prompt args')
		elif what_to_execute['environment'][0][1]==[] and args!=[]:
			raise Error('no prompt args needed')
		elif what_to_execute['environment'][0][1]!=[] and args!=[]:
			for val in args:
				self.stack.insert(0,val)

		while True:
			#print(instructions[self.PC])
			if len(instructions[self.PC])==2:
				opname,arg=instructions[self.PC]
				
				if opname in ["LOAD_CONST"]:
					arg = what_to_execute["const"][arg]
				elif opname in ["STORE_NAME","LOAD_NAME"]:
					arg = what_to_execute["name"][arg]
				elif opname in ['JSR']:
					arg = what_to_execute["environment"][arg]
				method = getattr(self,opname)
				if arg==None:
					method()
				else:
					method(arg)
			elif len(instructions[self.PC])==3:
				opname,arg1,arg2=instructions[self.PC]
				method=getattr(self,opname)
				method(arg1,arg2)
			else:
				raise ErrorArgument('Too many args in one instruction.')
			
			if self.PC < 0:
				break
			self.PC+=1


def runCode(code):
	print('>>>running in virtual machine')
	interpreter=Interpreter()
	interpreter.run_code(code)
	return