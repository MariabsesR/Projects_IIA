
from searchPlus import *
import copy

parametros="T=26\nM=6\nP=10"
linha1= "= = = = = = = = = =\n"
linha2= "= @ . * . . * . . =\n"
linha3= "= . = = = = = = . =\n"
linha4= "= . = F . . . . . =\n"
linha5= "= . = . . . . . . =\n"
linha6= "= . = . . . . . . =\n"
linha7= "= . = . . . . . . =\n"
linha8= "= * . . . . . . . =\n"
linha9= "= . . . . . . . . =\n"
linha10="= = = = = = = = = =\n"
grelha=linha1+linha2+linha3+linha4+linha5+linha6+linha7+linha8+linha9+linha10
mundoStandard=parametros + "\n" + grelha

class EstadosMedoTotal:
    #inicializa os atributos de um estado
    def __init__(self,t,m ,grid,pacman_pos,pastilhas_pos,fantasmas_pos):
        self.grid = grid
        self.pacman_pos = pacman_pos
        self.pastilhas_pos = pastilhas_pos
        self.fantasmas_pos = fantasmas_pos
        self.m = m
        self.t=t
    #verifica se ambos os estados apresentados apresentam o mesmo custo de entrada em todas as posições
    def equalCosts(self, other):
        for y, row in enumerate(self.grid):
            for x, (s, c) in enumerate(row):
                if self.grid[y][x][1] != other.grid[y][x][1]:
                    return False
        return True
    
    #verifica igualdade dos estados ou seja atributos que podem ser modificados ao longo do jogo 
    def __eq__(self,other):        
                    
        return (self.pacman_pos == other.pacman_pos
                and self.pastilhas_pos == other.pastilhas_pos
                and self.fantasmas_pos == other.fantasmas_pos
                and self.t == other.t
                and self.m == other.m
                and self.equalCosts(other))
    
