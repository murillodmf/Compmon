# Este é o conteúdo COMPLETO e CORRETO para o seu arquivo functions.py

import sys

'''
Este módulo possui algumas funções que vão ser usadas em alguma parte do código.
'''
'''
Função escolher criaturas:
Paramêtros: dados das criaturas, basicamente o arquivo JSON inteiro de criaturas no formato de dicionário
Percorre todo o dicionário printando as criaturas possiveis para escolha
Aquele if (escolha.isdigit(), basicamente o que ele faz é não deixar o mesmo pokemon ser escolhido pelos dois adversarios)
a pessoa escolhe o pokemon e o metodo retorna o pokemon escolhido
'''
def escolher_criaturas(dados):
    pokemon = dados['criaturas']
    print("Escolha uma criatura:\n")
    for i, criatura in enumerate(pokemon, 1):
        print(f"{i}. {criatura['nome']} - {criatura['tipo']}")
    escolha = input("\nDigite o número da criatura escolhida: \n")
    if escolha.isdigit() and 0 < int(escolha) <= len(pokemon):
        escolha = int(escolha) - 1
        print(f"Criatura escolhida: {pokemon[escolha]['nome']} - {pokemon[escolha]['tipo']}\n")
        return pokemon[escolha]
    else:
        print("Escolha inválida, tente novamente.\n")
        return escolher_criaturas(dados)


'''
Parâmetros: recebe a lista de todos os ataques e o tipo da criatura

Quando implementei o jogo, deixei que as criaturas poderiam somente escolher ataques do seu tipo e do tipo normal
essa função basicamente filtra os ataques que vão ser mostrados para o usuário escolher
'''
def filtrar_ataques(ataques, tipo_criatura):
    # Combina ataques gerais com ataques do tipo específico da criatura
    ataques_filtrados = []
    if f'ataques{tipo_criatura}' in ataques:
        ataques_filtrados.extend(ataques[f'ataques{tipo_criatura}'])
    if 'ataquesgeral' in ataques:
        ataques_filtrados.extend(ataques['ataquesgeral'])
    return ataques_filtrados


'''
Essa função recebe os ataques filtrados da criatura para que o usuário possa escolher os 4 ataques
que ele poderá utilizar na batalha
'''
def escolher_ataques(self, ataques_filtrados):
    print("Escolha até 4 ataques:\n")
    for i, ataque in enumerate(ataques_filtrados, 1):
        if ataque.get('dano') == False: # Usar .get() para evitar erro se a chave não existir
            print(f"{i}. {ataque['nome']} - Efeito: {ataque['efeito']}")
        else:
            print(f"{i}. {ataque['nome']} - Dano: {ataque['dano']}")
    escolhas = []
    countAtaquesForaDoTipo = 0
    print("\n")
    while len(escolhas) < 4:
        escolha = input("Digite o número do ataque escolhido: ")
        if escolha.isdigit() and 0 < int(escolha) <= len(ataques_filtrados):
            escolha = int(escolha) - 1
            if ataques_filtrados[escolha] in escolhas:
                print("Ataque já escolhido, tente novamente.")
                continue
            if ataques_filtrados[escolha]['tipo'] != self.tipo and ataques_filtrados[escolha]['tipo'] != 'normal' and countAtaquesForaDoTipo >= 2:
                print("Você já escolheu 2 ataques fora do tipo da criatura, escolha outro ataque.")
                continue
            else:
                escolhas.append(ataques_filtrados[escolha])
                if ataques_filtrados[escolha]['tipo'] != self.tipo and ataques_filtrados[escolha]['tipo'] != 'normal':
                    countAtaquesForaDoTipo += 1
                if len(escolhas) == 4:
                    break
        else:
            print("Escolha inválida, tente novamente.")
    return escolhas

'''
Função que mostra os ataques que a criatura possui
'''

def mostrar_ataques_criatura(criatura):
    print(f'{criatura.nome} tem os seguintes ataques:')
    for i,ataque in enumerate(criatura.ataques, 1):
        if ataque.get('dano') == False:
            print(f"{i}. {ataque['nome']} - Efeito: {ataque['efeito']}")
        else:
            print(f"{i}. {ataque['nome']} - Dano: {ataque['dano']}")
    print("\n")

'''
Escolhe o ataque da criatura, dentre os 4 ja escolhidos posteriormente
usado na hora que o jogador vai atacar o adversario
'''

def escolher_ataque_da_criatura(criatura):
    print(f'Escolha o ataque para {criatura.nome}:\n')
    for i, ataque in enumerate(criatura.ataques, 1):
        if ataque.get('dano') == False:
            print(f"{i}. {ataque['nome']} - Efeito: {ataque['efeito']}")
        else:
            print(f"{i}. {ataque['nome']} - Dano: {ataque['dano']}")
    escolha = input("\nDigite o número do ataque escolhido: ")
    if escolha.isdigit() and 0 < int(escolha) <= len(criatura.ataques):
        escolha = int(escolha) - 1
        print(f"Ataque escolhido: {criatura.ataques[escolha]['nome']}\n")
        return criatura.ataques[escolha]
    else:
        print("Escolha inválida, tente novamente.\n")
        return escolher_ataque_da_criatura(criatura)


