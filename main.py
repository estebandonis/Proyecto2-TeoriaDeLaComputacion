#Lista de todas las letra del alfabeto en mayuscula
import cyk as cykAlgorithm

def CFG(variables, terminales, rules):
    # Paso 1: Agregar reemplazar paso inicial
    first_key = next(iter(rules))
    newRules = {}
    newRules['S0'] = first_key
    newRules.update(rules)
    rules.clear()
    rules = newRules.copy()
    newVariables = []
    newVariables.append('S0')
    newVariables.extend(variables)
    variables.clear()
    variables = newVariables

    # Paso 2: BIN
    # Quitar reglas que contengan un terminales con no terminales
    rul = rules.copy()
    for i in rul:
        transition = rul[i]
        if type(transition) == list:
            trin = 0
            while trin < len(transition):
                tran = transition[trin]
                if (tran != 'epsilon' and any(char.isupper() for char in tran) and any(char.islower() for char in tran)):
                    strin = list(transition[trin])
                    numChar = 0
                    while numChar < len(strin):
                        char = strin[numChar]
                        if char.islower():
                            rules[char.upper()] = char
                            strin[numChar] = char.upper()
                            if char.upper() not in variables:
                                variables.append(char.upper())

                        numChar += 1
                    transition[trin] = ''.join(strin)
                    rules[i] = transition
                
                trin += 1

        else:
            if (transition != 'epsilon' and any(char.isupper() for char in transition) and any(char.islower() for char in transition)):
                if ' ' in transition:
                    transitions = transition.split(' ')
                    for a in transitions:
                        strin = list(a)
                        numChar = 0
                        while numChar < len(strin):
                            char = strin[numChar]
                            if char.islower():
                                rules[char.upper()] = char
                                strin[numChar] = char.upper()
                                if char.upper() not in variables:
                                    variables.append(char.upper())

                            numChar += 1
                        transitions[transitions.index(a)] = ''.join(strin)
                    rules[i] = ' '.join(transitions)
                else:
                    strin = list(transition)
                    numChar = 0
                    while numChar < len(strin):
                        char = strin[numChar]
                        if char.islower():
                            rules[char.upper()] = char
                            strin[numChar] = char.upper()
                            if char.upper() not in variables:
                                variables.append(char.upper())

                        numChar += 1
                    rules[i] = ''.join(strin)


    # Quitar reglas con más de 2 no terminales
    noMasdeTres = False
    prueba = 0
    while noMasdeTres == False:
        noMasdeTres = True
        rul = rules.copy()
        for k in rul:
            transition = rul[k]
            if type(transition) == list:
                trin = 0
                while trin < len(transition):
                    tran = transition[trin]
                    strin = tran.split(' ')
                    if 'epsilon' not in tran and len(strin) > 2:
                        noMasdeTres = False
                        letra = (strin[0]+strin[1])
                        newStri = letra + ' ' + ''.join(strin[2:])
                        if letra not in variables:
                            variables.append(letra)

                        transition[trin] = ''.join(newStri)
                        rules[k] = transition
                        rules[letra] = ' '.join(letra)
                    trin += 1

            else:
                strin = transition.split(' ')
                if 'epsilon' not in transition and len(strin) > 2:
                        noMasdeTres = False
                        letra = (strin[0]+strin[1])
                        newStri = letra + ' ' + ''.join(strin[2:])
                        if letra not in variables:
                            variables.append(letra)

                        transition = ''.join(newStri)
                        rules[k] = transition
                        rules[letra] = ' '.join(letra)


    # Paso 3: Eliminar producciones-ℇ
    rul = rules.copy()
    for i in rul:
        transition = rul[i]
        if type(transition) == list:
            trin = 0
            while trin < len(transition):
                tran = transition[trin]
                if tran == 'epsilon':
                    transition.remove(tran)
                    rules[i] = transition
                    for l in rules:
                        ltransition = rules[l]
                        if type(ltransition) == list:
                            for k in ltransition:
                                strinSplited = k.split(' ')
                                for letra in strinSplited:
                                    if letra == i:
                                        for letra in strinSplited:
                                            if letra != i:
                                                ltransition.append()
                                        if (l == 'S0'):
                                            ltransition.append('epsilon')
                                        rules[l] = ltransition
                        elif i == ltransition:
                            if type(ltransition) != list:
                                ltransition = list(ltransition)
                                if (l == 'S0'):
                                    ltransition.append('epsilon')
                                rules[l] = ltransition
                        else:
                            stringSplited = ltransition.split(' ')
                            for letra in stringSplited:
                                if letra == i:
                                    newList = []
                                    newList.append(ltransition)
                                    for letra in stringSplited:
                                        if letra != i:
                                            newList.append(letra)
                                    if (l == 'S0'):
                                        newList.append('epsilon')
                                    rules[l] = newList
                trin += 1

        else:
            if transition == 'epsilon':
                rules.pop(i)


    # Paso 4: Eliminar producciones unarias
    rul = rules.copy()
    for i in rul:
        transition = rul[i]
        if type(transition) == list:
            trin = 0
            while trin < len(transition):
                tran = transition[trin]
                splitedString = tran.split(' ')
                if len(splitedString) == 1 and tran.isupper():
                    transition.remove(tran)
                    for l in rules:
                        if l == tran:
                            if type(rules[l]) == list:
                                if type(transition) == list:
                                    transition = rules[l] + transition
                                    rules[i] = transition
                                else:
                                    rules[i] = transition
                            else:    
                                transition.append(rules[l])
                                rules[i] = transition
                trin += 1
        else:
            splitedString = transition.split(' ')
            if len(splitedString) == 1 and transition.isupper():
                if i != 'S0':
                    rules.pop(i)
                    for let in variables:
                        if let == i:
                            variables.remove(let)
                    for l in rules:
                        if type(rules[l]) == list:
                            for k in rules[l]:
                                if k == i:
                                    k = transition

                        else:
                            splitedStri = rules[l].split(' ')
                            for letra in splitedStri:
                                if letra == i:
                                    index_to_replace = splitedStri.index(letra)
                                    splitedStri[index_to_replace] = transition
                                    
                            rules[l] = ' '.join(splitedStri)
                
                else:
                    for l in rules:
                        if l == transition:
                            rules[i] = rules[l]


    # Paso 5: Eliminar producciones inaccesibles
    # Examinar que variables son alcanzables
    rul = rules.copy()
    alcanzables = []
    for i in rul:
        if i == 'S0':
            alcanzables.append(i)
            if type(rules[i]) == list:
                for k in rules[i]:
                    splitedString = k.split(' ')
                    for letra in splitedString:
                        alcanzables = agregarLetras(letra, alcanzables, rules)

            else:
                splitedString = rules[i].split(' ')
                for letra in splitedString:
                    alcanzables = agregarLetras(letra, alcanzables, rules)
    

    # Eliminar variables no alcanzables
    rul = rules.copy()
    for i in rul:
        if i not in alcanzables:
            rules.pop(i)
            for l in rules:
                if type(rules[l]) == list:
                    for k in rules[l]:
                        splitedStrin = k.split(' ')
                        for letra in splitedStrin:
                            if letra == i:
                                index_to_replace = splitedString.index(letra)
                                splitedString.pop(index_to_replace)
                                rules[l] = ' '.join(splitedStrin)
                else:
                    splitedString = rules[l].split(' ')
                    for letra in splitedString:
                        if letra == i:
                            index_to_replace = splitedString.index(letra)
                            splitedString.pop(index_to_replace)
                            rules[l] = ' '.join(splitedString)
            for let in variables:
                if let == i:
                    variables.remove(let)

    return variables, rules

