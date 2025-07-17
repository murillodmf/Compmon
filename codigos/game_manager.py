import functions
from data_loader import carregar_criaturas, carregar_ataques, carregar_efeitos
import random
from batalha import batalha
from criatura import criatura
from ataque import ataque
from efeitos import efeitos
import pygame
from pygame.locals import *

'''
Classe responsavel pela leitura de dados para o jogo dos ataques e criaturas e para seta-las antes da batalha

'''

class GameManager:
    def __init__(self, screen):
        self.dados_criaturas = carregar_criaturas() # Pega os dados das criaturas do arquivo JSON
        self.dados_ataques = carregar_ataques() # Pega os dados dos ataques do arquivo JSON
        
    '''
    Método configurar criatura
    Cria uma criatura, pede para o usuario escolher ela
    e os ataques da criatura, e retorna a criatura
    '''

    def configurar_criatura(self):
        criatura = functions.escolher_criaturas(self.dados_criaturas)
        ataques_filtrados = functions.filtrar_ataques(self.dados_ataques, criatura['tipo'])
        criatura['ataques'] = functions.escolher_ataques(self, ataques_filtrados) # Passando o self para pegar o tipo do pokemon
        return criatura

    '''
    Método onde o jogo começa
    Configura as criaturas e instacia a classe criatura para poder usar seus métodos
    Inicializa as criaturas e a batalha
    '''

    def Iniciar_jogo(self):
        print('Bem-vindo ao jogo Pokemon!')
        print("Escolha a primeira criatura e seus ataques:")
        criatura1 = self.configurar_criatura()
        criatura1 = criatura(criatura1['nome'], criatura1['tipo'], criatura1['hp'],criatura1['atk'], criatura1['def'], criatura1['spe'], criatura1['ataques'])
        
        print("Escolha a segunda criatura e seus ataques:")
        criatura2 = self.configurar_criatura()
        criatura2 = criatura(criatura2['nome'], criatura2['tipo'], criatura2['hp'],criatura2['atk'], criatura2['def'], criatura2['spe'], criatura2['ataques'])
        
        battle = batalha(criatura1, criatura2)
        battle.iniciar_batalha()