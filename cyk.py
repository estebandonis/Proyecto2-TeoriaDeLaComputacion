import tabulate
import pydotplus
import time


class Node:
    def __init__(self, label):
        self.label = label
        self.children = []


def build_syntax_tree(grammar, table, start, end):
    if start == end:
        # If we have a single non-terminal symbol in the cell, return it as a leaf node
        return Node(table[start][end].pop())
    else:
        for k in range(start, end):
            for rule in grammar:
                for left in table[start][k]:
                    for right in table[k + 1][end]:
                        if left + ' ' + right in rule[1]:
                            # Create a new node for this production
                            root = Node(rule[0])
                            # Recursively build the left and right subtrees
                            left_tree = build_syntax_tree(
                                grammar, table, start, k)
                            right_tree = build_syntax_tree(
                                grammar, table, k + 1, end)
                            root.children = [left_tree, right_tree]
                            return root
    return None


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

        return table, 0, n - 1
    else:
        return False, None, None


# Ejemplo de uso:
def main(grammar, input_string):
    input_string = input_string.split(' ')

    start_time = time.time()

    table, start, end = cyk_parse(grammar, input_string)
    
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Tiempo en validación: {elapsed_time} segundos")

    if table:
        pydotplus.find_graphviz()
        # Create a Graphviz graph for the syntax tree
        dot = pydotplus.Dot()
        dot.set_rankdir("TB")
        dot.set_prog("neato")

        def add_nodes_and_edges(node):
            if node:
                node_id = str(id(node))
                node_label = node.label.replace(
                    " ", "\n")  # Handle spaces in labels
                dot_node = pydotplus.Node(node_id, label=node_label)
                dot.add_node(dot_node)
                for child in node.children:
                    child_id = str(id(child))
                    dot_edge = pydotplus.Edge(node_id, child_id)
                    dot.add_edge(dot_edge)
                    add_nodes_and_edges(child)

        syntax_tree = build_syntax_tree(grammar, table, start, end)

        print("La cadena pertenece a la gramática.")

        print(tabulate.tabulate(table, tablefmt="fancy_grid"))

        # Add nodes and edges to the Graphviz graph
        add_nodes_and_edges(syntax_tree)

        # Save or display the graph
        dot_file_path = "graph.dot"
        dot.write(dot_file_path, format="dot")  # Save DOT file
        dot.write_png('syntax_tree.png')  # Save PNG file
        dot.write_svg("syntax_tree.svg")  # Save SVG file

    else:
        print("La cadena no pertenece a la gramática.")


def print_syntax_tree(node, indent):
    if node:
        print(" " * indent + node.label)
        for child in node.children:
            print_syntax_tree(child, indent + 2)
