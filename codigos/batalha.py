import pygame
from pygame.locals import *
import time
from efeitos import efeitos
import functions
import random

class batalha:
    def __init__(self, jogador, adversario, background, screen):
        self.jogador = jogador
        self.adversario = adversario
        self.turno = 0
        self.gestor_efeitos = efeitos()
        self.background = background
        self.screen = screen

        # Carregar as imagens necessárias
        self.fundovidaesq = pygame.image.load("images/battle/fundobarradevida.png")
        self.fundovidadir = self.flipimage(self.fundovidaesq)
        self.player1vida = pygame.image.load("images/battle/barradevida.png")
        self.player2vida = pygame.image.load("images/battle/barradevida.png")
        self.button = pygame.image.load("images/battle/button.png")
        self.buttonover = pygame.image.load("images/battle/buttonover.png")
        self.buttonNewGame = pygame.image.load("images/battle/buttonover.png")
        self.fundobuttonattack = pygame.image.load("images/battle/fundoselecionaratak.png")
        self.masterball = pygame.image.load("images/battle/masterball.png")
        self.pointer = pygame.image.load("images/util/pointer.png")
        self.pointer_grabbed = pygame.image.load("images/util/pointer_grabbed.png")
        self.player1image = pygame.image.load(self.jogador.image_path)
        self.player2image = pygame.image.load(self.adversario.image_path)
        self.player1iconetipo = self.load_tipo_png(self.jogador.tipo)
        self.player2iconetipo = self.load_tipo_png(self.adversario.tipo)
        self.localefeitos = pygame.image.load("images/battle/fundoefeitosnovo.png")
        self.triangulovezpoke = pygame.image.load("images/battle/triangulovezdopoke.png")
        
        # Carregando os efeitos (freeze, burn, etc.)
        self.effects_images = self.load_effect_images()

        # Definir a largura e altura do fundo do botão de ataque
        self.fundo_width = 800
        self.fundo_height = 250

    def flipimage(self, image):
        return pygame.transform.flip(image, True, False)
    
    def load_tipo_png(self, tipo):
        return pygame.image.load(f"images/battle/icons_types/{tipo}.png")
    
    def resize_image(self, image, width, height):
        return pygame.transform.scale(image, (width, height))

    def load_effect_images(self):
        # Define o tamanho desejado para as imagens dos efeitos
        largura = 120  # Largura desejada
        altura = 30   # Altura desejada

        effects = {
            "freeze": pygame.transform.scale(pygame.image.load("images/efeitos/freeze.png"), (largura, altura)),
            "burn": pygame.transform.scale(pygame.image.load("images/efeitos/burn.png"), (largura, altura)),
            "paralyzes": pygame.transform.scale(pygame.image.load("images/efeitos/paralysis.png"), (largura, altura)),
            "poison": pygame.transform.scale(pygame.image.load("images/efeitos/poison.png"), (largura, altura)),
            "sleep": pygame.transform.scale(pygame.image.load("images/efeitos/sleep.png"), (largura, altura)),
            "confusion": pygame.transform.scale(pygame.image.load("images/efeitos/confusion.png"), (largura, altura)),
        }
        return effects

    def desenhar_barras_de_vida(self):
        """Desenha as barras de vida atualizadas na tela para ambos os jogadores."""
        largura_total = 300  # Largura total fixa da barra de vida
        altura_barra = 30    # Altura fixa da barra de vida

        # Posicionamento das barras na tela
        posicao_vertical = 80  # Posição vertical das barras (mais para baixo)
        x_jogador = 200         # Posição horizontal da barra do jogador (mais para a direita)
        x_adversario = self.screen.get_width() - largura_total - 200  # Posição horizontal da barra do adversário

        self.screen.blit(self.fundovidaesq, (0, 0))
        self.screen.blit(self.fundovidadir, (self.screen.get_width() - self.fundovidadir.get_width(), 0))

        # Configurando a posição do localefeitos após fundovidaesq
        localefeitos = pygame.transform.rotate(self.localefeitos, 180)
        localefeitos_x = self.fundovidaesq.get_width() - 25  # Coloca localefeitos logo após fundovidaesq
        localefeitos_y = - (localefeitos.get_height() // 2) + 51  # Ajusta para alinhar o topo corretamente

        # Configurando a posição do localefeitos2 após fundovidadir
        localefeitos2 = self.flipimage(localefeitos)
        localefeitos2_x = self.screen.get_width() - self.fundovidadir.get_width() - localefeitos2.get_width() + 25 # Coloca localefeitos2 logo antes de fundovidadir
        localefeitos2_y = - (localefeitos2.get_height() // 2) + 51  # Ajusta para alinhar o topo corretamente

        # Desenhar os elementos localefeitos
        self.screen.blit(localefeitos, (localefeitos_x, localefeitos_y))
        self.screen.blit(localefeitos2, (localefeitos2_x, localefeitos2_y))

        # Calcula a largura atual da barra de vida do jogador (esquerda)
        largura_atual_jogador = max(0, int(largura_total * (self.jogador.hp / self.jogador.hpmax)))

        # Calcula a largura atual da barra de vida do adversário (direita)
        largura_atual_adversario = max(0, int(largura_total * (self.adversario.hp / self.adversario.hpmax)))

        # Desenhar o fundo das barras de vida (em preto)
        pygame.draw.rect(self.screen, (0, 0, 0), (x_jogador, posicao_vertical, largura_total, altura_barra))
        pygame.draw.rect(self.screen, (0, 0, 0), (x_adversario, posicao_vertical, largura_total, altura_barra))

        # Desenhar a parte perdida da barra de vida (em vermelho)
        pygame.draw.rect(self.screen, (255, 0, 0), (x_jogador + largura_atual_jogador, posicao_vertical, largura_total - largura_atual_jogador, altura_barra))
        pygame.draw.rect(self.screen, (255, 0, 0), (x_adversario, posicao_vertical, largura_total - largura_atual_adversario, altura_barra))

        # Desenhar a parte restante da barra de vida (em verde)
        pygame.draw.rect(self.screen, (0, 255, 0), (x_jogador, posicao_vertical, largura_atual_jogador, altura_barra))
        pygame.draw.rect(self.screen, (0, 255, 0), (x_adversario + (largura_total - largura_atual_adversario), posicao_vertical, largura_atual_adversario, altura_barra))


    def desenhar_triangulovezpoke(self, image, pos_x, pos_y):
        # Calcula a posição horizontal do triangulo
        triangulo_x = pos_x + 135  # Ajusta para o centro do Pokémon
        # Desenha o triangulo um pouco acima da imagem do Pokémon
        self.screen.blit(image, (triangulo_x, pos_y - image.get_height() - 10))

    def apply_red_tint(self, image):
        # Cria uma cópia da imagem original para preservar os dados
        red_tinted_image = image.copy()

        # Aplica um filtro vermelho (RGB) à imagem
        red_tinted_image.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)

        return red_tinted_image

    def load_attack_frames(self, attack_type):
        frames = []
        for i in range(6):  # Supondo que você tenha 6 frames para cada tipo de ataque
            frame = pygame.image.load(f'images/battle/gifsframes/{attack_type}/frame_0{i}.png')
            frames.append(frame)
        return frames
    
    def animate_attack(self, attack_type):
        attack_choice = random.choice(['single', 'rain'])

        if attack_choice == 'single':
            self.animate_single_fireball(attack_type)
        else:
            self.animate_fire_rain(attack_type)


    def animate_fire_rain(self, attack_type):
        frames = self.load_attack_frames(attack_type)  # Carrega os frames da animação de ataque
        num_frames = len(frames)
        descent_speed = 100  # Velocidade de descida das bolas de fogo (ajuste para descer mais rápido ou mais devagar)

        if self.turno % 2 == 0:
            # Define a posição do defensor à direita da tela
            defender_pos = (self.screen.get_width() - 700 + 175, self.screen.get_height() // 2 - 50)
        else:
            # Define a posição do defensor à esquerda da tela
            defender_pos = (300 + 175, self.screen.get_height() // 2 - 50)

        # Lista para rastrear as posições atuais de cada bola de fogo
        fireballs = []

        # Inicializa as bolas de fogo com posições iniciais aleatórias acima da tela
        for _ in range(5):  # Número de bolas de fogo na chuva (ajuste este valor para mais ou menos bolas)
            frame_index = 0
            frame = frames[frame_index]
            rotated_frame = pygame.transform.rotate(frame, -90)  # Rotaciona o frame para que fique virado para baixo

            # Posiciona as bolas de fogo aleatoriamente em x, perto do defensor, e bem acima da tela em y
            start_x = random.randint(defender_pos[0] - 150, defender_pos[0] + 50)  # Controle a dispersão em x ajustando o valor de 100
            start_y = random.randint(-300, -100)  # Controle a posição inicial em y (acima da tela)

            # Adiciona a bola de fogo à lista com sua posição inicial e índice do frame
            fireballs.append({
                'x': start_x,
                'y': start_y,
                'frame_index': frame_index
            })

        animation_running = True
        while animation_running:
            # Redesenha o fundo e os elementos estáticos da tela
            self.screen.blit(self.background, (0, 0))
            self.desenhar_barras_de_vida()  # Desenha as barras de vida
            self.desenhar_barras_e_criaturas()  # Desenha as criaturas

            animation_running = False  # Assume que a animação terminou, a menos que uma bola ainda esteja descendo

            for fireball in fireballs:
                fireball['y'] += descent_speed  # Atualiza a posição em y da bola de fogo (controle o quanto ela desce)

                # Verifica se a bola de fogo ainda não atingiu o defensor
                if fireball['y'] + rotated_frame.get_height() < defender_pos[1] + 100:
                    animation_running = True  # Continua a animação se alguma bola ainda não atingiu o alvo

                # Atualiza o frame da bola de fogo para criar a animação
                fireball['frame_index'] = (fireball['frame_index'] + 1) % num_frames
                frame = frames[fireball['frame_index']]
                rotated_frame = pygame.transform.rotate(frame, -90)  # Rotaciona novamente para garantir que esteja virado para baixo

                # Desenha a bola de fogo na posição atualizada
                self.screen.blit(rotated_frame, (fireball['x'], fireball['y']))

            pygame.display.update()  # Atualiza a tela inteira após apagar e redesenhar
            pygame.time.delay(50)  # Delay entre cada frame para controlar a velocidade da animação

        self.apply_damage_effect()  # Aplica o efeito de dano ao final da animação


    def animate_single_fireball(self, attack_type):
        frames = self.load_attack_frames(attack_type)
        num_frames = len(frames)

        if self.turno % 2 == 0:
            # O atacante é o jogador (esquerda), o defensor está à direita
            attacker_pos = (300, self.screen.get_height() // 2 - 50)
            defender_pos = (self.screen.get_width() - 700 + 175, self.screen.get_height() // 2 - 50)
            flipped = False
        else:
            # O atacante é o adversário (direita), o defensor está à esquerda
            attacker_pos = (self.screen.get_width() - 700, self.screen.get_height() // 2 - 50)
            defender_pos = (300 + 175, self.screen.get_height() // 2 - 50)
            flipped = True

        # Calcular a velocidade do ataque
        dx = (defender_pos[0] - attacker_pos[0]) / num_frames
        dy = (defender_pos[1] - attacker_pos[1]) / num_frames

        for i in range(num_frames):
            # Redesenha o fundo e os elementos estáticos da tela
            self.screen.blit(self.background, (0, 0))
            self.desenhar_barras_de_vida()
            self.desenhar_barras_e_criaturas()

            frame = frames[i]
            if flipped:
                frame = pygame.transform.flip(frame, True, False)

            # Ajuste para mover a bola um pouco mais em x se o ataque vier da direita
            frame_pos_x = attacker_pos[0] + i * dx
            if flipped:
                frame_pos_x -= 100  # Ajuste fino para mover a bola mais para a esquerda

            frame_pos = (frame_pos_x, attacker_pos[1] + i * dy)
            self.screen.blit(frame, frame_pos)
            
            pygame.display.update()  # Atualiza a tela inteira após apagar e redesenhar
            pygame.time.delay(50)  # Reduzido para acelerar a animação

        self.apply_damage_effect()


    def apply_damage_effect(self):
        if self.turno % 2 == 0:
            # O atacante é o jogador, então o defensor está à direita
            defender_image = self.player2image
            defender_pos = (self.screen.get_width() - 700, self.screen.get_height() // 2 - 50)

            # Verifica se a imagem precisa ser invertida
            if self.adversario.nome in ("Camarujo", "Codark", "Galouvor", "Ilusiopato", "Pokemolden"):
                defender_image = self.flipimage(defender_image)
        else:
            # O atacante é o adversário, então o defensor está à esquerda
            defender_image = self.player1image
            defender_pos = (300, self.screen.get_height() // 2 - 50)

            # Verifica se a imagem precisa ser invertida
            if self.jogador.nome not in ("Camarujo", "Codark", "Galouvor", "Ilusiopato", "Pokemolden"):
                defender_image = self.flipimage(defender_image)

        # Redimensiona a imagem para 350x350
        defender_image = pygame.transform.scale(defender_image, (350, 350))

        # Cria uma cópia da imagem original e aplica o efeito vermelho
        red_tinted_image = defender_image.copy()
        red_tinted_image.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)

        # Desenha a imagem tingida de vermelho na mesma posição
        self.screen.blit(red_tinted_image, defender_pos)
        pygame.display.update([defender_pos[0], defender_pos[1], red_tinted_image.get_width(), red_tinted_image.get_height()])  # Atualiza apenas a área da imagem tingida
        pygame.time.delay(100)  # Reduzido para acelerar o efeito

        # Redesenha a imagem original para remover o efeito após o tempo
        self.screen.blit(defender_image, defender_pos)
        pygame.display.update([defender_pos[0], defender_pos[1], defender_image.get_width(), defender_image.get_height()])  # Atualiza apenas a área da imagem original


    def desenhar_barras_e_criaturas(self):
        # Ajustando o posicionamento das miniaturas dos Pokémon
        player1image = pygame.transform.scale(self.player1image, (110, 110))
        player2image = pygame.transform.scale(self.player2image, (110, 110))

        if self.jogador.nome not in ("Camarujo", "Codark", "Galouvor", "Ilusiopato", "Pokemolden"):
            player1image = self.flipimage(player1image)
        if self.adversario.nome in ("Camarujo", "Codark", "Galouvor", "Ilusiopato", "Pokemolden"):
            player2image = self.flipimage(player2image)

        # Desenhando as miniaturas nas bordas de vida
        self.screen.blit(player1image, (15, 0))  # Ajuste para a esquerda dentro da moldura
        self.screen.blit(player2image, (self.screen.get_width() - 130, 0))  # Ajuste para a direita dentro da moldura

        compmonlogo = pygame.image.load("images/background/compmonlogo.png")
        compmonlogo = pygame.transform.scale(compmonlogo, (400, 300))
        self.screen.blit(compmonlogo, (762, -90))
        # Desenhando o tipo do Pokémon e o nome, acima da barra de vida
        self.screen.blit(self.player1iconetipo, (self.fundovidaesq.get_width() // 2 - 70, 12))  # Ícone do tipo acima da barra de vida esquerda
        self.screen.blit(self.player2iconetipo, (self.screen.get_width() - 237, 12))  # Ícone do tipo acima da barra de vida direita

        # Exemplo de como desenhar o nome do Pokémon acima da barra de vida
        font = pygame.font.Font(None, 35)  # Usando uma fonte padrão
        nome1 = font.render(self.jogador.nome, True, (255, 255, 255))  # Nome em branco
        nome2 = font.render(self.adversario.nome, True, (255, 255, 255))

        # Nome do jogador 1 acima da barra de vida esquerda
        self.screen.blit(nome1, (self.fundovidaesq.get_width() // 2 - 15, 25))

        # Calculando a posição do nome do jogador 2 para ficar à esquerda do ícone do tipo
        nome2_x = self.screen.get_width() - 237 - nome2.get_width() - 10  # Subtraindo a largura do nome e adicionando espaço
        self.screen.blit(nome2, (nome2_x, 25))  # Nome do jogador 2 acima da barra de vida direita

        # Desenhando o triângulo "vezpoke" sobre o Pokémon que está atacando
        triangulo = pygame.transform.scale(self.triangulovezpoke, (50, 50))
        if self.turno % 2 == 0:
            self.desenhar_triangulovezpoke(triangulo, 300, self.screen.get_height() // 2 - 50)
        else:
            self.desenhar_triangulovezpoke(triangulo, self.screen.get_width() - 700, self.screen.get_height() // 2 - 50)

        # Desenhando as criaturas maiores no campo de batalha
        player1image = pygame.transform.scale(self.player1image, (350, 350))
        player2image = pygame.transform.scale(self.player2image, (350, 350))

        if self.jogador.nome not in ("Camarujo", "Codark", "Galouvor", "Ilusiopato", "Pokemolden"):
            player1image = self.flipimage(player1image)
        if self.adversario.nome in ("Camarujo", "Codark", "Galouvor", "Ilusiopato", "Pokemolden"):
            player2image = self.flipimage(player2image)

        self.screen.blit(player2image, (self.screen.get_width() - 700, self.screen.get_height() // 2 - 50))
        self.screen.blit(player1image, (300, self.screen.get_height() // 2 - 50))

        # Desenhar ícones de efeitos após criaturas
        self.desenhar_efeitos()

    def desenhar_efeitos(self):
        # Dimensões dos ícones dos efeitos
        largura_img = 130
        altura_img = 50

        # Posição inicial do primeiro efeito
        inicio_x_jogador = 520
        inicio_y_jogador = 10
        inicio_x_adversario = self.screen.get_width() - self.fundovidadir.get_width() - 250
        inicio_y_adversario = 10

        # Contadores para a posição na grade 2x2
        posicao_jogador = 0
        posicao_adversario = 0

        # Função auxiliar para calcular a posição do efeito
        def calcular_posicao(posicao, inicio_x, inicio_y, jogador):
            coluna = posicao % 2
            linha = posicao // 2
            return (inicio_x + coluna * largura_img, inicio_y + linha * altura_img)

        for efeito in self.jogador.efeitosativos.efeitosativos:
            if efeito in ["freeze", "burn", "paralyzes", "poison", "sleep", "confusion"]:
                x_y_jogador = calcular_posicao(posicao_jogador, inicio_x_jogador, inicio_y_jogador, True)
                self.screen.blit(self.effects_images[efeito], x_y_jogador)
                posicao_jogador += 1

        # Desenha os efeitos do adversário
        for efeito in self.adversario.efeitosativos.efeitosativos:
            if efeito in ["freeze", "burn", "paralyzes", "poison", "sleep", "confusion"]:
                x_y_adversario = calcular_posicao(posicao_adversario, inicio_x_adversario, inicio_y_adversario, False)
                self.screen.blit(self.effects_images[efeito], x_y_adversario)
                posicao_adversario += 1

    def desenhar_botao_ataque(self, ataques, mouse_pos, mouse_clicked):
        # Aumentando o fundo dos botões de ataque para criar sobra dos lados
        fundo = pygame.transform.scale(self.fundobuttonattack, (self.fundo_width, self.fundo_height))
        self.screen.blit(fundo, (self.screen.get_width() // 2 - self.fundo_width // 2, self.screen.get_height() - self.fundo_height))

        # Reduzindo o tamanho dos botões para caberem confortavelmente com sobra
        botao_largura, botao_altura = int(self.button.get_width() * 0.8), int(self.button.get_height() * 0.8)
        botao_largura, botao_altura = int(self.button.get_width() * 0.8), int(self.button.get_height() * 0.8)
        button = pygame.transform.scale(self.button, (botao_largura, botao_altura))
        buttonover = pygame.transform.scale(self.buttonover, (botao_largura, botao_altura))

        # Posições dos botões ao redor da masterball
        posicoes = [
            (self.screen.get_width() // 2 - botao_largura - 30, self.screen.get_height() - self.fundo_height + self.fundo_height // 2 - botao_altura - 20),
            (self.screen.get_width() // 2 + 30, self.screen.get_height() - self.fundo_height + self.fundo_height // 2 - botao_altura - 20),
            (self.screen.get_width() // 2 - botao_largura - 30, self.screen.get_height() - self.fundo_height + self.fundo_height // 2 + 20),
            (self.screen.get_width() // 2 + 30, self.screen.get_height() - self.fundo_height + self.fundo_height // 2 + 20)
        ]

        # Desenhando a masterball no centro do fundo
        self.screen.blit(self.masterball, (
            self.screen.get_width() // 2 - self.masterball.get_width() // 2,
            self.screen.get_height() - self.fundo_height + self.fundo_height // 2 - self.masterball.get_height() // 2
        ))

        # Desenhando os botões de ataque e seus textos
        font = pygame.font.Font(None, 20)  # Fonte para os nomes dos ataques
        for i, ataque in enumerate(ataques):
            pos_x, pos_y = posicoes[i]
            rect = pygame.Rect(pos_x, pos_y, botao_largura, botao_altura)

            # Checando se o mouse está sobre o botão
            if rect.collidepoint(mouse_pos):
                self.screen.blit(buttonover, (pos_x, pos_y))
            else:
                self.screen.blit(button, (pos_x, pos_y))

            # Desenhar o nome do ataque no botão
            texto_ataque = font.render(ataque.nome, True, (255, 255, 255))  # Nome em branco
            icon_ataque = pygame.image.load(f"images/battle/icons_types/{ataque.tipo}.png")
            texto_rect = texto_ataque.get_rect(center=(pos_x + botao_largura // 2, pos_y + botao_altura // 2))
            self.screen.blit(icon_ataque, (pos_x + 10, pos_y + 5))
            self.screen.blit(texto_ataque, texto_rect.topleft)

        # Desenhar o cursor
        if mouse_clicked:
            self.screen.blit(self.pointer_grabbed, mouse_pos)
        else:
            self.screen.blit(self.pointer, mouse_pos)

    def selecionar_ataque(self):
        jogador_atual = self.jogador if self.turno % 2 == 0 else self.adversario
        adversario_atual = self.adversario if self.turno % 2 == 0 else self.jogador

        if jogador_atual.is_ai:
            return jogador_atual.ai.escolher_ataque(jogador_atual, adversario_atual)
        else:
            ataques = jogador_atual.ataques
            while True:
                mouse_pos = pygame.mouse.get_pos()
                mouse_clicked = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_clicked = True
                        pos = pygame.mouse.get_pos()

                        posicoes = [
                            (self.screen.get_width() // 2 - int(self.button.get_width() * 0.8) - 30, self.screen.get_height() - self.fundo_height + self.fundo_height // 2 - int(self.button.get_height() * 0.8) - 20),
                            (self.screen.get_width() // 2 + 30, self.screen.get_height() - self.fundo_height + self.fundo_height // 2 - int(self.button.get_height() * 0.8) - 20),
                            (self.screen.get_width() // 2 - int(self.button.get_width() * 0.8) - 30, self.screen.get_height() - self.fundo_height + self.fundo_height // 2 + 20),
                            (self.screen.get_width() // 2 + 30, self.screen.get_height() - self.fundo_height + self.fundo_height // 2 + 20)
                        ]

                        for i, ataque in enumerate(ataques):
                            rect = pygame.Rect(posicoes[i], (int(self.button.get_width() * 0.8), int(self.button.get_height() * 0.8)))  # Criar um retângulo para detectar o clique
                            if rect.collidepoint(pos):
                                time.sleep(0.2)  # Adiciona um pequeno delay para garantir a detecção do clique
                                return ataque

                # Desenha o fundo para limpar a tela antes de redesenhar os elementos
                self.screen.blit(self.background, (0, 0))

                self.desenhar_barras_de_vida()
                self.desenhar_barras_e_criaturas()
                self.desenhar_botao_ataque(ataques, mouse_pos, mouse_clicked)
                pygame.display.flip()

    def iniciar_batalha(self):
        clock = pygame.time.Clock()  # Adicionado para controlar o FPS
        running = True
        while running:
            # Desenha o fundo da tela
            self.screen.blit(self.background, (0, 0))

            # Desenha barras de vida, Pokémon, tipos, e efeitos
            self.desenhar_barras_de_vida()
            self.desenhar_barras_e_criaturas()

            # Desenha os botões de ataque e espera a seleção
            ataque_selecionado = self.selecionar_ataque()

            # Executa o turno com o ataque selecionado
            self.executar_acao(ataque_selecionado)

            # Atualiza a tela
            pygame.display.flip()

            # Verifica se o jogo acabou
            if self.verificar_fim_de_jogo():
                running = False

            # Passa para o próximo turno
            self.turno += 1

            clock.tick(60)  # Limita o jogo a 60 FPS

    def executar_acao(self, ataque):
        jogador_atual = self.jogador if self.turno % 2 == 0 else self.adversario
        adversario_atual = self.adversario if self.turno % 2 == 0 else self.jogador

        if adversario_atual.is_ai:
            adversario_atual.ai.aprender_com_oponente(ataque)
        
        if ataque.tipo in ["fogo", "agua", "planta", "lutador", "sombrio", "psiquico", "areia", "gelo", "eletrico", "normal"]:  # Adicione outros tipos conforme necessário
            self.animate_attack(ataque.tipo)
        
        pygame.display.flip()

        if ataque.efeito:
            self.gestor_efeitos.effects(ataque, jogador_atual, adversario_atual)
        else:
            multiplicador = functions.vantagens(ataque, adversario_atual)
            dano = ataque.calcular_dano(jogador_atual, adversario_atual, multiplicador)
            print(f"{jogador_atual.nome} usou {ataque.nome} e causou {dano} de dano!")
            adversario_atual.receber_dano(dano)

            self.desenhar_barras_de_vida()


    def mostrar_tela_vencedor(self, pokemon_image_path):
        backgroundVencedor = pygame.image.load("images/battle/imagemvencedor.png")
        backgroundVencedor = pygame.transform.scale(backgroundVencedor, (self.screen.get_width(), self.screen.get_height()))

        # Carrega a imagem do Pokémon vencedor
        imagemPokemon = pygame.image.load(pokemon_image_path)
        imagemPokemon = pygame.transform.scale(imagemPokemon, (400, 400))

        # Configurar o botão para o canto inferior direito
        buttonProximoJogo = pygame.transform.scale(self.buttonNewGame, (200, 50))
        buttonProximoJogoRect = buttonProximoJogo.get_rect(bottomright=(self.screen.get_width() - 40, self.screen.get_height() - 40))

        self.screen.blit(backgroundVencedor, (0, 0))
        self.screen.blit(imagemPokemon, (self.screen.get_width() // 2 - 200, self.screen.get_height() // 2 - 200))

        # Desenhar o botão e o texto "Próximo jogo"
        self.screen.blit(buttonProximoJogo, buttonProximoJogoRect.topleft)
        font = pygame.font.Font(None, 30)
        textoProximoJogo = font.render("Próximo jogo", True, (255, 255, 255))
        texto_rect = textoProximoJogo.get_rect(center=buttonProximoJogoRect.center)
        self.screen.blit(textoProximoJogo, texto_rect)

        pygame.display.flip()

        # Esperar pelo clique do usuário no botão
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True
                    if buttonProximoJogoRect.collidepoint(event.pos):
                        return

            # Redesenhar a tela para atualizar a posição do cursor
            self.screen.blit(backgroundVencedor, (0, 0))
            self.screen.blit(imagemPokemon, (self.screen.get_width() // 2 - 200, self.screen.get_height() // 2 - 200))
            self.screen.blit(buttonProximoJogo, buttonProximoJogoRect.topleft)
            self.screen.blit(textoProximoJogo, texto_rect)

            # Desenhar o cursor com base no clique
            if mouse_clicked:
                self.screen.blit(self.pointer_grabbed, mouse_pos)
            else:
                self.screen.blit(self.pointer, mouse_pos)

            pygame.display.flip()


    def verificar_fim_de_jogo(self):
        if self.jogador.hp <= 0:
            print(f"{self.jogador.nome} desmaiou! {self.adversario.nome} venceu a batalha!")
            self.mostrar_tela_vencedor(self.adversario.image_path)
            return True
        elif self.adversario.hp <= 0:
            print(f"{self.adversario.nome} desmaiou! {self.jogador.nome} venceu a batalha!")
            self.mostrar_tela_vencedor(self.jogador.image_path)
            return True
        return False
