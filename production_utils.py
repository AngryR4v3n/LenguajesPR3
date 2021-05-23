import sys
import os
sys.path.append(os.path.abspath(os.path.join("AFD/AFN")))
import tokenizer as Token
def production_tokens(key, string, production_dict, token_dict):
    tokens = []
    skip = 0
    operator = ""
    exclude = ['[', '{', '}', ']', '|', '"', "(", "<"]
    current = 0
    counter = 0
    stack = []
    symb_to_ignore = first_v2(production_dict)
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

            if is_production:
                if ch == "<":
                    buffer = ""
                    while ch != ">":
                        ch = string[i]
                        buffer += ch
                        i += 1
                    buffer = buffer.replace("<", "(").replace(">", ")")
                    vals = buffer.split("(")[1].replace(")", "")

                    code = vals + " = " + "self." + operator.strip() + buffer
                    tkk = Token.Tokenizer(type_t="PRODUCTION", value=f"{code}", identifier=None)
                    stack.append(tkk)
                else:
                    tkk = Token.Tokenizer(type_t="PRODUCTION", value=f"self.{operator}()", identifier=None)
                    stack.append(tkk)
                
                
            if is_token:
                print("found token!")


            if ch == "{":

                buffer = ""
                while ch != "}":
                    ch = string[i]
                    buffer += ch
                    i += 1
                buffer = buffer.replace("{", "").replace("}", "")
                first_de_linea = firstCode(buffer, production_dict, symb_to_ignore)
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

                x = firstCode(buffer, production_dict, symb_to_ignore)
                tkk_if = Token.Tokenizer(type_t="IF", value="if()", identifier=[])
                tkk_if.identifier = x
                stack.append(tkk_if)
                
            elif ch == "}":
                tkk = Token.Tokenizer(type_t="ENDWHILE", value="", identifier=None)
                stack.append(tkk)

            elif ch == "]":
                tkk = Token(type_t="ENDIF", value="", identifier=None)
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
            first_de_linea = firstCode(string[i:], production_dict, symb_to_ignore)
            stack.append(Token.Tokenizer(type_t="CODE", value=x[2:], identifier=first_de_linea))

        #if entre parentesis
        elif ch == "(" and follow_ch != ".":
            buffer = ""
            while ch != ")":
                ch = string[i]
                buffer += ch
                i += 1

            x = firstCode(buffer, production_dict, symb_to_ignore)
            tkk_if = Token.Tokenizer(type_t="IFP", value="if()", identifier=x)
            stack.append(tkk_if)

        current += 1


    return stack

def code_prods(prod_tokens):
    code = ""
    flagWhile = None
    counterPipes = 0
    counterTabs = 1
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
            code += (counterTabs*'\t') + "if lastToken == " + "'" + first[0] + "': \n"
            counterTabs += 1
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

        elif prod_tokens[x].type == "ENDWHILE":
            flagWhile = None
            counterTabs -= 1
        elif prod_tokens[x].type == "PIPE":
            steps = x - flagWhile + 1
            firstWhile = prod_tokens[flagWhile].identifier
            for i in firstWhile:
                first = i 
                counterPipes += 1
                if counterPipes <= 1:
                    code += (counterTabs*'\t') + "if lastToken == " + "'" + first + "': \n"
                    codeStack = []
                    counterTabs += 1 

                    #Aqui viene lo que esta dentro del if
                    for c in range(1,steps-1):
                        innerCode = ""
                        n = prod_tokens[x-c]
                        print(n)
                        innerCode = (counterTabs*'\t') + n.value + "\n"
                        codeStack.append(innerCode)


                    counterTabs -= 1 
                    reverCodeStack = codeStack.copy()
                    reverCodeStack.reverse()
                    
                    code += ''.join(reverCodeStack)


                else:
                    code += (counterTabs*'\t') + "if lastToken == " + "'" + first + "': \n"
                    counterTabs += 1
                    for c in range(1,steps):
                        
                        n = prod_tokens[x+c]
                        print(n)
                        code += (counterTabs*'\t') + n.value + "\n"

                    counterTabs -= 1

    
    print(code)
    return code




        


        
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
        if val == elem:
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






def first_v2(productions):
    endings = [")", "}", "]"]
    #productions = {'expr': 'codigo'}
    #dict_ntokens = {'expr': [+, *]}
    #expr hace refencia a term y term tiene -, / 
    dict_ntokens = {}
    new_tokens = []
    for l in productions:
        code = productions[l]
        counter = 0
        #revise unicamente los ")" que estan dentro del codio de la produccion 
        while counter < len(code):
            if code[counter] == '"':
                #OJO LO MEJOR ES ANALIZAR POR EL | Y HACER SPLIT PARA SABER CUANTOS HAY EN EL PRIMERO 
                if code[counter+1] not in endings:
                    new_tokens.append(code[counter+1])
                counter += 2
            counter +=1
        dict_ntokens[l] = new_tokens
        new_tokens = []
        
    #revisar los ")" que esten dentro de las funciones a las que haga referencia la produccion
    
    for l in productions: #l es la produccion que estoy leyendo
        #si esta vacio significa que no tiene terminales y busca en la primera referencia
        if len(dict_ntokens[l]) == 0:
            code = productions[l]
            counter = 0
            for x in productions:
                if str(x) in code:
                    additional_tokens=dict_ntokens[x]
                    dict_ntokens[l] = additional_tokens
                    counter += 1
                if counter > 0:
                    break   

    return dict_ntokens



def firstCode(code, productions, dict_ntokens):
    endings = [")", "}", "]"]
    new_tokens = []
    counter = 0
    if "|" in code:
        code = code.strip()
        list1 = code.split("|")
        for x in list1:
            x = x.strip()
            if x[0] == '"':                
                new_tokens.append(x[1])
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