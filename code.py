
import sys
import os
sys.path.append(os.path.abspath(os.path.join('AFD/AFN/parsers')))
from Automata import Automata
from Transition import Transition

class TokenInterpreter:
	def __init__(self, tokens):
		self.tokens = tokens
		self.counter = 0
		self.curr_token = self.tokens[self.counter]
		self.other_token = ""

	def next_token( self ):
		self.counter += 1
		if self.counter < len(self.tokens):
			self.curr_token = self.tokens[self.counter]
			self.other_token = self.tokens[self.counter - 1]

	def expect(self, item, tkk = False):
		charCount = 1
		for j in range(0,self.counter):
			charCount += len(self.tokens[j].value)
			
		if tkk:
			if self.curr_token.type == item:
				self.next_token()
				return True
			else:
				print (f'#Syntax Error at char {charCount}, expected: ' + '"' + str(item) + '"' + f" but got {self.curr_token.value}")
				return False
		else:
			if self.curr_token.value == item:
				self.next_token()
				return True
			else:
				print (f'#Syntax Error at char {charCount}, expected: ' + '"' + str(item) + '"' + f" but got {self.curr_token.value}")
				return False
	def Expr(self):

    		while self.curr_token.type == 'number' or self.curr_token.type == 'decnumber' or self.curr_token.value == '-' or self.curr_token.value == '(':
    			self.Stat()
    			self.expect(";")
    			self.expect(".")
    
	def Stat(self):
		value =0
		value = self.expression(value)
		print(str(value))

	def expression(self,result):
		result1, result2 =0, 0
		result1 = self.Term(result1)
		while self.curr_token.value=="+" or self.curr_token.value=="-" :
			if self.curr_token.value == '+': 
				self.expect('+')
				result2 = self.Term(result2)
				result1+=result2
			if self.curr_token.value == '-': 
				self.expect('-')
				result2 = self.Term(result2)
				result1-=result2
				
		return result1

	def Term(self,result):
		result1, result2 =0,0
		result1 = self.Factor(result1)
		while self.curr_token.value=="*" or self.curr_token.value=="/" :
			if self.curr_token.value == '*': 
				self.expect('*')
				result2 = self.Factor(result2)
				result1*=result2
			if self.curr_token.value == '/': 
				self.expect('/')
				result2 = self.Factor(result2)
				result1/=result2
				
		result=result1
		return result

	def Factor(self,result):
		signo=1
		if self.curr_token.value == '-':
			self.expect('-')
			signo = -1
		if self.curr_token.type == 'number': 
			self.expect('number', True)
			result = self.Number(result)
		if self.curr_token.type == 'decnumber': 
			self.expect('decnumber', True)
			result = self.Number(result)
		if self.curr_token.value == '(': 
			self.expect('(')
			result = self.expression(result)
			
			self.expect(')')
		result*=signo
		return result

	def Number(self,result):
		if self.curr_token.type == 'number': 
			self.expect('number', True)
		if self.curr_token.type == 'decnumber': 
			self.expect('decnumber', True)
			
		result = float(self.other_token.value)
		return result


class Token:
	def __init__(self, type, value):
		self.type = type
		self.value = value


automata = Automata([],['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ζ', '.', '+', '-', '/', '*'], Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 63, 64, 65, 66], '0',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
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
, Transition([67], None,None, {'operators': 67})
, Transition([67], None,None, {'operators': 67})
, Transition([67], None,None, {'operators': 67})
, Transition([67], None,None, {'operators': 67})
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
], [Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 63, 64, 65, 66], '0',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 63, 64, 65, 66], '1',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 63, 64, 65, 66], '2',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 63, 64, 65, 66], '3',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 63, 64, 65, 66], '4',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 63, 64, 65, 66], '5',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 63, 64, 65, 66], '6',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 63, 64, 65, 66], '7',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 63, 64, 65, 66], '8',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 63, 64, 65, 66], '9',[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], {'number': 20})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 63, 64, 65, 66], '+',[67], {'operators': 67})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 63, 64, 65, 66], '-',[67], {'operators': 67})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 63, 64, 65, 66], '/',[67], {'operators': 67})
, Transition([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 63, 64, 65, 66], '*',[67], {'operators': 67})
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
, Transition([67], None,None, {'operators': 67})
, Transition([67], None,None, {'operators': 67})
, Transition([67], None,None, {'operators': 67})
, Transition([67], None,None, {'operators': 67})
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
tokens = {'number': {'token': '((0γ1γ2γ3γ4γ5γ6γ7γ8γ9)((0γ1γ2γ3γ4γ5γ6γ7γ8γ9))α)', 'isExcept': True}, 'decnumber': {'token': '(0γ1γ2γ3γ4γ5γ6γ7γ8γ9)δ((0γ1γ2γ3γ4γ5γ6γ7γ8γ9)α)δ.δ(0γ1γ2γ3γ4γ5γ6γ7γ8γ9)δ((0γ1γ2γ3γ4γ5γ6γ7γ8γ9)α)', 'isExcept': False}, 'operators': {'token': '(+γ-γ/γ*)', 'isExcept': False}}
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
            tkk = Token(type="UNDEFINED", value=resultado)
            stackTokens.append(tkk)
    
    for elem in stackTokens:
        if elem.value == " ":
            stackTokens.remove(elem)
    
    parser = TokenInterpreter(stackTokens)
    parser.Expr()

x = reader_tester()    