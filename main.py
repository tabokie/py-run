'''
#2017-9-25-rough version
Description: Only support basic instruction and rough rough run-time stack
Remaining Bug:
	function as name but not object
	command-line variable debug
	NOT bool operative
	>=,<= operative
	function call clause as expr
	else clause
	give function pointer-->not necessary
'''

from Scanner import tokenOf
from Parser import syntaxOf
from AssemblyGenerator import codeOf
from VirtualMachine import runCode

#expected print result:
#>>>9
testData="""
		def func(a):
			a=9
			return a
a=0
func(a)
if a==1:
	b="a string"
else:
	b=9
print(b)
"""

runCode(codeOf(syntaxOf(tokenOf(testData))))





