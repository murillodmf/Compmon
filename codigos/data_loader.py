import json
import os

'''
O data loader possuem funções para carregar as informações que estão nos arquivos JSON
As criaturas, os ataques e os efeitos
Ele basicamente ele navega ate o diretorio de pasta data e usa comandos da biblioteca JSON para 
receber essas informações

Se eu me lembro bem essas informações ficam em formato de dicionário quando passado pro python ( não lembro ao certo)
'''
def carregar_criaturas(filename = 'criaturas.json'):
    caminho = os.path.join(os.path.dirname(__file__), '..', 'data', filename)
    with open(caminho, 'r') as f:
        criaturas = json.load(f)
    return criaturas

def carregar_ataques(filename = 'ataques.json'):
    caminho = os.path.join(os.path.dirname(__file__), '..', 'data', filename)
    with open(caminho, 'r') as f:
        ataques = json.load(f)
    return ataques

def carregar_efeitos(filename = 'efeitos.json'):
    caminho = os.path.join(os.path.dirname(__file__), '..', 'data', filename)
    with open(caminho, 'r') as f:
        efeitos = json.load(f)
    return efeitos 



