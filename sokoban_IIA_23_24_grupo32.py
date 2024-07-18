from planningPlus import *
from logic import *
from utils import *
from search import *

""" Verifica se uma posicao é parede ou reachable """
def isNavegavel(simbolo):
       if simbolo == '#' or simbolo == ' ':
            return False
       return True

""" Recebe uma posicao que é navegavel
e retorna uma lista das ações Andar que são possiveis na posicao [y][x]"""
def getAndarActions(matrix, y, x):
    andar_actions = []

    if y < len(matrix) - 1 and isNavegavel(matrix[y + 1][x]):
        precond = expr(f'Sokoban(C_{y}_{x}) & ~Sobre(C_{y + 1}_{x})')
        effect = expr(f'Sokoban(C_{y + 1}_{x}) & ~Sokoban(C_{y}_{x})')
        andar_actions.append(Action(expr(f'Andar(C_{y}_{x}, C_{y + 1}_{x})'), precond, effect))

    if y > 0 and isNavegavel(matrix[y - 1][x]):
        precond = expr(f'Sokoban(C_{y}_{x}) & ~Sobre(C_{y - 1}_{x})')
        effect = expr(f'Sokoban(C_{y - 1}_{x}) & ~Sokoban(C_{y}_{x})')
        andar_actions.append(Action(expr(f'Andar(C_{y}_{x}, C_{y - 1}_{x})'), precond, effect))

    if x < len(matrix[y]) - 1 and isNavegavel(matrix[y][x + 1]):
        precond = expr(f'Sokoban(C_{y}_{x}) & ~Sobre(C_{y}_{x + 1})')
        effect = expr(f'Sokoban(C_{y}_{x + 1}) & ~Sokoban(C_{y}_{x})')
        andar_actions.append(Action(expr(f'Andar(C_{y}_{x}, C_{y}_{x + 1})'), precond, effect))

    if x > 0 and isNavegavel(matrix[y][x - 1]):
        precond = expr(f'Sokoban(C_{y}_{x}) & ~Sobre(C_{y}_{x - 1})')
        effect = expr(f'Sokoban(C_{y}_{x - 1}) & ~Sokoban(C_{y}_{x})')
        andar_actions.append(Action(expr(f'Andar(C_{y}_{x}, C_{y}_{x - 1})'), precond, effect))

    return andar_actions

"""Verifica se posicao é um canto
canto sao todas as posicoes que fazem com que uma caixa fique presa sem que se consiga mover
ou seja 2 paredes adjacentes e posicao nao é objetivo"""
def isCanto(matrix,y,x):
    # posicao é objetivo logo nao é canto
    if matrix[y][x] == 'o' or matrix[y][x] == '+' or matrix[y][x] == '*':
        return False
    # posicao tem paredes adjacentes e nao é objetivo
    if (not isNavegavel(matrix[y-1][x]) or not isNavegavel(matrix[y+1][x])) and (not isNavegavel(matrix[y][x-1]) or not isNavegavel(matrix[y][x+1])):
         return True
    return False

