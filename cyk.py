def cyk_parse(grammar, input_string):
    n = len(input_string)
    num_rules = len(grammar)

    # Inicializar una tabla de DP (programación dinámica) para almacenar los resultados intermedios
    table = [[set() for _ in range(n)] for _ in range(n)]

    # Llenar la diagonal principal de la tabla con las producciones correspondientes a las terminales
    for i in range(n):
        for rule in grammar:
            splitRule = rule[1].split(' ')
            for sl in splitRule:
                if input_string[i] == sl:
                    table[i][i].add(rule[0])

    # Calcular las entradas para las subcadenas de longitud creciente
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for rule in grammar:
                    for left in table[i][k]:
                        for right in table[k + 1][j]:
                            if left + ' ' + right in rule[1]:
                                table[i][j].add(rule[0])


    # Comprobar si el símbolo inicial está en la entrada correspondiente a toda la cadena
    if grammar[0][0] in table[0][n - 1]:
        return True
    else:
        return False


# Ejemplo de uso:
def main(grammar, input_string):
    # Define la gramática
    # grammar = [
    #     ('S', 'A B'),
    #     ('S', 'B A'),
    #     ('A', 'e'),
    #     ('A', 'A C'),
    #     ('A', 'A D'),
    #     ('B', 'd'),
    #     ('B', 'E B'),
    #     ('B', 'F B'),
    #     ('C', 'c'),
    #     ('D', 'd'),
    #     ('E', 'e'),
    #     ('F', 'f'),
    # ]

    # # Cadena de entrada
    # input_string = ("e c d f d").split(' ')

    # grammar = [
    #     ('S', 'NP VP'),
    #     ('NP', 'DET N'),
    #     ('VP', 'V NP'),
    #     ('DET', 'the'),
    #     ('N', 'cat'),
    #     ('V', 'chases')
    # ]

    # input_string = ('the').split(' ')
    input_string = input_string.split(' ')

    if cyk_parse(grammar, input_string):
        print("La cadena pertenece a la gramática.")
    else:
        print("La cadena no pertenece a la gramática.")

# main()