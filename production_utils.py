import sys
import os
sys.path.append(os.path.abspath(os.path.join("AFD/AFN")))
import tokenizer as Token


"""
Produce tokens en base a las producciones recibidas por atg
IN: 
    key: llave de lo que se esta leyendo
    string: value de dicha llave (todo el codigo)
    production_dict: contiene el diccionario que viene de ATGREADER.PY {Expr: "..."}
    token_dict: contiene los tokens leidos por ATGREADER.PY {operations="+|-|/|*"}

OUT:
    <Array> Token object 
"""
def production_tokens(key, string, production_dict, token_dict):
    tokens = []
    skip = 0
    operator = ""

    #special chars
    special = ['[', '{', '}', ']', '|', '"', "(", "<", ")"]
    current = 0
    counter = 0
    stack = []
    #contiene los first de cada produccion.
    first_per_prod = first(production_dict, token_dict)
    ifFlag = False
    for i in range(len(string)-1):
        
        if skip > 0:
            skip -= 1
            continue

        ch = string[i]
        next_ch = string[i+1]
        #si no esta en los operadores... ni es un espacio
        if ch not in special and ch not in first_per_prod:
            operator += ch
        
        else:
            #revisamos si no existe una produccion ya definida
            is_production = check_dict(operator.strip(), production_dict)
            #revisa si lo que esta siendo leido no es un token por el ATG
            is_token = check_dict(operator.strip(), token_dict)
            #revisa caracteres despues de llamada de produccion
            after_ch = after_chars(first_per_prod, ch)
            if after_ch and next_ch == '"' and stack[-1].type == "PRODUCTION":
                
                
                tkk = Token.Tokenizer(type_t="FOLLOW", value="", identifier=[ch])
                stack.append(tkk)

            #si encontramos produccion, entonces generamos token de tipo produccion
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
                
            #si encontramos token, entonces generamos token de tipo token
            if is_token:
                operator = operator.strip()
                tkk = Token.Tokenizer(type_t="TOKEN", value=f"self.read('{operator}', True)")
                stack.append(tkk)

            #encontramos un while.
            if ch == "{":

                buffer = ""
                while ch != "}":
                    ch = string[i]
                    buffer += ch
                    i += 1
                buffer = buffer.replace("{", "").replace("}", "")
                first_de_linea = charLinea(buffer, production_dict, first_per_prod, token_dict.keys())
                tkk = Token.Tokenizer(type_t="WHILE", value="while First()", identifier=[])
                tkk.identifier = first_de_linea
                stack.append(tkk)

            #Encontramos un or
            elif ch == "|":
                tkk = Token.Tokenizer(type_t="OR", value="|", identifier=None)
                stack.append(tkk)

            #Encontramos un opcional.. 
            elif ch == "[":
                buffer = ""
                while ch != "]":
                    ch = string[i]
                    buffer += ch
                    i += 1

                x = charLinea(buffer, production_dict, first_per_prod, token_dict.keys())
                tkk_if = Token.Tokenizer(type_t="IF", value="if()", identifier=[])
                tkk_if.identifier = x
                stack.append(tkk_if)
                
            elif ch == "}":
                tkk = Token.Tokenizer(type_t="ENDWHILE", value="", identifier=None)
                stack.append(tkk)

            elif ch == "]":
                tkk = Token.Tokenizer(type_t="ENDIF", value="", identifier=None)
                stack.append(tkk)
            
            
            operator = ""

        #Encontramos codigo
        if ch == "(" and next_ch == ".":
            x, skip = get_code(string[i:])
            
            stack.append(Token.Tokenizer(type_t="CODE", value=x[2:], identifier=""))

        #if de parens
        elif ch == "(" and next_ch != "." and next_ch != '"':
            buffer = ""
            while ch != ")":
                ch = string[i]
                buffer += ch
                i += 1

            x = charLinea(buffer, production_dict, first_per_prod, token_dict.keys())
            tkk_if = Token.Tokenizer(type_t="PARENS_IF", value="", identifier=x)
            stack.append(tkk_if)
            ifFlag = True

        #END IF PARENS
        elif ch == ")" and next_ch != '"' and ifFlag:
            ifFlag = False
            tkk_end = Token.Tokenizer(type_t="END_PARENS_IF", value="", identifier=None)
            stack.append(tkk_end)
            
        current += 1


    return stack


