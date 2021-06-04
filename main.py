from ATGReader import ATGReader
from ATGParser import ATGParser

words = open('./C.atg', "r").read().split("\n")
reader = ATGReader(words)


reader.build_atg()

#Conversion process
atgAutomatas = ATGParser(reader)

#Scanner writer

imports = """import sys
import os
sys.path.append(os.path.abspath(os.path.join('AFD/AFN/parsers')))
from Automata import Automata
from Transition import Transition
"""

#Obtenemos automata..
#automata.states, automata.language, automata.start, automata.end, automata.fn
states, language, start, end, fn = atgAutomatas.main_tree()

#construimos automata en el scanner..
buildAutomata = f"""
automata = Automata({states},{language}, {start}, {end}, {fn})
tokens = {reader.tokens}
keywords = {reader.keywords}
ignoreChars = {reader.ignore}
"""

keysearch = """\n
def keyword_search(string):
    for elem in keywords.keys():
        if string == elem:
            return elem
    return None\n"""

reading = """f = open('test.txt', 'r')

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
    parser.Expr()

x = reader_tester()    """


scanner = open("code.py", "w")

imports = """
import sys
import os
sys.path.append(os.path.abspath(os.path.join('AFD/AFN/parsers')))
from Automata import Automata
from Transition import Transition
"""

clase="""
class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.id_token = 0
		self.curr_token = self.tokens[self.id_token]
		self.other_token = ""

	def next_token( self ):
		self.id_token += 1
		if self.id_token < len(self.tokens):
			self.curr_token = self.tokens[self.id_token]
			self.other_token = self.tokens[self.id_token - 1]

	def expect(self, item, tkk = False):
		charCount = 1
		for j in range(0,self.id_token):
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
"""
methods = atgAutomatas.methods_string()
scanner.write(imports)
scanner.write(clase)
scanner.write(methods)
tokenClass = """
class Token:
	def __init__(self, type, value):
		self.type = type
		self.value = value

	def __repr__(self):
		return f'<Token {self.type} value: {self.value} >'
"""
scanner.write(tokenClass)
scanner.write(buildAutomata)
scanner.write(keysearch)
scanner.write(reading)
scanner.close()
print("End parsing ATG")

