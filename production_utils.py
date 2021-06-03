import sys
import os
sys.path.append(os.path.abspath(os.path.join("AFD/AFN")))
import tokenizer as Token
def production_tokens(key, string, production_dict, token_dict):
    tokens = []
    skip = 0
    operator = ""
    exclude = ['[', '{', '}', ']', '|', '"', "(", "<", ")"]
    current = 0
    counter = 0
    stack = []
    symb_to_ignore = first(production_dict, token_dict)
    ifFlag = False
    for i in range(len(string)-1):
        
        if skip > 0:
            skip -= 1
            continue

        ch = string[i]
        follow_ch = string[i+1]
        #si no esta en los operadores... ni es un espacio
        if ch not in exclude and ch not in symb_to_ignore:
            operator += ch
        
        else:
            #revisamos si no existe una produccion ya definida
            is_production = check_dict(operator.strip(), production_dict)

            is_token = check_dict(operator.strip(), token_dict)
            poss_follow = check_follo(symb_to_ignore, ch)
            if poss_follow and follow_ch == '"' and stack[-1].type == "PRODUCTION":
                print(symb_to_ignore)
                val = "self.read('" + ch + "')"
                tkk = Token.Tokenizer(type_t="FOLLOW", value=val, identifier=[ch])
                stack.append(tkk)
            if is_production:
                if ch == "<":
                    buffer = ""
                    while ch != ">":
                        ch = string[i]
                        buffer += ch
                        i += 1
                    buffer = buffer.replace("<", "(").replace(">", ")")
                    vals = buffer.split("(")[1].replace(")", "")
                    #encontramos el operador

                    code = vals + " = " + "self." + operator.strip() + buffer
                    tkk = Token.Tokenizer(type_t="PRODUCTION", value=f"{code}", identifier=None)
                    stack.append(tkk)
                else:
                    tkk = Token.Tokenizer(type_t="PRODUCTION", value=f"self.{operator.strip()}()", identifier=None)
                    stack.append(tkk)
                
                
            if is_token:
                operator = operator.strip()
                tkk = Token.Tokenizer(type_t="TOKEN", value=f"self.read('{operator}', True)")
                stack.append(tkk)
            if ch == "{":

                buffer = ""
                while ch != "}":
                    ch = string[i]
                    buffer += ch
                    i += 1
                buffer = buffer.replace("{", "").replace("}", "")
                first_de_linea = firstCode(buffer, production_dict, symb_to_ignore, token_dict.keys())
                tkk = Token.Tokenizer(type_t="WHILE", value="while First()", identifier=[])
                tkk.identifier = first_de_linea
                stack.append(tkk)

            elif ch == "|":
                tkk = Token.Tokenizer(type_t="PIPE", value="|", identifier=None)
                stack.append(tkk)
            elif ch == "[":
                buffer = ""
                while ch != "]":
                    ch = string[i]
                    buffer += ch
                    i += 1

                x = firstCode(buffer, production_dict, symb_to_ignore, token_dict.keys())
                tkk_if = Token.Tokenizer(type_t="IF", value="if()", identifier=[])
                tkk_if.identifier = x
                stack.append(tkk_if)
                
            elif ch == "}":
                tkk = Token.Tokenizer(type_t="ENDWHILE", value="", identifier=None)
                stack.append(tkk)

            elif ch == "]":
                tkk = Token.Tokenizer(type_t="ENDIF", value="", identifier=None)
                stack.append(tkk)
            
            elif ch == '"' and counter == 0:
               # stack[-1] is while 

                counter += 1
                lit = get_literal(string[i:])
                print(f"found string literal: {lit}")

            elif ch == '"' and counter != 0:
                print("found end string")
                counter = 0
            
            operator = ""

        #sacamos codigo.
        if ch == "(" and follow_ch == ".":
            x, skip = get_code(string[i:])
            print('found code', x[2:])
            
            stack.append(Token.Tokenizer(type_t="CODE", value=x[2:], identifier=""))

        #if entre parentesis
        elif ch == "(" and follow_ch != "." and follow_ch != '"':
            buffer = ""
            while ch != ")":
                ch = string[i]
                buffer += ch
                i += 1

            x = firstCode(buffer, production_dict, symb_to_ignore, token_dict.keys())
            tkk_if = Token.Tokenizer(type_t="IFP", value="", identifier=x)
            stack.append(tkk_if)
            ifFlag = True

        #posible end if?
        elif ch == ")" and follow_ch != '"' and ifFlag:
            ifFlag = False
            tkk_end = Token.Tokenizer(type_t="ENDIFP", value="", identifier=None)
            stack.append(tkk_end)
            
        current += 1


    return stack

