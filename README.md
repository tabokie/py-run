# py-run

Lightweight Interpreter for python3 written in python3, run instructions on stack-based virtual machine in python.

Currently supports `Weakly Typed variable`, `Function Call by Value`, `Basic Control`, `Basic Syscall`, `Block by Indent`.

## Module

* **Scanner**: using ply.lex, parsing strings to 21 basic tokens.

* **Parser**: context-free grammar stored in matrix. Analyse tokens into SyntaxTree(n-ary tree).

* **Assembly**: A assembly machine with complete global variable and local variable area, syscall trap list, local name table. Convert syntex tree to instruction sets.

* **Virtual Machine**: Implement instruction based on python3 environment, execute instruction with stack and frame stack.

## Test

* Case 1: 

```python
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
```

```shell
$ 9
```