class MedoTotal(Problem):
    
    #inicializa o jogo 
    def __init__(self, situacaoInicial=mundoStandard):
        #recebe um EstadosMedoTotal, divide a grid por \n  e guarda os seus atributos
        data = situacaoInicial.split("\n") 
        t = int(data[0].split("=")[1])
        m = int(data[1].split("=")[1])
        p = int(data[2].split("=")[1])
        
        self.p = p
        self.dim  = len(data[3:]) -1
       
        
        pacman_pos = (-1,-1)
        pastilhas_pos = []
        fantasmas_pos = []
        
        grid = []
        for y, line in enumerate(data[3:]):
            line = line.replace(" ", "")  # Remove os espaços na linha
            row = []
            for x, symbol in enumerate(line):
                if symbol == '@': #encontra e guarda a posicao do pacman, sendo que nesta posicao tem de estar associado um custo 1
                    pacman_pos = (y,x)
                    row.append((symbol, 1))
                else:
                    row.append((symbol, 0))#se o pacman naoe stiver na posicao esta associado um custo 0
                if symbol == '*':
                    pastilhas_pos.append((y,x))# guarda as posicoes das pastilhas
                elif symbol == 'F':
                    fantasmas_pos.append((y,x))#guarda as posicoes dos fantasmas
            grid.append(row)
        
        self.initial = EstadosMedoTotal(t,m,grid,pacman_pos,pastilhas_pos,fantasmas_pos) #inicializa o estado inicial do jogo 

    def distancia_manhattan(self,pacman, pastilha):
        #Calcula a distancia de Manhattan entre o pacman e a pastilha
        x1, y1 = pacman
        x2, y2 = pastilha
        return abs(x1 - x2) + abs(y1 - y2) 
    
    def instantes_pastilha_proxima(self,state):
        pacman_pos = state.pacman_pos
        pastilhas_pos = state.pastilhas_pos
        
        pastilha_mais_proxima = pastilhas_pos[0]
        distancia_min = self.distancia_manhattan(pacman_pos, pastilha_mais_proxima)
        #percorre todas as posiçoes das pastilhas para encontrar a mais proxima
        for pastilha_pos in pastilhas_pos[1:]:   
            distance = self.distancia_manhattan(pacman_pos, pastilha_pos)
            if distance < distancia_min:
                distancia_min = distance
                pastilha_mais_proxima = pastilha_pos
        return distancia_min
    
    #soma de todos os poderes da pastilha em jogo
    def soma_todas_pastilhas(self,state):
        return len(state.pastilhas_pos)*self.p
    #verifica se o jogo se encontra terminado
    def goal_test(self, state):
        return state.t <= 0 and state.m > 0
    #encontra as possiveis acoes do pacman na posicao atual 
    def actions(self, state):
        (y, x) = state.pacman_pos
        actions = []
        #Se o Pacman está com medo de intensidade inferior aos instantes de medo necessários ainda para atingir o objectivo e já não há super-pastilhas. 
        # Se o Pacman está com medo de intensidade inferior aos instantes de medo necessários ainda para atingir o objectivo e a distância à super-pastilha mais próxima implicar mais instantes do que a intensidade de medo no fantasma.
        if state.m < state.t and (not state.pastilhas_pos or self.instantes_pastilha_proxima(state) > state.m):
            return actions
        # Se o Pacman está com medo de intensidade inferior aos instantes de medo necessários ainda para atingir o objectivo e 
        # tem medo suficiente para atingir pelo menos uma super-pastilha, mas a soma dos poderes de todas as super-pastilhas com a distância 
        # à super-pastilha mais próxima é menor do que os instantes de medo que faltam ainda para atingir o objectivo.

        if (
            state.m < state.t
            and self.instantes_pastilha_proxima(state) <= state.m
            and self.soma_todas_pastilhas(state) + self.instantes_pastilha_proxima(state) < state.t
        ):
            return actions
        #adiciona ao array as possiveis acoes 
        if state.grid[y - 1][x][0] != "=" and state.grid[y - 1][x][0] != "F":
            actions.append("N")
        if state.grid[y][x - 1][0] != "=" and state.grid[x - 1][y][0] != "F":
            actions.append("W")
        if state.grid[y][x + 1][0] != "=" and state.grid[y][x + 1][0] != "F":
            actions.append("E")
        if state.grid[y + 1][x][0] != "=" and state.grid[y + 1][x][0] != "F":
            actions.append("S")
        return actions

    #cria uma copia do novo estado apos uma acao ter sido realizada     
    def result(self, state, action):
        new_copy = copy.deepcopy(state)
        (y,x)=new_copy.pacman_pos
        new_copy.grid[y][x]=(".",new_copy.grid[y][x][1]) # aqui trocamos a posiçao onde o pacman se encontrava para vazia 
        #nova posicao do pacman
        if action =="N":
            (y,x)=(y-1,x)
        elif action =="S":
            (y,x)=(y+1,x)
        elif action =="E":
            (y,x)=(y,x+1)   
        elif action =="W":
            (y,x)=(y,x-1)
        
        comeu_pastilha = 0
        new_copy.pacman_pos=(y,x)
        #se a nova posicao do pacman for a de uma pastilha entao atualiza o medo
        if new_copy.pacman_pos in new_copy.pastilhas_pos:
            comeu_pastilha = 1
            new_copy.m = self.p
            new_copy.pastilhas_pos.remove(new_copy.pacman_pos)    
        #vai buscar o custo de entrar na nova posicao e adiciona +1 ao custo    
        n_visits=(new_copy.grid[y][x][1])
        new_copy.grid[y][x]=("@",n_visits+1) # colocamos o pacman no seu novo sitio
        new_copy.t=new_copy.t-1 #retira um t ao pacman para significar que este se moveu
        #se nao comeu pastilha o medo do fantasma ira diminuir -1
        if comeu_pastilha == 0: 
            new_copy.m=new_copy.m-1
        return new_copy
    
    #custo de passar de um estado ao outro, a  nova posicao do pacman deve ser adjacente a anterior
    def path_cost(self, c, state1,action,next_state):
        (y,x) = next_state.pacman_pos
        return c + next_state.grid[y][x][1]
    #executa programa 
    def executa(p,estado,accoes,verbose=False):
        """Executa uma sequência de acções a partir do estado devolvendo o triplo formado pelo estado, 
        pelo custo acumulado e pelo booleano que indica se o objectivo foi ou não atingido. Se o objectivo for atingido
        antes da sequência ser atingida, devolve-se o estado e o custo corrente.
        Há o modo verboso e o não verboso, por defeito."""
        custo = 0
        for a in accoes:
            seg = p.result(estado,a)
            custo = p.path_cost(custo,estado,a,seg)
            estado = seg
            objectivo=p.goal_test(estado)
            if verbose:
                print('Custo Total:',custo)
                print('Atingido o objectivo?', objectivo)
            if objectivo:
                break
        return (estado,custo,objectivo)
    
    def display(self, state):
        #Devolve a grelha em modo txt
        ret = ""
        counter = 0
        for y, row in enumerate(state.grid):
            for x, (s, c) in enumerate(row):
                ret += s + " "
                counter +=1
                if counter == self.dim:
                    ret += '\n'
                    counter = 0
        return ret