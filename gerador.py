from typing import List
import random as rdm

'''
conteudo da entrada:
    coroa; escudo; espada; bandeira; cavaleiro; martelo; balança; 
    (id_ação, posição1, posição2)*;


    ações:
    - place : 1,p1;
    - hide : 2,p1;
    - swap : 3,p1,p2;
    - peek : 4,p1; || 4,p1,p2,p3;
    - challenge: 5,p1;
    - boast: 6
    - boast I: 7
    - boast II: 8
    - boast III: 9

'''
class Pedra():
    
    def __init__(self, nome):
        self.nome = nome
        self.posicao = 'F' # F = 70, ? = 63
        self.oculta = False

    def __str__(self):
        return f'({self.nome},{self.posicao},{self.oculta})'

    def __repr__(self):
        return self.__str__()

class Jogo():
    def __init__(self, pedras: List[Pedra], num_acoes):
        self.pedras = pedras
        
        self.fora  = list(pedras)
        rdm.shuffle(self.fora)
        
        self.pista = []
        
        self.oculta = []
        self.nao_oculta = []
        rdm.shuffle(self.nao_oculta)

        self.conhecidas = [None]*(num_acoes)
        
        self.posicoes_lives = [4, 4]
        self.jogador = False
        self.acoes = ['']*num_acoes


    def reset(self):
        for p in self.pedras:
            p.posicao='F'
            p.oculta=False
        
        self.fora  = list(self.pedras)
        rdm.shuffle(self.fora)
        
        self.pista = []
        
        self.oculta = []
        self.nao_oculta = []
        rdm.shuffle(self.nao_oculta)

        self.conhecidas = [None]*(len(self.acoes))
        
        self.posicoes_lives = [4, 4]
        self.jogador = 0
        self.acoes = ['']*len(self.acoes)


    def checa_acoes_possiveis(self) -> int:
        acoes = []
        if len(self.fora)>0:
            acoes.append(1)
        if len(self.pista) > len(self.oculta):
            acoes.append(2)
        if len(self.pista) > 1:
            acoes.append(3)
        if len(self.oculta) > 0:
            acoes.append(5)
            if self.jogador:
                acoes.append(4)
            
        
        return rdm.choice(acoes)
        
        
    def realizar_acao(self):
        self.jogador= not self.jogador
        acao = self.checa_acoes_possiveis()
        
        if acao==1: # place
            p = self.fora.pop(0)
            if len (self.posicoes_lives) > 1 :
                p.posicao = rdm.choice(self.posicoes_lives)
                if p.posicao==4:
                    self.posicoes_lives[0] -=1
                    self.posicoes_lives[1] +=1

                elif p.posicao == self.posicoes_lives[0]:
                    if self.posicoes_lives[0]>1:
                        self.posicoes_lives[0] -=1
                    else:
                        self.posicoes_lives.remove(1)
                else:
                    if self.posicoes_lives[1]<7:
                        self.posicoes_lives[1] +=1
                    else:
                        self.posicoes_lives.remove(7)
            else:
                p.posicao = self.posicoes_lives[0]
                if(self.posicoes_lives[0] < 4):
                    self.posicoes_lives[0]-=1
                else:
                    self.posicoes_lives[0]+=1
            
            
            self.pista.append(p)
            self.nao_oculta.append(p)
            
            self.acoes.pop(0)
            self.acoes.append(f'1,{p.posicao}')

            self.conhecidas.pop(0)
            self.conhecidas.append(p)
            
            
        elif acao==2: # hide
            rdm.shuffle(self.nao_oculta)
            p = self.nao_oculta.pop(0)
            p.oculta=True
            self.oculta.append(p)
            
            self.acoes.pop(0)
            self.acoes.append(f'2,{p.posicao}')

            self.conhecidas.pop(0)
            self.conhecidas.append(p)
            
        elif acao==3: # swap
            rdm.shuffle(self.pista)
            p1 = self.pista.pop(0)
            p2 = self.pista.pop(0)
            aux = p1.posicao
            p1.posicao = p2.posicao
            p2.posicao = aux
            self.pista.append(p1)
            self.pista.append(p2)

            self.acoes.pop(0)
            self.acoes.append(f'3,{p1.posicao},{p2.posicao}')

            if not p1.oculta:
                self.conhecidas.pop(0)
                self.conhecidas.append(p1)
            if not p2.oculta:
                self.conhecidas.pop(0)
                self.conhecidas.append(p2)

        elif acao==4: # peek
            p = rdm.choice(self.oculta)
            self.acoes.pop(0)
            self.acoes.append(f'4,{p.posicao}')

            self.conhecidas.pop(0)
            self.conhecidas.append(p)
            
        elif acao==5:
            p = rdm.choice(self.oculta)
            self.acoes.pop(0)
            self.acoes.append(f'5,{p.posicao}')


            if rdm.randint(0,1) == 0:
                self.conhecidas.pop(0)
                self.conhecidas.append(None)
            else:
                self.reset()
            

    def imprime_tupla(self):
        for p in self.pedras:
            if(p.oculta):
                print('?;',end='')
            else:
                print(f'{p.posicao};',end='')
        
        
        for a in self.acoes:
            print(f'{a};',end='')
        
        for p in range(6):
            if self.pedras[p].oculta:
                if self.conhecidas.count(self.pedras[p]) > 0:
                    # print(f' aq ({self.pedras[p]}) ',end='')
                    print(f'{self.pedras[p].posicao};',end='')
                else:
                    print('?;',end='')
            else:
                print(f'{self.pedras[p].posicao};',end='')
    
        if self.pedras[6].oculta:
            if self.conhecidas.count(self.pedras[6]) > 0:
                print(f'{self.pedras[6].posicao}')
            else:
                print('?')
        else:
            print(self.pedras[6].posicao)
                


def imprime_cabecalho(n):
    print('coroa;escudo;espada;bandeira;cavaleiro;martelo;balanca;',end='')
    for a in range(1,n+1):
        print(f'acao_{a};',end='')
    print('final_coroa;final_escudo;final_espada;final_bandeira;final_cavaleiro;final_martelo;final_balanca')

if __name__=='__main__':
    n = 3
    # imprime_cabecalho(n)
    pedras = [Pedra('coroa'), Pedra('escudo'), Pedra('espada'), Pedra('bandeira'), 
        Pedra('cavaleiro'), Pedra('martelo'), Pedra('balanca')]
    
    jogo = Jogo(pedras,n)
    jogo.imprime_tupla()
    
    for i in range(500):
        jogo.realizar_acao()
        jogo.imprime_tupla()