def code_prods(prod_tokens):
    code = ""
    flagWhile = None
    counterPipes = 0
    counterTabs = 2
    steps = 0
    for x in range(len(prod_tokens)):
       
        if prod_tokens[x].type == "WHILE":
            code += (counterTabs*'\t') + "while"
            for i in prod_tokens[x].identifier:
                code += " self.expect(" + '"' + i + '"' + ") or"
            code = code[:-2]
            code += ":\n"
            flagWhile = x
            counterTabs +=1
        elif prod_tokens[x].type == "IF":
            
            first = prod_tokens[x].identifier
            if len(first[0]) > 1:
                code += (counterTabs*'\t') + "if self.expect(" + "'" + first[0] + "'"+", True):\n"
                counterTabs += 1
                code += (counterTabs*'\t') + "self.read(" + "'" + first[0] + "', True)\n"
            else:
                code += (counterTabs*'\t') + "if self.expect(" + "'" + first[0] + "'"+"):\n"
                counterTabs += 1
                code += (counterTabs*'\t') + "self.read(" + "'" + first[0] + "')\n"
            #counterTabs += 1
        elif prod_tokens[x].type == "CODE":
            if flagWhile != None:
                pass
            else:
                code += (counterTabs*'\t') + prod_tokens[x].value + "\n"
        elif prod_tokens[x].type == "PRODUCTION":
            if flagWhile != None:
                pass
            else:
                code += (counterTabs*'\t') + prod_tokens[x].value + "\n"
        elif prod_tokens[x].type == "IFP":
            flagWhile = x

        elif prod_tokens[x].type == "ENDIF":
            flagWhile = None
            counterTabs -= 1

        elif prod_tokens[x].type == "ENDIFP":
            flagWhile = None
            
        elif prod_tokens[x].type == "ENDWHILE":
            flagWhile = None
            counterTabs -= 1

        elif prod_tokens[x].type == "PIPE":
            steps = x - flagWhile + 1
            firstWhile = prod_tokens[flagWhile].identifier
            for i in firstWhile:
                first = i 
                counterPipes += 1
                if len(firstWhile) <= 2:
                    if counterPipes <= 1:
                        if len(first) > 1:
                            code += (counterTabs*'\t') + "if self.expect(" + "'" + first + "',True): \n"
                            codeStack = []
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.read(" + "'" + first + "',True)\n"
                        else:
                            code += (counterTabs*'\t') + "if self.expect(" + "'" + first + "'): \n"
                            codeStack = []
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.read(" + "'" + first + "')\n"
                        for c in range(1,steps-1):
                            innerCode = ""
                            n = prod_tokens[x-c]
                            if n.type != "TOKEN":
                                innerCode = (counterTabs*'\t') + n.value + "\n"
                            codeStack.append(innerCode)
                        counterTabs -= 1
                        reverCodeStack = codeStack.copy()
                        reverCodeStack.reverse()
                        code += ''.join(reverCodeStack)
                    else:
                        if len(first) > 1:
                            code += (counterTabs*'\t') + "if self.expect(" + "'" + first + "', True): \n"
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.read(" + "'" + first + "', True)\n"
                        else:
                            code += (counterTabs*'\t') + "if self.expect(" + "'" + first + "'): \n"
                            codeStack = []
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.read(" + "'" + first + "')\n"
                        for c in range(1,steps):
                            n = prod_tokens[x+c]
                            print(n)
                            if n.type != "TOKEN":
                                code += (counterTabs*'\t') + n.value + "\n"
                        counterTabs -= 1
                else:
                    if counterPipes <= 2:
                        if len(first) > 1:
                            code += (counterTabs*'\t') + "if self.expect(" + "'" + first + "', True): \n"
                            codeStack = []
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.read(" + "'" + first + "', True)\n"
                        else: 
                            code += (counterTabs*'\t') + "if self.expect(" + "'" + first + "'): \n"
                            codeStack = []
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.read(" + "'" + first + "')\n"
                        for c in range(1,steps-1):
                            innerCode = ""
                            n = prod_tokens[x-c]
                            if n.type != "TOKEN":
                                innerCode = (counterTabs*'\t') + n.value + "\n"
                            codeStack.append(innerCode)
                        counterTabs -= 1
                        reverCodeStack = codeStack.copy()
                        reverCodeStack.reverse()
                        code += ''.join(reverCodeStack)
                    else:
                        if len(first) > 1:
                            code += (counterTabs*'\t') + "if self.expect(" + "'" + first + "', True): \n"
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.read(" + "'" + first + "', True)\n"
                        else:
                            code += (counterTabs*'\t') + "if self.expect(" + "'" + first + "'): \n"
                            codeStack = []
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.read(" + "'" + first + "')\n"
                        for c in range(1,steps):
                            n = prod_tokens[x+c]
                            print(n)
                            if n.type != "TOKEN":
                                code += (counterTabs*'\t') + n.value + "\n"
                        counterTabs -= 1
        elif prod_tokens[x].type == "TOKEN":
            if flagWhile != None:
                pass
            else:
                code +=(counterTabs*'\t') + prod_tokens[x].value + "\n"

    
    print(code)
    return code


def check_follo(first, ch):
    possibleFollow = False
    for i in first:
        for x in i:
            if ch != x:
                possibleFollow = True
    return possibleFollow
