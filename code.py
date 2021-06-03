
import sys
import os
sys.path.append(os.path.abspath(os.path.join('AFD/AFN/parsers')))
from Automata import Automata
from Transition import Transition

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.id_token = 0
		self.actual_token = self.tokens[self.id_token]
		self.last_token = ''
		self.ok = True

		self.check()

	
	def check(self):
		
		charCounter = 0
		for i in range(len(self.tokens)-1):
			token = self.tokens[i] 
			nextToken = self.tokens[i+1]
			charCounter += len(token.value)
			#caso 1
			if token.type == "operators" and nextToken.type == "ANY":
				print(f'Error sintactico, caracter {charCounter}')
				
				
			elif (token.type == "ANY") and (nextToken.value == ";"):
				print(f'Error sintactico, caracter {charCounter}')
				self.ok = False
				break
				




	def advance( self ):
		self.id_token += 1
		if self.id_token < len(self.tokens):
			self.actual_token = self.tokens[self.id_token]
			self.last_token = self.tokens[self.id_token - 1]

	def expect(self, item, arg = False):
		og = self.id_token
		possible = False
		try:
			ans = self.read(item, arg)
			if type(ans) == bool:
				possible = ans
			else:
				possible = True
		except:
			possible = False
		self.id_token = og
		self.actual_token = self.tokens[self.id_token]
		self.last_token = self.tokens[self.id_token - 1]
		return possible

	def read(self, item, type = False):
		if type:
			if self.actual_token.type == item:
				self.advance()
				return True
			else:
				return False
				#print('expected ', item, ' got ', self.actual_token.type)
		else:
			if self.actual_token.value == item:
				self.advance()
				return True
			else:
				return False
	def Expr(self):

		while self.expect('number', True) or self.expect('decnumber', True) or self.expect('-') or self.expect('('):
			self.Stat()
			self.read(";")
			self.read(".")
    
	def Stat(self):
		value =0
		value = self.expression(value)
		print(str(value))

	def expression(self,result):
		result1, result2 =0, 0
		result1 = self.Term(result1)
		while self.expect("+") or self.expect("-") :
			if self.expect('+'): 
				self.read('+')
				result2 = self.Term(result2)
				result1+=result2
			if self.expect('-'): 
				self.read('-')
				result2 = self.Term(result2)
				result1-=result2
				
		return result1

	def Term(self,result):
		result1, result2 =0,0
		result1 = self.Factor(result1)
		while self.expect("*") or self.expect("/") :
			if self.expect('*'): 
				self.read('*')
				result2 = self.Factor(result2)
				result1*=result2
			if self.expect('/'): 
				self.read('/')
				result2 = self.Factor(result2)
				result1/=result2
				
		result=result1
		return result

	def Factor(self,result):
		signo=1
		if self.expect('-'):
			self.read('-')
			signo = -1
		if self.expect('number', True): 
			self.read('number', True)
			result = self.Number(result)
		if self.expect('decnumber', True): 
			self.read('decnumber', True)
			result = self.Number(result)
		if self.expect('('): 
			self.read('(')
			result = self.expression(result)
			self.read(')')
		result*=signo
		return result

	def Number(self,result):
		if self.expect('number',True): 
			self.read('number',True)
		if self.expect('decnumber', True): 
			self.read('decnumber', True)
			
		result = float(self.last_token.value)
		return result


class Token:
	def __init__(self, type, value):
		self.type = type
		self.value = value

	def __repr__(self):
		return f'<Token {self.type} value: {self.value} >'

automata = Automata([],['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ζ', '.'], Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], '0',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, [Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
], [Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], '0',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], '1',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], '2',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], '3',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], '4',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], '5',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], '6',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], '7',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], '8',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], '9',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], '0',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], '1',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], '2',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], '3',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], '4',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], '5',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], '6',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], '7',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], '8',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], '9',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], '.',[42, 43, 44, 45, 46, 47, 48, 49, 50, 51], None)
, Transition([42, 43, 44, 45, 46, 47, 48, 49, 50, 51], '0',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([42, 43, 44, 45, 46, 47, 48, 49, 50, 51], '1',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([42, 43, 44, 45, 46, 47, 48, 49, 50, 51], '2',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([42, 43, 44, 45, 46, 47, 48, 49, 50, 51], '3',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([42, 43, 44, 45, 46, 47, 48, 49, 50, 51], '4',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([42, 43, 44, 45, 46, 47, 48, 49, 50, 51], '5',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([42, 43, 44, 45, 46, 47, 48, 49, 50, 51], '6',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([42, 43, 44, 45, 46, 47, 48, 49, 50, 51], '7',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([42, 43, 44, 45, 46, 47, 48, 49, 50, 51], '8',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([42, 43, 44, 45, 46, 47, 48, 49, 50, 51], '9',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], '0',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], '1',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], '2',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], '3',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], '4',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], '5',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], '6',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], '7',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], '8',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], '9',[52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], {'decnumber': 62})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], None,None, {'number': 20})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
, Transition([52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], None,None, {'decnumber': 62})
])
tokens = {'number': {'token': '((0γ1γ2γ3γ4γ5γ6γ7γ8γ9)((0γ1γ2γ3γ4γ5γ6γ7γ8γ9))α)', 'isExcept': True}, 'decnumber': {'token': '(0γ1γ2γ3γ4γ5γ6γ7γ8γ9)δ((0γ1γ2γ3γ4γ5γ6γ7γ8γ9)α)δ.δ(0γ1γ2γ3γ4γ5γ6γ7γ8γ9)δ((0γ1γ2γ3γ4γ5γ6γ7γ8γ9)α)', 'isExcept': False}}
keywords = {'while': 'wδhδiδlδe', 'do': 'dδo', 'if': 'iδf'}
ignoreChars = []


def keyword_search(string):
    for elem in keywords.keys():
        if string == elem:
            return elem
    return None
f = open('test.txt', 'r')

def reader_tester():
    x = f.read()
    pos = 0
    stackTokens = []
    while pos < len(x):
        resultado, pos, aceptacion = automata.simulate_DFA(x, pos, ignoreChars)
        if aceptacion:
            allowed = True

            if allowed:
                identifier = list(aceptacion.type.keys())[0]
                #obtenemos el token
                tkk = tokens[identifier]
                #buscamos en los keywords
                if tkk["isExcept"]:
                    key=keyword_search(resultado)
                    if key:
                        print(" ->  ",repr(resultado), "identified keyword", key, " <-")
                        tkk = Token(type=key, value=resultado)
                        stackTokens.append(tkk)
                    else:
                        print(" ->  ",repr(resultado), "identified", identifier, " <-")
                        tkk = Token(type=identifier, value=resultado)
                        stackTokens.append(tkk)
                else:
                    print(" ->  ",repr(resultado), "identified", identifier, " <-")
                    tkk = Token(type=identifier, value=resultado)
                    stackTokens.append(tkk)
        else:
            print(" ->  ",repr(resultado), "unidentified string of chars <-")
            tkk = Token(type="ANY", value=resultado)
            stackTokens.append(tkk)
    
    for elem in stackTokens:
        if elem.value == " ":
            stackTokens.remove(elem)
    
    parser = Parser(stackTokens)
    if parser.ok:
        parser.Expr()
    

x = reader_tester()    