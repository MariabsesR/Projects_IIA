from csp import *
from utils import *
from logic import *

def csp_prop(formulas):
    # Variáveis
    variaveis = set()
    [variaveis.update(prop_symbols(x)) for x in formulas]

    variaveis_strings = [str(y) for y in list(sorted(variaveis))]

    kb = PropKB()
    [kb.tell(c) for c in formulas]
    limpa_clausulas(kb)
    # separa binarias para vizinhos e unarias para a definiçao dos dominios
    unarias = []
    binarias = []

    for expressao in kb.clauses:
        if expressao.op == '~' or len(expressao.args) == 0:
            unarias.append(expressao)
        else:
            binarias.append(expressao)
    
    # Domínios - com filtragem de restrições unárias
    dominios = {str(var): [False,True] for var in variaveis}

    for expressao in unarias:
        if expressao.op == '~' and len(expressao.args) == 1:
            dominios[str(expressao.args[0])].remove(True)
        elif len(expressao.args) == 0:
            dominios[str(expressao)].remove(False)
    
    # Vizinhos
    vizinhos = {str(var): [] for var in variaveis}

    # Para cada variável, verificar vizinhos nas cláusulas
    for a in variaveis:
        vizinhos_a = set()
        for clausula in binarias:
            if a in prop_symbols(clausula):
                for j in prop_symbols(clausula):
                    if j!=a:
                        vizinhos_a.add(str(j))
        vizinhos.update({str(a) : sorted(list(vizinhos_a))})

    def constraints(A, a, B, b):
        """Função que verifica se A = a e B = b eh aceite por todas as restriçoes onde A e B estao presentes"""
        x_exp = expr(A) if a else expr('~' + A)
        y_exp = expr(B) if b else expr('~' + B)
        
        mini_kb = PropKB()
        mini_kb.tell(x_exp)
        mini_kb.tell(y_exp)

        result = True
        for clausula in kb.clauses:
            # ambas variaveis estao na clausula
            simb = [str(s) for s in prop_symbols(clausula)]
            if A in simb and B in simb and not mini_kb.ask_if_true(clausula):
                result = False
                break
    
        return result

    return CSP(variaveis_strings, dominios, vizinhos, constraints)