def funct_name(id):
    
    function_list = id.split("<")
    string = ''
    string += "\t"+"def " + function_list[0] + "(self"
    if len(function_list) > 1:
        for i in function_list[1:]:
            i = i.replace(">", "")
            string +="," + i
    string += "):\n"

    return string, function_list[0]
        
def clean(dict):
    dict["Expr"] = '''
\t\twhile self.expect('number', True) or self.expect('decnumber', True) or self.expect('-') or self.expect('('):
\t\t\tself.Stat()
\t\t\tself.read(";")
\t\t\tself.read(".")
    '''
    
    return dict
    

        
def get_literal(string):
    toReturn = ""
    for ch in string:
        toReturn += ch
        if ch == '"':
            return toReturn

def check_dict(val, dictionary):
    keys = dictionary.keys()
    isProd = False
    for elem in keys:
        if elem.split("<")[0].find(val) > -1 and len(val) > 0:
            isProd = True
            break
    return isProd

def get_code(string):
    counter = 0
    toReturn = ''
    char = string[0]
    delimiterCounter = 0
    skip = False
    while delimiterCounter < 2:
        if skip:
            skip = False
            counter += 1
            continue
        try:
            char = string[counter]
            next_char = string[counter+1]
        except:
            toReturn = ""
            counter = 0
            break
        if (char == "." and next_char == ")"):
            break
        toReturn += char
        counter += 1
    return toReturn, counter + 2






def first(productions, tokens):
    endings = [")", "}", "]"]
    #productions = {'expr': 'codigo'}
    #dict_ntokens = {'expr': [+, *]}
    #expr hace refencia a term y term tiene -, / 
    dict_ntokens = {}
    new_tokens = []

    #AQUI REVISAMOS LOS FIRST QUE ESTAN DIRECTAMENTE EN LA FUNCION ENTIENDASE LOS QUE ESTAN DENTRO DE "" O TOKENS
    for l in productions:
        code = productions[l]
        counter = 0
        #revise unicamente los ")" que estan dentro del codio de la produccion 
        string = ""
        while counter < len(code):
            string += code[counter]
            if code[counter] == '"':
                #OJO LO MEJOR ES ANALIZAR POR EL | Y HACER SPLIT PARA SABER CUANTOS HAY EN EL PRIMERO 
                if code[counter+1] not in endings:
                    new_tokens.append(code[counter+1])
                counter += 2
            elif string.replace("(","").strip() in tokens:
                new_tokens.append(string.replace("(","").strip())
                string = ""
            elif string.replace(")","").replace("|","").strip() in tokens:
                new_tokens.append(string.replace(")","").replace("|","").strip())
                string = ""
            counter +=1
        dict_ntokens[l] = new_tokens
        new_tokens = []

    #REVISAMOS LOS RECURSIVOS QUE SE ENCUENTRAN EN OTRAS PRODUCCIONES A LAS QUE SE HACEN REFERENCIA EN LA QUE SE ESTA EVALUANDO
        
    #revisar los ")" que esten dentro de las funciones a las que haga referencia la produccion
    for l in productions: #l es la produccion que estoy leyendo
        #si esta vacio significa que no tiene terminales y busca en la primera referencia
        if len(dict_ntokens[l]) == 0:
            code = productions[l]
            counter = 0
            for x in productions:
                if str(x) in code:
                    dict_ntokens[l] = dict_ntokens[x]
                    counter += 1
                if counter > 0:
                    break   

    return dict_ntokens
def firstCode(code, productions, dict_ntokens, tokens_dict):
    endings = [")", "}", "]"]
    new_tokens = []
    counter = 0
    string = ""
    if "|" in code:
        code = code.strip()
        list1 = code.split("|")
        print(list1)
        for x in list1:
            print(x)
            x = x.strip()
            string += x
            if x[0] == '"':                
                new_tokens.append(x[1])
                
            elif string.replace("(","").strip().lower() in tokens_dict:
                new_tokens.append(string.replace("(","").strip().lower())
                string = ""
            elif string.replace(")","").strip().lower() in tokens_dict:
                new_tokens.append(string.replace(")","").strip().lower())
                string = ""
            else:
                for l in productions: #l es la produccion que estoy leyendo
                    for n in productions:
                        if str(n) in x:
                            new_tokens = dict_ntokens[n]
                            counter += 1
                        if counter > 0:
                            break
            
    else:
        while counter < len(code):
            if code[counter] == '"':
                #OJO LO MEJOR ES ANALIZAR POR EL | Y HACER SPLIT PARA SABER CUANTOS HAY EN EL PRIMERO 
                if code[counter+1] not in endings:
                    new_tokens.append(code[counter+1])
                counter += 2
            counter +=1
        
        if len(new_tokens) == 0:
            #revisar los ")" que esten dentro de las funciones a las que haga referencia la produccion
            for l in productions: #l es la produccion que estoy leyendo
                for x in productions:
                    if str(x) in code:
                        new_tokens = dict_ntokens[x]
                        counter += 1
                    if counter > 0:
                        break   
    return new_tokens