'''
Um if-else gigante para calcular a vantagem de um tipo sobre o outro
A função foi modificada para aceitar tanto um objeto 'defensor' quanto uma string com o tipo do defensor.
'''
def vantagens(ataque, defensor):
    tipo_ataque = ataque.tipo

    if isinstance(defensor, str):
        tipo_defensor = defensor
    else:
        tipo_defensor = defensor.tipo

    if tipo_ataque == 'fogo' and tipo_defensor == 'planta':
        return 2
    elif tipo_ataque == 'fogo' and tipo_defensor == 'agua':
        return 0.5
    elif tipo_ataque == 'fogo' and tipo_defensor == 'fogo':
        return 0.5
    elif tipo_ataque == 'fogo' and tipo_defensor == 'gelo':
        return 2
    elif tipo_ataque == 'fogo' and tipo_defensor == 'areia':
        return 0.5
    elif tipo_ataque == 'agua' and tipo_defensor == 'fogo':
        return 2
    elif tipo_ataque == 'agua' and tipo_defensor == 'areia':
        return 2
    elif tipo_ataque == 'agua' and tipo_defensor == 'agua':
        return 0.5
    elif tipo_ataque == 'agua' and tipo_defensor == 'planta':
        return 0.5
    elif tipo_ataque == 'agua' and tipo_defensor == 'eletrico':
        return 0.5
    elif tipo_ataque == 'planta' and tipo_defensor == 'agua':
        return 2
    elif tipo_ataque == 'planta' and tipo_defensor == 'areia':
        return 2
    elif tipo_ataque == 'planta' and tipo_defensor == 'fogo':
        return 0.5
    elif tipo_ataque == 'planta' and tipo_defensor == 'planta':
        return 0.5
    elif tipo_ataque == 'planta' and tipo_defensor == 'gelo':
        return 0.5
    elif tipo_ataque == 'lutador' and tipo_defensor == 'normal':
        return 2
    elif tipo_ataque == 'lutador' and tipo_defensor == 'gelo':
        return 2
    elif tipo_ataque == 'lutador' and tipo_defensor == 'sombrio':
        return 2
    elif tipo_ataque == 'lutador' and tipo_defensor == 'psiquico':
        return 0.5
    elif tipo_ataque == 'lutador' and tipo_defensor == 'lutador':
        return 0.5
    elif tipo_ataque == 'sombrio' and tipo_defensor == 'psiquico':
        return 2
    elif tipo_ataque == 'sombrio' and tipo_defensor == 'eletrico':
        return 2
    elif tipo_ataque == 'sombrio' and tipo_defensor == 'lutador':
        return 0.5
    elif tipo_ataque == 'sombrio' and tipo_defensor == 'sombrio':
        return 0.5
    elif tipo_ataque == 'psiquico' and tipo_defensor == 'lutador':
        return 2
    elif tipo_ataque == 'psiquico' and tipo_defensor == 'areia':
        return 2
    elif tipo_ataque == 'psiquico' and tipo_defensor == 'sombrio':
        return 0.5
    elif tipo_ataque == 'psiquico' and tipo_defensor == 'psiquico':
        return 0.5
    elif tipo_ataque == 'areia' and tipo_defensor == 'eletrico':
        return 2
    elif tipo_ataque == 'areia' and tipo_defensor == 'fogo':
        return 2
    elif tipo_ataque == 'areia' and tipo_defensor == 'psiquico':
        return 0.5
    elif tipo_ataque == 'areia' and tipo_defensor == 'areia':
        return 0.5
    elif tipo_ataque == 'areia' and tipo_defensor == 'planta':
        return 0.5
    elif tipo_ataque == 'areia' and tipo_defensor == 'agua':
        return 0.5
    elif tipo_ataque == 'eletrico' and tipo_defensor == 'agua':
        return 2
    elif tipo_ataque == 'eletrico' and tipo_defensor == 'gelo':
        return 2
    elif tipo_ataque == 'eletrico' and tipo_defensor == 'sombrio':
        return 0.5
    elif tipo_ataque == 'eletrico' and tipo_defensor == 'eletrico':
        return 0.5
    elif tipo_ataque == 'eletrico' and tipo_defensor == 'areia':
        return 0.5
    elif tipo_ataque == 'gelo' and tipo_defensor == 'planta':
        return 2
    elif tipo_ataque == 'gelo' and tipo_defensor == 'areia':
        return 2
    elif tipo_ataque == 'gelo' and tipo_defensor == 'gelo':
        return 0.5
    elif tipo_ataque == 'gelo' and tipo_defensor == 'fogo':
        return 0.5
    elif tipo_ataque == 'gelo' and tipo_defensor == 'lutador':
        return 0.5
    elif tipo_ataque == 'gelo' and tipo_defensor == 'eletrico':
        return 0.5
    elif tipo_ataque == 'normal' and tipo_defensor == 'normal':
        return 1.5
    else:
        return 1
    
'''
Menu do jogo
'''
def menu():
    print("Escolha uma opção:\n")
    print("1. Iniciar jogo")
    print("2. Sair\n")
    escolha = input()
    if escolha == '1':
        return 'jogo'
    elif escolha == '2':
        return 'sair'
    else:
        print("Escolha inválida, tente novamente.\n")
        return menu()