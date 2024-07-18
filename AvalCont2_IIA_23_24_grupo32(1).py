

#Grupo 32
#nº58208 Maria Rocha
#nº57596 Ana Sa



#PERGUNTA 1---------------------------------------------------------------------------------------

import queue
from MedoTotal import * 

class MedoTotalTurbo(MedoTotal):
    """A variant of MedoTotal that uses real distances for anticipation of failure."""
    def __init__(self, texto_input=mundoStandard):
        super().__init__(texto_input)
       # self.distances = self.calculate_real_distances()

    def calculate_real_distances(self):
        distances = {}
        
        for i in range(self.dim):
            for j in range(self.dim):
                if (j, i) not in self.obstacles and (j, i) != self.fantasma:
                    distances[(j, i)] = self.calculate_distances_from((j,i),self.initial)
        return distances
    
    #primeiro calcular distancia entre todas as navegaveis ate á pastilha mais proxima
    #chamar calculate distances para cada uma das pastilhas
    #apos mantemos so a pastilha mais proxima
    #fazer algoritmo largura
     
    def calculate_distances_from(self,start,end):
        
        # NORTE, WEST, EAST, SUL
        moves = [(0, -1), (-1, 0), (1, 0), (0, 1)]
        
        #fronteira queue
        fronteira = FIFOQueue()
        explorados = set()
        custo = 0
        
        # inc custo sempre que
        fronteira.append((start, custo))
        
        while fronteira:
            (node,custo) = fronteira.pop()
            if node == end and node != start:
                return custo
            
            explorados.add(node)
            # testamos todos os moves possiveis a e b eh delta x, y
            for (a,b)  in moves:
                #start position
                (j,i) = node
                posicao_a_testar = (j+a,i+b)
                if 0 <= j+a < self.dim and 0 <= i+b < self.dim:
                    # adicionar á fronteira se nao for obstaculo ou fantasma e nao estiver em explorados
                    if posicao_a_testar not in explorados and posicao_a_testar not in fronteira and posicao_a_testar != self.fantasma and posicao_a_testar not in self.obstacles and self.goal-custo >= 0:
                        fronteira.append((posicao_a_testar,custo+1))
       
        
        return None
    
    def falha_antecipada(self,state):
        if state.tempo <= state.medo:
            return False
        if state.pastilhas == set(): # se não há mais pastilhas e eram necessárias
            return True
        minDist = min(list(map(lambda x: self.calculate_distances_from(state.pacman,x),state.pastilhas)))
      
        if minDist > state.medo: # se não há tempo (manhatan) para chegar à próxima super-pastilha
            return True
        if (state.medo + self.poder * len(state.pastilhas)) < state.tempo:
            # se o poder de todas as pastilhas mais o medo são insuficientes.
            return True
        
      
        return False
    
    def actions(self, state):
        """Podes mover-te para uma célula em qualquer das direcções para uma casa 
           que não seja obstáculo nem fantasma."""
        x, y = state.pacman
      
        
                    
            
        return [act for act in self.directions.keys() 
                if (x+self.directions[act][0],y+self.directions[act][1]) not in (self.obstacles | {self.fantasma}) and 
                not self.falha_antecipada(self.result(state,act)) ]
        
        
        
        
        
        
    	
#PERGUNTA 2 -----------------------------------------------------------------------------------------------------------------------------------------

from MedoTotal import * 

from MedoTotal import *
from searchPlus import Node, Stack

def depth_first_tree_search_all_count(problem, optimal=False, verbose=False):
    # stack porque algoritmo profundidade
    frontier = Stack()
    
    resultado = None
    visitados = 0
    finais = 0
    
    frontier.append(Node(problem.initial))
    max_mem = 1
    
    while frontier:
        
        if len(frontier) > max_mem:
            max_mem = len(frontier)
            
        node = frontier.pop()
        visitados+=1

        
        if verbose:
            print("---------------------\n")
            print(problem.display(node.state))
            print("Custo:", node.path_cost)
        
        #alterar forma como child nodes sao armazenados na stack
        child_nodes = node.expand(problem)
        
        #adicionamos a fronteira se nao for estado final
        # se for estado final - inc estado final e se verbose imprime
        toAdd = []
        for child in child_nodes:
            if(problem.goal_test(child.state)):
                # nao visita estados que sejam piores que resultado no optimal
                if resultado is None or not optimal or (optimal and child.path_cost < resultado.path_cost):
                    finais+=1
                    visitados+=1
                    if verbose:
                        print("---------------------\n")
                        print(problem.display(child.state))
                        print("GGGGooooooallllll --------- com o custo:", child.path_cost)
                    if resultado is None or child.path_cost < resultado.path_cost:
                        resultado = child
                        if verbose:
                            print("Di best goal até agora")
            else:
                if not optimal:
                    toAdd.append(child)
                elif resultado is None:
                    toAdd.append(child)
                elif optimal and child.path_cost < resultado.path_cost:
                    toAdd.append(child)
                    
        #porque ordem do stor no verbose esta diferente tive de fazer extra step
        toAdd = toAdd[::-1]
        frontier.extend(toAdd)
            
                    
    return resultado, max_mem, visitados, finais


#PERGUNTA 3------------------------------------------------------------------------------------

from MedoTotal import *
from GrafoAbstracto import *

def ida_star_graph_search_count(problem, f, verbose=False):
    
    def depth_first_limited_search(problem, limiar, visitados, expandidos, frontier):
        
        f_exceded = []
        
        if verbose and visitados > 1:
            print("")
            print("------Cutoff at",limiar)
            print("")
            
        while frontier:
            
            node = frontier.pop()
            expandidos.add(node)
            
            if problem.goal_test(node.state) and f(node) <= limiar:
                if verbose:
                    print(problem.display(node.state))
                    print("Cost:", node.path_cost,"f=",f(node))
                    print("Goal found within cutoff!")
                return node,visitados
                
            if f(node)>limiar:
                f_exceded.append(f(node))
                if verbose:
                    print(problem.display(node.state))
                    print("Cost:", node.path_cost,"f=",f(node))
                    print("Out of cutoff -- minimum out:",f(node))
                    print("")
            else:
                #se o f for menor ou igual a loimiar e nao for uma solucao adiciona filhos
                for child  in node.expand(problem)[::-1]:
                    if(child not in expandidos and child not in frontier ):
                        frontier.append(child)
                        visitados+=1
                       
                if verbose:
                    print(problem.display(node.state))
                    print("Cost:", node.path_cost,"f=",f(node))
                    if frontier or len(f_exceded) > 0:
                        print("")
                
        if f_exceded:
            frontier = Stack()
            frontier.append(Node(problem.initial))                  
            return depth_first_limited_search(problem, min(f_exceded), visitados+1, set(), frontier)
        else:
            return None,visitados
        
    
    # inicializacao das variaveis para iniciar pesquisa profundidade limitada
    
    frontier = Stack()
    frontier.append(Node(problem.initial))
    limiar = f(Node(problem.initial))
    if verbose:
        print("------Cutoff at",limiar)
        print("")
    return depth_first_limited_search(problem, limiar, 1, set(), frontier)