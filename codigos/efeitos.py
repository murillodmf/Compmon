import random
from data_loader import carregar_efeitos

'''
Classe efeitos: Classe responsável por administrar os efeitos, o que eles vão fazer, e adicionalos nas criaturas
Atributos:
- Os dados dos arquivos JSON de feitos
- dicionario vazio que vai receber efeitos que eventualmente ficarem ativos


Muitas da comparações dessa classe tem a ver com o modo que eu escrevi no arquivo JSON.
'''

class efeitos:
    def __init__(self):
        self.dadosefeitos = carregar_efeitos()
        self.efeitosativos = {}


    '''
    Metodo effects ( metodo chamado toda vez que o ataque selecionado é um efeito)

    If1  Calcula se o efeito vai ser acertado (chance de 70%)
    Procura o index do efeito no dicionario que esta todos os efeitos
    Pega o efeito aplicado no dicionario dados efeitos
    Pega o tipo do efeito 
    Em seguida ele chama o metodo responsavel por aquele efeito, a funcao getattr
    junta o efeito_ com o tipo correspondente e armazena em x

    Os outros ifs so verificam que tipo que é o efeito, aplicam o efeito no jogador correto
    ( adiciona o efeito nos efeitos ativos da criatura) 
    e chamam a função para executar o efeito

    Alguns efeitos são aplicados no proprio jogador que utilizou o ataque
    outros no adversario, outros nos dois, por isso é feito essa verificação

    '''
    def effects(self, ataque, jogador, adversario):
        if ataque.efeito and self.calcular_acerto_efeito():
            index = self.procurar_indice_efeitos(ataque.efeito)
            efeito_info = self.dadosefeitos[index]
            tipo_efeito = efeito_info['tipo']
            x = getattr(self, f"efeito_{tipo_efeito}")

            if tipo_efeito in ['dano', 'disabled', 'stunned']:
                self.adicionar_efeitos_jogador(efeito_info, adversario)
                x(index, adversario, jogador)
            elif tipo_efeito in ['health', 'buff', 'status']:
                self.adicionar_efeitos_jogador(efeito_info, jogador)
                x(index, jogador, adversario)
            elif tipo_efeito == 'perdeturno':
                self.adicionar_efeitos_jogador(efeito_info, jogador)
                x(index, jogador, adversario)
            elif tipo_efeito == 'life':
                self.adicionar_efeitos_jogador(efeito_info, jogador)
                self.adicionar_efeitos_jogador(efeito_info, adversario)
                x(index, jogador, adversario)
            
        else:
            pass
    
    '''
    Metodo atualizar_feitos_jogador

    Atualiza o numero de turnos que o efeito ficara ativo
    Se o numero for menor que (turnos) 0 remove os efeitos
    '''
    def atualizar_efeitos_jogador(self, jogador):
        efeitos_a_remover = []
        for nome_efeito, dados_efeito in jogador.efeitosativos.efeitosativos.items():
            dados_efeito['turnos'] -= 1
            if dados_efeito['turnos'] <= 0:
               efeitos_a_remover.append(nome_efeito)
        for nome_efeito in efeitos_a_remover:
            del jogador.efeitosativos.efeitosativos[nome_efeito]

    '''
    adicionar_efeitos_jogador

    
    adiciona os efeitos no dicionario do jogador(objeto efeitos ativos do jogador)
    '''
    def checar_se_sleep(self, jogador, adversario):
        index = self.procurar_indice_efeitos('sleep')
        for efeito in jogador.efeitosativos.efeitosativos.values():
            if efeito['tipo'] == 'sleep' and efeito['turnos'] > 0:
                print(f"{jogador.nome} está dormindo!")
                return True
        return False

    def checar_se_freeze(self, jogador, adversario):
        index = self.procurar_indice_efeitos('freeze')
        for efeito in jogador.efeitosativos.efeitosativos.values():
            if efeito['tipo'] == 'freeze' and efeito['turnos'] > 0:
                if self.efeito_freeze(index, jogador, adversario):
                    return True
                else:
                    return False



    def adicionar_efeitos_jogador(self,efeito, jogador):
        jogador.efeitosativos.efeitosativos[efeito['nome']] = {
            'turnos': efeito['turnos'],
            'tipo': efeito['tipo'],
            'dano': efeito['dano'],
        }


    '''
    Método que checa se o pokemon esta stunnado
    Ele percorre o dicionario de efeitos ativos do jogador procurando um efeito stunned
    '''
    def checar_se_stunned(self, jogador, adversario):
        index = self.procurar_indice_efeitos('stunned')
        for efeito in jogador.efeitosativos.efeitosativos.values():
            if efeito['tipo'] == 'stunned' and efeito['turnos'] > 0:
                if self.efeito_stunned(index, jogador, adversario):
                    return True
                else:
                    return False
    
    '''
    Método que checa se o pokemon esta desabilitado
    Ele percorre o dicionario de efeitos ativos do jogador procurando um efeito disabled
    '''
    def checar_se_disabled(self, jogador, adversario):
        index = self.procurar_indice_efeitos('disabled')
        for efeito in jogador.efeitosativos.efeitosativos.values():
            if efeito['tipo'] == 'disabled' and efeito['turnos'] > 0:
                self.efeito_disabled(index, jogador, adversario)
                return True
        return False

    '''
    Aplica os efeitos ativos do jogador
    é chamado em cada turno de batalha
    '''
    def aplicar_efeitos_ativos_jogador(self, jogador, adversario):
        for efeito in jogador.efeitosativos.efeitosativos.keys():
            index = self.procurar_indice_efeitos(efeito)
            x = getattr(self, f"efeito_{self.dadosefeitos[index]['tipo']}")
            x(index, jogador, adversario)

    '''
    recebe dano, se tiver efeito ativo de dano
    '''

    def efeito_dano(self,index, jogador, adversario):
        jogador.receber_dano(self.dadosefeitos[index]['dano'])
    
    '''
    efeito disabled, o adversario fica atordoado
    '''
    def efeito_disabled(self,index, jogador, adversario):
        print(f"{jogador.nome} está atordoado!")

    '''
    efeito perde turno, o jogador passa o turno para o adversario
    '''

    def efeito_perdeturno(self,index, jogador, adversario):
        print(f"{jogador.nome} perdeu o turno!")


    '''
    o jogador recupera sua vida, baseado em calculos com a sua vida
    '''
    def efeito_health(self,index, jogador, adversario):
        fator = (jogador.hp / 100) * 25
        if jogador.hp + fator > jogador.hpmax:
            jogador.hp = jogador.hpmax
            print(f"{jogador.nome} esta de vida cheia!")
        else:
            jogador.hp += fator
            print(f"{jogador.nome} recuperou {fator} de vida!")

    '''
    o jogador rouba a vida do adversário
    '''

    def efeito_life(self,index, jogador, adversario):
        fator = (adversario.hp / 100) * 25
        if jogador.hp == jogador.hpmax:
            jogador.hp = jogador.hpmax
            print(f"{jogador.nome} esta de vida cheia!")
        elif jogador.hp + fator > jogador.hpmax:
            jogador.hp = jogador.hpmax
            adversario.hp = adversario.hp - (jogador.hp + fator - 200)
            print(f"{jogador.nome} roubou {jogador.hp + fator - 200} de vida!")
        else:
            jogador.hp += fator
            adversario.hp -= fator
            print(f"{jogador.nome} roubou {fator} de vida!")

    '''
    efeitos de status( velocidade, atk, def, speed)
    '''
    def efeito_status(self,index, jogador, adversario):
        if self.dadosefeitos[index]['nome'] == 'slow':
            adversario.velocidade -= 5
            print(f"{adversario.nome} está mais lento!")
        elif self.dadosefeitos[index]['nome'] == 'atk':
            jogador.atk += 5
            print(f"{jogador.nome} está mais forte!")
        elif self.dadosefeitos[index]['nome'] == 'def':
            adversario.defesa -= 5
            print(f"{adversario.nome} está mais fraco!")
        elif self.dadosefeitos[index]['nome'] == 'spe':
            jogador.velocidade += 5
            print(f"{jogador.nome} está mais rápido!")
        elif self.dadosefeitos[index]['nome'] in ['poison', 'burn']:
            jogador.hp -= 10
            print(f"{jogador.nome} perdeu 10 pontos de {self.dadosefeitos[index]['nome']}!")
        elif self.dadosefeitos[index]['nome'] == 'sleep':	# mecanica sleep q eu entendi, não é possível acordar até o final dos turnos
            print(f"{jogador.nome} está dormindo!")

    '''
    calculo para ver se o jogador vai ficar atordoado
    '''
    def efeito_stunned(self,index, jogador,adversario):
        x = random.randint(0, 100)
        if x <= 80:
            print(f"{jogador.nome} está confuso!")
            return True
        else:
            return False

    '''
    Método: Procurar indice efeitos

    Ele procura no dicionário, dados efeitos, o índice do efeito que está sendo abordado no turno da batalha
    '''

    def efeito_freeze(self,index, jogador, adversario): # mecanica freeze: a cada turno do freeze, o jogador tem 20% de chance de se descongelar
            x = random.randint(0, 100) 
            if x <= 80:
                print(f"{jogador.nome} está congelado!")
                return True
            else:
                self.efeitos_a_remover.append(self.dadosefeitos[index]['nome'])
                return False


    def procurar_indice_efeitos(self, efeito):
        for i, efei in enumerate(self.dadosefeitos):
            if efei['nome'] == efeito:
                return i
    
    '''
    Calcula se o efeito vai acertar ou não(70%)
    '''
    def calcular_acerto_efeito(self):
        x = random.randint(0, 100)
        if x <= 30:
            print("O ataque falhou!")
            return False
        else:
            return True
        