def Expr(self):
		while self.actual_token.type == 'number' or self.actual_token.type == 'decnumber' or self.actual_token.value == '-' or self.actual_token.value == '(':
			self.Stat()
			self.read(";", panic=True)
		self.read(".",panic=True)
    
	def Stat(self):
		value = 0
		value = self.expression(value)
		print(value)

	def expression(self,result1):
		result1, result2 = 0, 0
		result1 = self.Term(result1)
		while self.actual_token.value == "+" or self.actual_token.value == "-" :
			if self.actual_token.value == '+': 
				self.read('+', panic=True)
				result2 = self.Term(result2)
				result1+=result2
			if self.actual_token.value == '-': 
				self.read('-', panic=True)
				result2 = self.Term(result2)
				result1-=result2
				
		return result1

	def Term(self,result):
		result1, result2 =  0,0
		result1 = self.Factor(result1)
		while self.actual_token.value == "*" or self.actual_token.value == "/" :
			if self.actual_token.value == '*': 
				self.read('*', panic=True)
				result2 = self.Factor(result2)
				result1*=result2
			if self.actual_token.value == '/': 
				self.read('/', panic=True)
				result2 = self.Factor(result2)
				result1/=result2
				
		result=result1
		return result

	def Factor(self,result):
		signo=1
		if self.actual_token.value == '-': 
			self.read('-', panic=True)
			signo = -1
		if self.actual_token.type == 'number': 
			self.read('number', True, True)
			result = self.Number(result)
		if self.actual_token.type == 'decnumber': 
			self.read('decnumber', True, True)
			result = self.Number(result)
		if self.actual_token.value == '(': 
			self.read('(', panic=True)
			result = self.expression(result)
			self.read(')', panic=True)
		result*=signo
		return result

	def Number(self,result):
		if self.actual_token.type == 'number': 
			self.read('number',True, True)
		if self.actual_token.type == 'decnumber': 
			self.read('decnumber', True, True)
			
		result = float(self.last_token.value)
		return result