# Funcion recursiva para agregar letras alcanzables    
def agregarLetras(letra, alcanzables, rules):
    if letra.isupper() and letra not in alcanzables:
        alcanzables.append(letra)
        for l in rules:
            if l == letra:
                if type(rules[l]) == list:
                    for ksa in rules[l]:
                        splitedStrings = ksa.split(' ')
                        for letras in splitedStrings:
                            if letras.isupper() and letras not in alcanzables:
                                alcanzables = agregarLetras(letras, alcanzables, rules)
                else:
                    splitedStringe = rules[l].split(' ')
                    for letrae in splitedStringe:
                        if letrae.isupper() and letrae not in alcanzables:
                            alcanzables.append(letrae)
                            alcanzables = agregarLetras(letrae, alcanzables, rules)

    return alcanzables

def main():

    variables = ['S', 'A', 'B', 'VP', 'PP', 'NP', 'V', 'P', 'N', 'DET']
    terminales = ['he', 'she', 'cooks', 'drinks', 'eats', 'cuts', 'in', 'with', 'cat', 'dog', 'beer', 'cake', 'juice', 'meat', 'soup', 'fork', 'knife', 'oven', 'spoon', 'a', 'the']
    rules = { 
        'S': 'A B',
        'A': 'NP',
        'B': 'VP',
        'VP': ['VP PP', 'V NP', 'cooks', 'drinks', 'eats', 'cuts'],
        'PP': 'P NP',
        'NP': ['DET N', 'he', 'she'],
        'V': ['cooks', 'drinks', 'eats', 'cuts'],
        'P': ['in', 'with'],
        'N': ['cat', 'dog', 'beer', 'cake', 'juice', 'meat', 'soup', 'fork', 'knife', 'oven', 'spoon'],
        'DET': ['a', 'the', 'an']
    }

    variables, rules = CFG(variables, terminales, rules)

    # Tranformacion a lista para algoritmo CYK
    listRules = []
    for rule in rules:
        if type(rules[rule]) == list:
            for r in rules[rule]:
                listRules.append((rule, r))
        else:
            listRules.append((rule, rules[rule]))


    print('CYK')
    # input_phrase = 'she cooks a cake in the oven'
    # print('Frase semánticamente correcta 1:', input_phrase)
    # cykAlgorithm.main(listRules, input_phrase)

    # input_phrase = 'he cuts a meat with a knife'
    # print('Frase semánticamente correcta 2:', input_phrase)
    # cykAlgorithm.main(listRules, input_phrase)

    # input_phrase = 'a cat drinks a cake with an oven'
    # print('Frase semánticamente incorrecta 1:', input_phrase)
    # cykAlgorithm.main(listRules, input_phrase)

    # input_phrase = 'the dog drinks a spoon in a beer'
    # print('Frase semánticamente incorrecta 2:', input_phrase)
    # cykAlgorithm.main(listRules, input_phrase)

    # input_phrase = 'he eat cake'
    # print('Frase no perteneciente al lenguaje 1:', input_phrase)
    # cykAlgorithm.main(listRules, input_phrase)

    input_phrase = 'dog cut beer'
    print('Frase no perteneciente al lenguaje 2:', input_phrase)
    cykAlgorithm.main(listRules, input_phrase)

main()