"""
IN: Tokens producidos
OUT: string de codigo.
"""
def code_prods(prod_tokens):
    code = ""
    flag = None
    conditionalCount = 0
    #tabs iniciales puesto que inicia dentro de una clase, y un metodo.
    counterTabs = 2
    steps = 0
    for x in range(len(prod_tokens)):
       
        if prod_tokens[x].type == "WHILE":
            code += (counterTabs*'\t') + "while"
            for i in prod_tokens[x].identifier:
                code += " self.curr_token.value==" + '"' + i + '"' + " or"
            code = code[:-2]
            code += ":\n"
            flag = x
            counterTabs +=1
        elif prod_tokens[x].type == "IF":
            
            first = prod_tokens[x].identifier
            if len(first[0]) > 1:
                code += (counterTabs*'\t') + "if self.curr_token.type == " + "'" + first[0] + "'"+":\n"
                counterTabs += 1
                code += (counterTabs*'\t') + "self.expect(" + "'" + first[0] + "')\n"
            else:
                code += (counterTabs*'\t') + "if self.curr_token.value == " + "'" + first[0] + "'"+":\n"
                counterTabs += 1
                code += (counterTabs*'\t') + "self.expect(" + "'" + first[0] + "')\n"
            #counterTabs += 1
        elif prod_tokens[x].type == "CODE":
            if flag != None:
                pass
            else:
                code += (counterTabs*'\t') + prod_tokens[x].value + "\n"
        elif prod_tokens[x].type == "PRODUCTION":
            if flag != None:
                pass
            else:
                code += (counterTabs*'\t') + prod_tokens[x].value + "\n"
        elif prod_tokens[x].type == "PARENS_IF":
            flag = x

        elif prod_tokens[x].type == "ENDIF":
            flag = None
            counterTabs -= 1

        elif prod_tokens[x].type == "END_PARENS_IF":
            flag = None
            
        elif prod_tokens[x].type == "ENDWHILE":
            flag = None
            counterTabs -= 1

        elif prod_tokens[x].type == "OR":
            steps = x - flag + 1
            firstWhile = prod_tokens[flag].identifier
            for i in firstWhile:
                first = i 
                conditionalCount += 1
                if len(firstWhile) <= 2:
                    if conditionalCount <= 1:
                        if len(first) > 1:
                            code += (counterTabs*'\t') + "if self.curr_token.type == " + "'" + first + "': \n"
                            codeStack = []
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.expect(" + "'" + first + "', True)\n"
                        else:
                            code += (counterTabs*'\t') + "if self.curr_token.value == " + "'" + first + "': \n"
                            codeStack = []
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.expect(" + "'" + first + "')\n"
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
                            code += (counterTabs*'\t') + "if self.curr_token.type == " + "'" + first + "': \n"
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.expect(" + "'" + first + "', True)\n"
                        else:
                            code += (counterTabs*'\t') + "if self.curr_token.value == " + "'" + first + "': \n"
                            codeStack = []
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.expect(" + "'" + first + "')\n"
                        for c in range(1,steps):
                            n = prod_tokens[x+c]
                            print(n)
                            if n.type != "TOKEN":
                                code += (counterTabs*'\t') + n.value + "\n"
                        counterTabs -= 1
                else:
                    if conditionalCount <= 2:
                        if len(first) > 1:
                            code += (counterTabs*'\t') + "if self.curr_token.type == " + "'" + first + "': \n"
                            codeStack = []
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.expect(" + "'" + first + "', True)\n"
                        else: 
                            code += (counterTabs*'\t') + "if self.curr_token.value == " + "'" + first + "': \n"
                            codeStack = []
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.expect(" + "'" + first + "')\n"
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
                            code += (counterTabs*'\t') + "if self.curr_token.type == " + "'" + first + "': \n"
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.expect(" + "'" + first + "', True)\n"
                        else:
                            code += (counterTabs*'\t') + "if self.curr_token.value == " + "'" + first + "': \n"
                            codeStack = []
                            counterTabs += 1
                            code += (counterTabs*'\t') + "self.expect(" + "'" + first + "')\n"
                        for c in range(1,steps):
                            n = prod_tokens[x+c]
                            print(n)
                            if n.type != "TOKEN":
                                code += (counterTabs*'\t') + n.value + "\n"
                        counterTabs -= 1
        elif prod_tokens[x].type == "TOKEN":
            if flag != None:
                pass
            else:
                code +=(counterTabs*'\t') + prod_tokens[x].value + "\n"

    
    print(code)
    return code

