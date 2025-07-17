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
        
        self.effects_images = self.load_effect_images()

        self.fundo_width = 800
        self.fundo_height = 250

    def flipimage(self, image):
        return pygame.transform.flip(image, True, False)
    
    def load_tipo_png(self, tipo):
        return pygame.image.load(f"images/battle/icons_types/{tipo}.png")
    
    def resize_image(self, image, width, height):
        return pygame.transform.scale(image, (width, height))

    def load_effect_images(self):
        largura = 120
        altura = 30

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
        largura_total = 300
        altura_barra = 30

        posicao_vertical = 80
        x_jogador = 200
        x_adversario = self.screen.get_width() - largura_total - 200

        self.screen.blit(self.fundovidaesq, (0, 0))
        self.screen.blit(self.fundovidadir, (self.screen.get_width() - self.fundovidadir.get_width(), 0))

        localefeitos = pygame.transform.rotate(self.localefeitos, 180)
        localefeitos_x = self.fundovidaesq.get_width() - 25
        localefeitos_y = - (localefeitos.get_height() // 2) + 51

        localefeitos2 = self.flipimage(localefeitos)
        localefeitos2_x = self.screen.get_width() - self.fundovidadir.get_width() - localefeitos2.get_width() + 25
        localefeitos2_y = - (localefeitos2.get_height() // 2) + 51

        self.screen.blit(localefeitos, (localefeitos_x, localefeitos_y))
        self.screen.blit(localefeitos2, (localefeitos2_x, localefeitos2_y))

        largura_atual_jogador = max(0, int(largura_total * (self.jogador.hp / self.jogador.hpmax)))
        largura_atual_adversario = max(0, int(largura_total * (self.adversario.hp / self.adversario.hpmax)))

        pygame.draw.rect(self.screen, (0, 0, 0), (x_jogador, posicao_vertical, largura_total, altura_barra))
        pygame.draw.rect(self.screen, (0, 0, 0), (x_adversario, posicao_vertical, largura_total, altura_barra))

        pygame.draw.rect(self.screen, (255, 0, 0), (x_jogador + largura_atual_jogador, posicao_vertical, largura_total - largura_atual_jogador, altura_barra))
        pygame.draw.rect(self.screen, (255, 0, 0), (x_adversario, posicao_vertical, largura_total - largura_atual_adversario, altura_barra))

        pygame.draw.rect(self.screen, (0, 255, 0), (x_jogador, posicao_vertical, largura_atual_jogador, altura_barra))
        pygame.draw.rect(self.screen, (0, 255, 0), (x_adversario + (largura_total - largura_atual_adversario), posicao_vertical, largura_atual_adversario, altura_barra))

    def desenhar_triangulovezpoke(self, image, pos_x, pos_y):
        triangulo_x = pos_x + 135
        self.screen.blit(image, (triangulo_x, pos_y - image.get_height() - 10))

    def apply_red_tint(self, image):
        red_tinted_image = image.copy()
        red_tinted_image.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)
        return red_tinted_image

    def load_attack_frames(self, attack_type):
        frames = []
        for i in range(6):
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
        frames = self.load_attack_frames(attack_type)
        num_frames = len(frames)
        descent_speed = 100

        if self.turno % 2 == 0:
            defender_pos = (self.screen.get_width() - 700 + 175, self.screen.get_height() // 2 - 50)
        else:
            defender_pos = (300 + 175, self.screen.get_height() // 2 - 50)

        fireballs = []
        for _ in range(5):
            frame_index = 0
            frame = frames[frame_index]
            rotated_frame = pygame.transform.rotate(frame, -90)
            start_x = random.randint(defender_pos[0] - 150, defender_pos[0] + 50)
            start_y = random.randint(-300, -100)
            fireballs.append({'x': start_x, 'y': start_y, 'frame_index': frame_index})

        animation_running = True
        while animation_running:
            self.screen.blit(self.background, (0, 0))
            self.desenhar_barras_de_vida()
            self.desenhar_barras_e_criaturas()
            animation_running = False

            for fireball in fireballs:
                fireball['y'] += descent_speed
                if fireball['y'] + rotated_frame.get_height() < defender_pos[1] + 100:
                    animation_running = True
                fireball['frame_index'] = (fireball['frame_index'] + 1) % num_frames
                frame = frames[fireball['frame_index']]
                rotated_frame = pygame.transform.rotate(frame, -90)
                self.screen.blit(rotated_frame, (fireball['x'], fireball['y']))

            pygame.display.update()
            pygame.time.delay(50)

        self.apply_damage_effect()

    def animate_single_fireball(self, attack_type):
        frames = self.load_attack_frames(attack_type)
        num_frames = len(frames)

        if self.turno % 2 == 0:
            attacker_pos = (300, self.screen.get_height() // 2 - 50)
            defender_pos = (self.screen.get_width() - 700 + 175, self.screen.get_height() // 2 - 50)
            flipped = False
        else:
            attacker_pos = (self.screen.get_width() - 700, self.screen.get_height() // 2 - 50)
            defender_pos = (300 + 175, self.screen.get_height() // 2 - 50)
            flipped = True

        dx = (defender_pos[0] - attacker_pos[0]) / num_frames
        dy = (defender_pos[1] - attacker_pos[1]) / num_frames

        for i in range(num_frames):
            self.screen.blit(self.background, (0, 0))
            self.desenhar_barras_de_vida()
            self.desenhar_barras_e_criaturas()

            frame = frames[i]
            if flipped:
                frame = pygame.transform.flip(frame, True, False)

            frame_pos_x = attacker_pos[0] + i * dx
            if flipped:
                frame_pos_x -= 100

            frame_pos = (frame_pos_x, attacker_pos[1] + i * dy)
            self.screen.blit(frame, frame_pos)
            
            pygame.display.update()
            pygame.time.delay(50)

        self.apply_damage_effect()

    def apply_damage_effect(self):
        if self.turno % 2 == 0:
            defender_image = self.player2image
            defender_pos = (self.screen.get_width() - 700, self.screen.get_height() // 2 - 50)
            if self.adversario.nome in ("Camarujo", "Codark", "Galouvor", "Ilusiopato", "Pokemolden"):
                defender_image = self.flipimage(defender_image)
        else:
            defender_image = self.player1image
            defender_pos = (300, self.screen.get_height() // 2 - 50)
            if self.jogador.nome not in ("Camarujo", "Codark", "Galouvor", "Ilusiopato", "Pokemolden"):
                defender_image = self.flipimage(defender_image)

        defender_image = pygame.transform.scale(defender_image, (350, 350))
        red_tinted_image = defender_image.copy()
        red_tinted_image.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)

        self.screen.blit(red_tinted_image, defender_pos)
        pygame.display.update([defender_pos[0], defender_pos[1], red_tinted_image.get_width(), red_tinted_image.get_height()])
        pygame.time.delay(100)

        self.screen.blit(defender_image, defender_pos)
        pygame.display.update([defender_pos[0], defender_pos[1], defender_image.get_width(), defender_image.get_height()])

    def desenhar_barras_e_criaturas(self):
        player1image = pygame.transform.scale(self.player1image, (110, 110))
        player2image = pygame.transform.scale(self.player2image, (110, 110))

        if self.jogador.nome not in ("Camarujo", "Codark", "Galouvor", "Ilusiopato", "Pokemolden"):
            player1image = self.flipimage(player1image)
        if self.adversario.nome in ("Camarujo", "Codark", "Galouvor", "Ilusiopato", "Pokemolden"):
            player2image = self.flipimage(player2image)

        self.screen.blit(player1image, (15, 0))
        self.screen.blit(player2image, (self.screen.get_width() - 130, 0))

        compmonlogo = pygame.image.load("images/background/compmonlogo.png")
        compmonlogo = pygame.transform.scale(compmonlogo, (400, 300))
        self.screen.blit(compmonlogo, (762, -90))
        
        self.screen.blit(self.player1iconetipo, (self.fundovidaesq.get_width() // 2 - 70, 12))
        self.screen.blit(self.player2iconetipo, (self.screen.get_width() - 237, 12))

        font = pygame.font.Font(None, 35)
        nome1 = font.render(self.jogador.nome, True, (255, 255, 255))
        nome2 = font.render(self.adversario.nome, True, (255, 255, 255))

        self.screen.blit(nome1, (self.fundovidaesq.get_width() // 2 - 15, 25))
        nome2_x = self.screen.get_width() - 237 - nome2.get_width() - 10
        self.screen.blit(nome2, (nome2_x, 25))

        triangulo = pygame.transform.scale(self.triangulovezpoke, (50, 50))
        if self.turno % 2 == 0:
            self.desenhar_triangulovezpoke(triangulo, 300, self.screen.get_height() // 2 - 50)
        else:
            self.desenhar_triangulovezpoke(triangulo, self.screen.get_width() - 700, self.screen.get_height() // 2 - 50)

        player1image_battle = pygame.transform.scale(self.player1image, (350, 350))
        player2image_battle = pygame.transform.scale(self.player2image, (350, 350))

        if self.jogador.nome not in ("Camarujo", "Codark", "Galouvor", "Ilusiopato", "Pokemolden"):
            player1image_battle = self.flipimage(player1image_battle)
        if self.adversario.nome in ("Camarujo", "Codark", "Galouvor", "Ilusiopato", "Pokemolden"):
            player2image_battle = self.flipimage(player2image_battle)

        self.screen.blit(player2image_battle, (self.screen.get_width() - 700, self.screen.get_height() // 2 - 50))
        self.screen.blit(player1image_battle, (300, self.screen.get_height() // 2 - 50))

        self.desenhar_efeitos()

    def desenhar_efeitos(self):
        largura_img, altura_img = 130, 50
        inicio_x_jogador, inicio_y_jogador = 520, 10
        inicio_x_adversario, inicio_y_adversario = self.screen.get_width() - self.fundovidadir.get_width() - 250, 10
        posicao_jogador, posicao_adversario = 0, 0

        def calcular_posicao(posicao, inicio_x, inicio_y):
            coluna, linha = posicao % 2, posicao // 2
            return (inicio_x + coluna * largura_img, inicio_y + linha * altura_img)

        for efeito in self.jogador.efeitosativos.efeitosativos:
            if efeito in self.effects_images:
                x_y_jogador = calcular_posicao(posicao_jogador, inicio_x_jogador, inicio_y_jogador)
                self.screen.blit(self.effects_images[efeito], x_y_jogador)
                posicao_jogador += 1

        for efeito in self.adversario.efeitosativos.efeitosativos:
            if efeito in self.effects_images:
                x_y_adversario = calcular_posicao(posicao_adversario, inicio_x_adversario, inicio_y_adversario)
                self.screen.blit(self.effects_images[efeito], x_y_adversario)
                posicao_adversario += 1

    def desenhar_botao_ataque(self, ataques, mouse_pos, mouse_clicked):
        fundo = pygame.transform.scale(self.fundobuttonattack, (self.fundo_width, self.fundo_height))
        self.screen.blit(fundo, (self.screen.get_width() // 2 - self.fundo_width // 2, self.screen.get_height() - self.fundo_height))

        botao_largura, botao_altura = int(self.button.get_width() * 0.8), int(self.button.get_height() * 0.8)
        button = pygame.transform.scale(self.button, (botao_largura, botao_altura))
        buttonover = pygame.transform.scale(self.buttonover, (botao_largura, botao_altura))

        posicoes = [
            (self.screen.get_width() // 2 - botao_largura - 30, self.screen.get_height() - self.fundo_height + self.fundo_height // 2 - botao_altura - 20),
            (self.screen.get_width() // 2 + 30, self.screen.get_height() - self.fundo_height + self.fundo_height // 2 - botao_altura - 20),
            (self.screen.get_width() // 2 - botao_largura - 30, self.screen.get_height() - self.fundo_height + self.fundo_height // 2 + 20),
            (self.screen.get_width() // 2 + 30, self.screen.get_height() - self.fundo_height + self.fundo_height // 2 + 20)
        ]

        self.screen.blit(self.masterball, (self.screen.get_width() // 2 - self.masterball.get_width() // 2, self.screen.get_height() - self.fundo_height + self.fundo_height // 2 - self.masterball.get_height() // 2))

        font = pygame.font.Font(None, 20)
        for i, ataque in enumerate(ataques):
            pos_x, pos_y = posicoes[i]
            rect = pygame.Rect(pos_x, pos_y, botao_largura, botao_altura)

            if rect.collidepoint(mouse_pos):
                self.screen.blit(buttonover, (pos_x, pos_y))
            else:
                self.screen.blit(button, (pos_x, pos_y))

            texto_ataque = font.render(ataque.nome, True, (255, 255, 255))
            icon_ataque = pygame.image.load(f"images/battle/icons_types/{ataque.tipo}.png")
            texto_rect = texto_ataque.get_rect(center=(pos_x + botao_largura // 2, pos_y + botao_altura // 2))
            self.screen.blit(icon_ataque, (pos_x + 10, pos_y + 5))
            self.screen.blit(texto_ataque, texto_rect.topleft)

        if mouse_clicked:
            self.screen.blit(self.pointer_grabbed, mouse_pos)
        else:
            self.screen.blit(self.pointer, mouse_pos)

    def selecionar_ataque(self):
        jogador_atual = self.jogador if self.turno % 2 == 0 else self.adversario
        adversario_atual = self.adversario if self.turno % 2 == 0 else self.jogador

        if jogador_atual.is_ai:
            time.sleep(1) # Pequena pausa para o jogador ver a ação da IA
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
                            rect = pygame.Rect(posicoes[i], (int(self.button.get_width() * 0.8), int(self.button.get_height() * 0.8)))
                            if rect.collidepoint(pos):
                                time.sleep(0.2)
                                return ataque

                self.screen.blit(self.background, (0, 0))
                self.desenhar_barras_de_vida()
                self.desenhar_barras_e_criaturas()
                self.desenhar_botao_ataque(ataques, mouse_pos, mouse_clicked)
                pygame.display.flip()

    def iniciar_batalha(self):
        clock = pygame.time.Clock()
        running = True
        vencedor = None
        
        while running:
            self.screen.blit(self.background, (0, 0))
            self.desenhar_barras_de_vida()
            self.desenhar_barras_e_criaturas()
            
            # Atualiza a tela para mostrar o estado antes da seleção de ataque
            pygame.display.flip()

            ataque_selecionado = self.selecionar_ataque()
            self.executar_acao(ataque_selecionado)

            pygame.display.flip()

            vencedor = self.verificar_fim_de_jogo()
            if vencedor:
                running = False

            self.turno += 1
            clock.tick(60)
        
        return vencedor # <<< ALTERAÇÃO AQUI

    def executar_acao(self, ataque):
        jogador_atual = self.jogador if self.turno % 2 == 0 else self.adversario
        adversario_atual = self.adversario if self.turno % 2 == 0 else self.jogador

        if adversario_atual.is_ai:
            adversario_atual.ai.aprender_com_oponente(ataque)
        
        if ataque.tipo in ["fogo", "agua", "planta", "lutador", "sombrio", "psiquico", "areia", "gelo", "eletrico", "normal"]:
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
        imagemPokemon = pygame.image.load(pokemon_image_path)
        imagemPokemon = pygame.transform.scale(imagemPokemon, (400, 400))
        buttonProximoJogo = pygame.transform.scale(self.buttonNewGame, (200, 50))
        buttonProximoJogoRect = buttonProximoJogo.get_rect(bottomright=(self.screen.get_width() - 40, self.screen.get_height() - 40))

        self.screen.blit(backgroundVencedor, (0, 0))
        self.screen.blit(imagemPokemon, (self.screen.get_width() // 2 - 200, self.screen.get_height() // 2 - 200))
        
        self.screen.blit(buttonProximoJogo, buttonProximoJogoRect.topleft)
        font = pygame.font.Font(None, 30)
        textoProximoJogo = font.render("Próximo jogo", True, (255, 255, 255))
        texto_rect = textoProximoJogo.get_rect(center=buttonProximoJogoRect.center)
        self.screen.blit(textoProximoJogo, texto_rect)
        pygame.display.flip()

        esperando_clique = True
        while esperando_clique:
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True
                    if buttonProximoJogoRect.collidepoint(event.pos):
                        esperando_clique = False
            
            # Redesenha a tela para o cursor
            self.screen.blit(backgroundVencedor, (0, 0))
            self.screen.blit(imagemPokemon, (self.screen.get_width() // 2 - 200, self.screen.get_height() // 2 - 200))
            self.screen.blit(buttonProximoJogo, buttonProximoJogoRect.topleft)
            self.screen.blit(textoProximoJogo, texto_rect)
            if mouse_clicked:
                self.screen.blit(self.pointer_grabbed, mouse_pos)
            else:
                self.screen.blit(self.pointer, mouse_pos)
            pygame.display.flip()

    def verificar_fim_de_jogo(self):
        if self.jogador.hp <= 0:
            print(f"{self.jogador.nome} desmaiou! {self.adversario.nome} venceu a batalha!")
            self.mostrar_tela_vencedor(self.adversario.image_path)
            return self.adversario # <<< ALTERAÇÃO AQUI
        elif self.adversario.hp <= 0:
            print(f"{self.adversario.nome} desmaiou! {self.jogador.nome} venceu a batalha!")
            self.mostrar_tela_vencedor(self.jogador.image_path)
            return self.jogador # <<< ALTERAÇÃO AQUI
        return None # <<< ALTERAÇÃO AQUI