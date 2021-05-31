def Expr(self):

    while self.expect('numbers') or self.expect('-') or self.expect('('):
        self.Stat()
        self.expect(';')
    self.expect('.') 
    
def Stat(self):
	value =0
	value = self.expression(value)
	print(str(value))

def expression(self,result):
	result1, result2 =0, 0
	result1 = self.Term(result1)
	while self.expect("+") or self.expect("-") :
		if lastToken == '+': 
			result2 = self.Term(result2)
			result1+=result2
		if lastToken == '-': 
			result2 = self.Term(result2)
			result1-=result2
			
	return result1

def Term(self,result):
	result1, result2 =0,0
	result1 = self.Factor(result1)
	while self.expect("*") or self.expect("/") :
		if lastToken == '*': 
			result2 = self.Factor(result2)
			result1*=result2
		if lastToken == '/': 
			result2 = self.Factor(result2)
			result1/=result2
			
	result=result1
	return result

def Factor(self,result):
	signo=1
	if lastToken == '-': 
		signo = -1
	if lastToken == 'number': 
		result = self.Number(result)
		self.result>()
	if lastToken == '(': 
		result = self.expression(result)
		self.result>()
		
	result*=signo
	return result

def Number(self,result):
	result =int(self.last_token.value)
	return result