"""
IN: 
    productions: recibe el dict de las producciones del atg
    tokens: dict de los tokens del atg

OUT:
    <Dict> {"nombre_prod": [caracteres]}
"""
def first(productions, tokens):
    endings = [")", "}", "]"]

    dict_ntokens = {}
    new_tokens = []

    
    for l in productions:
        code = productions[l]
        counter = 0
        
        string = ""
        while counter < len(code):
            string += code[counter]
            clean_string = clean_str(string)
            if code[counter] == '"':
                
                if code[counter+1] not in endings:
                    new_tokens.append(code[counter+1])
                counter += 2
            elif clean_string in tokens:
                new_tokens.append(clean_string)
                string = ""
            elif clean_string in tokens:
                new_tokens.append(clean_string)
                string = ""
            counter +=1
        dict_ntokens[l] = new_tokens
        new_tokens = []

    
        
    
    for l in productions: 
        
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




def name_def(id):    
    function_list = id.split("<")
    string = ''
    string += "\t"+"def " + function_list[0] + "(self"
    if len(function_list) > 1:
        for i in function_list[1:]:
            i = i.replace(">", "")
            string +="," + i
    string += "):\n"

    return string, function_list[0]


def after_chars(first, ch):
    after = False
    for i in first:
        for x in i:
            if ch != x:
                after = True
    return after


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




def charLinea(code, productions, dict_ntokens, tokens_dict):
    endings = [")", "}", "]"]
    new_tokens = []
    counter = 0
    string = ""


    if "|" in code:
        code = code.strip()
        list1 = code.split("|")

        for x in list1:
            x = x.strip()
            string += x

            clean_string = clean_str(string)
            if x[0] == '"':                
                new_tokens.append(x[1])
            
            elif clean_string in tokens_dict:
                new_tokens.append(clean_string)
                string = ""
            elif clean_string in tokens_dict:
                new_tokens.append(clean_string)
                string = ""
            else:
                for l in productions:
                    for n in productions:
                        if str(n) in x:
                            new_tokens = dict_ntokens[n]
                            counter += 1
                        if counter > 0:
                            break
            
    else:
        while counter < len(code):
            if code[counter] == '"':
                
                if code[counter+1] not in endings:
                    new_tokens.append(code[counter+1])
                counter += 2
            counter +=1
        
        if len(new_tokens) == 0:
            
            for l in productions:
                for x in productions:
                    if str(x) in code:
                        new_tokens = dict_ntokens[x]
                        counter += 1
                    if counter > 0:
                        break   
    return new_tokens


def clean_str(string):
    string = string.replace("(","").replace(")","").replace("|","").strip().lower()
    return string


def clean(dict):
    dict["Expr"] = '''
    \t\twhile self.curr_token.type == 'number' or self.curr_token.type == 'decnumber' or self.curr_token.value == '-' or self.curr_token.value == '(':
    \t\t\tself.Stat()
    \t\t\tself.expect(";")
    \t\t\tself.expect(".")
    '''
    
    return dict