""""Retorna todas as açoes "Empurrar(p1,p2,p3)" possiveis apartir de  uma dada
posicao. 
Empurrar se posicao p3 for navegável ou seja nao for parede nem ' ' e se p3 nao for um canto sem objetivo (caixa pode ficar presa)"""
def getValidPushes(matrix, y, x):
    empurrar_actions = []

    # Empurrar para sul
    if y + 2 < len(matrix) and isNavegavel(matrix[y + 1][x]) and isNavegavel(matrix[y + 2][x]) and not isCanto(matrix,y+2,x):
        precond = expr(f'Sokoban(C_{y}_{x}) & Sobre(C_{y + 1}_{x}) & ~Sobre(C_{y + 2}_{x})')
        effect = expr(f'Sokoban(C_{y + 1}_{x}) & ~Sokoban(C_{y}_{x}) & Sobre(C_{y + 2}_{x}) & ~Sobre(C_{y + 1}_{x})')
        empurrar_actions.append(Action(expr(f'Empurrar(C_{y}_{x}, C_{y + 1}_{x}, C_{y + 2}_{x})'), precond, effect))

    # Empurrar para este
    if x + 2 < len(matrix[y]) and isNavegavel(matrix[y][x + 1]) and isNavegavel(matrix[y][x + 2]) and not isCanto(matrix,y,x+2):
        precond = expr(f'Sokoban(C_{y}_{x}) & Sobre(C_{y}_{x + 1}) & ~Sobre(C_{y}_{x + 2})')
        effect = expr(f'Sokoban(C_{y}_{x + 1}) & ~Sokoban(C_{y}_{x}) & Sobre(C_{y}_{x + 2}) & ~Sobre(C_{y}_{x + 1})')
        empurrar_actions.append(Action(expr(f'Empurrar(C_{y}_{x}, C_{y}_{x + 1}, C_{y}_{x + 2})'), precond, effect))

    # Empurrar para oeste
    if x - 2 > 0 and isNavegavel(matrix[y][x - 1]) and isNavegavel(matrix[y][x - 2]) and not isCanto(matrix,y,x-2):
        precond = expr(f'Sokoban(C_{y}_{x}) & Sobre(C_{y}_{x - 1}) & ~Sobre(C_{y}_{x - 2})')
        effect = expr(f'Sokoban(C_{y}_{x - 1}) & ~Sokoban(C_{y}_{x}) & Sobre(C_{y}_{x - 2}) & ~Sobre(C_{y}_{x - 1})')
        empurrar_actions.append(Action(expr(f'Empurrar(C_{y}_{x}, C_{y}_{x - 1}, C_{y}_{x - 2})'), precond, effect))

    # Empurrar para norte
    if y - 2 > 0 and isNavegavel(matrix[y - 1][x]) and isNavegavel(matrix[y - 2][x]) and not isCanto(matrix,y-2,x):
        precond = expr(f'Sokoban(C_{y}_{x}) & Sobre(C_{y - 1}_{x}) & ~Sobre(C_{y - 2}_{x})')
        effect = expr(f'Sokoban(C_{y - 1}_{x}) & ~Sokoban(C_{y}_{x}) & Sobre(C_{y - 2}_{x}) & ~Sobre(C_{y - 1}_{x})')
        empurrar_actions.append(Action(expr(f'Empurrar(C_{y}_{x}, C_{y - 1}_{x}, C_{y - 2}_{x})'), precond, effect))

    return empurrar_actions

def get_actions(matrix):
    acoes = []
    # adicionamos action se for possivel 1) andar 2) empurrar
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if isNavegavel(matrix[y][x]):
                acoes.extend(getAndarActions(matrix, y, x))
                acoes.extend(getValidPushes(matrix,y,x))
                    
                 
    return acoes

def parse_puzzle(puzzle):
       # Transformar puzzle em matriz para ser mais facil de manipular
       matrix = [list(line) for line in puzzle.strip().split('\n')]
       # estado = lista de expr
       estado = PropKB()
       goal = []
       objetivo_pos = []
       isSokoban = False
        
       for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                if isNavegavel(matrix[y][x]):
                    # estado tem posicao sokoban
                    # sokoban no chao , sokoban num objetivo
                    if matrix[y][x] == '@' or matrix[y][x] == '+':
                        estado.tell(expr(f"Sokoban(C_{y}_{x})"))
                        isSokoban = True
                    else:
                        estado.tell(expr(f"~Sokoban(C_{y}_{x})"))
                    # posicao caixas
                    # Caixa no chao, caixa no objetivo
                    if matrix[y][x] == '$' or matrix[y][x]  == '*':
                        estado.tell(expr(f"Sobre(C_{y}_{x})"))
                    else:
                        estado.tell(expr(f"~Sobre(C_{y}_{x})"))
                    
                    # Para fazer GOAL objetivo , sokoban num objetivo , caixa num objetivo
                    if matrix[y][x] == 'o' or matrix[y][x] == '+' or matrix[y][x] == '*':
                        objetivo_pos.append((y,x))

       #goal
       strings_caixas_sobre_objetivos = [f'Sobre(C_{y}_{x}) & ' for ((y, x)) in objetivo_pos]
       goal_str = ''.join(strings_caixas_sobre_objetivos)
       goal = goal_str[:-2]
       return estado,goal,matrix

def sokoban(puzzle):
    # representar estado : parse puzzle para tuplo que contem (posicaoSokoban , kb)
    # kb = dominio
    (estado , goal , matrix) = parse_puzzle(puzzle)
    th = PlanningProblem(initial=estado.clauses, goals=goal, actions= [], domain= [])
    p = ForwardPlan(th)
    p.expanded_actions = get_actions(matrix)
    return p