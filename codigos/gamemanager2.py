import random
import pygame
from criatura import criatura 
from selectioncursor import SelectionCursor
import textwrap
from data_loader import carregar_ataques
from functions import filtrar_ataques
from ataque import ataque

class GameManager:
    def __init__(self, screen, background, dados_criaturas, pngs):
        # Inicializa a tela e carrega os dados das criaturas e o fundo da tela de seleção
        self.screen = screen
        self.dados_criaturas = dados_criaturas  # Dados das criaturas passados como parâmetro
        self.selection_background = background
        self.pngs = pngs  # Dicionário de PNGs passados como parâmetro
        self.keys_pressed = set()  # Armazena as teclas que estão sendo pressionadas
        self.creatures_selected = [None, None]  # Armazena as criaturas selecionadas por cada jogador

    def handle_key_events(self):
        # Lida com os eventos de teclado e saída do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)

    def selecionar_criaturas(self):
    # Gerencia o processo de seleção de criaturas pelos jogadores
        cursors, positions = self.init_selection(self.dados_criaturas)  # Inicializa os cursos e as posições das criaturas

        while None in self.creatures_selected:
        # Continua o loop até que ambos os jogadores tenham selecionado suas criaturas
            self.handle_key_events()

            for i, cursor in enumerate(cursors):
            # Atualiza a posição do cursor e verifica se uma criatura foi selecionada ou deselecionada
                cursor.move(self.keys_pressed, positions)

                if cursor.controls['select'] in self.keys_pressed and not cursor.selected:
                # Seleciona a criatura atual e bloqueia o cursor
                    col_index, row_index = cursor.position
                    index = col_index * 3 + (row_index)
                    self.creatures_selected[i] = self.dados_criaturas[index]
                    cursor.select()

                if cursor.selected and cursor.controls['cancel'] in self.keys_pressed:
                # Permite que o jogador deselecione a criatura e mova o cursor novamente
                    self.creatures_selected[i] = None
                    cursor.deselect()

            self.draw_selection_screen(positions, cursors)  # Desenha a tela de seleção

    # Retorna as criaturas selecionadas após ambos os jogadores confirmarem suas escolhas
        return self.configurar_criatura(self.creatures_selected[0]), self.configurar_criatura(self.creatures_selected[1])


    def init_selection(self, creatures_data):
    # Organiza as criaturas em uma grade de 10 colunas por 3 linhas e inicializa os cursos de seleção
        positions = []
    
        creature_width = 100  # Largura de cada criatura
        creature_height = 100  # Altura de cada criatura

    # Espaçamento horizontal e vertical ajustado para centralizar as colunas
        x_spacing = 50  # Espaçamento horizontal entre as colunas
        y_spacing = 30  # Espaçamento vertical entre as linhas

        start_x = (1920 - (10 * creature_width + 9 * x_spacing)) // 2  # Ajusta para centralizar as colunas
        start_y = (1080 - (3 * creature_height + 2 * y_spacing)) // 2  # Ajusta para centralizar as linhas

        num_columns = 10  # Número de colunas
        num_rows = 3  # Número de linhas

    # Organiza as criaturas por colunas
        for col in range(num_columns):
            for row in range(num_rows):
                index = col + row * num_columns  # Calcula o índice da criatura baseado na coluna e linha
                if index < len(creatures_data):
                    x = start_x + col * (creature_width + x_spacing)
                    y = start_y + row * (creature_height + y_spacing)
                    positions.append((creatures_data[index], (x, y)))

    # Inicializa os cursos de seleção para cada jogador
        cursors = [
            SelectionCursor([0, 0], (100, 100), {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d, 'select': pygame.K_SPACE, 'cancel': pygame.K_ESCAPE}, (255, 0, 0)),
            SelectionCursor([9, 2], (100, 100), {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'select': pygame.K_RETURN, 'cancel': pygame.K_BACKSPACE}, (0, 255, 0))
        ]
    
        return cursors, positions



    def draw_selection_screen(self, positions, cursors):
    # Desenha o fundo da tela de seleção
        self.screen.blit(self.selection_background, (0, 0))

        # Desenha a mensagem de boas-vindas no topo da tela
        font = pygame.font.Font(None, 40)  # Fonte padrão com tamanho 60
        welcome_message = font.render("Bem-vindo ao mundo Compmon! Selecione sua criatura.", True, (255, 255, 255))
        welcome_rect = welcome_message.get_rect(center=(self.screen.get_width() // 2, 200))
        self.screen.blit(welcome_message, welcome_rect)

        # Dicionário de descrições personalizadas para cada criatura
        descricoes = {
            "Beta": "Nosso peixinho favorito, sempre pronto para um mergulho no código.",
            "Tortugrita": "Tartaruga poderosa do DC, sem pressa, mais sempre no tempo certo.",
            "Camarujo": "Caramujo marujo, sempre pronto para uma aventura no mar da computação.",
            "Magmamute": "Mamute mais poderoso da computação, capaz de derrotar até o código mais complexo.",
            "Picolava": "Sorvete de fogo, responsável por derreter cerébros de computeiros.",
            "Tulcao": "Tucano em erupção, sempre pronto para uma explosão de conhecimento.",
            "Perry": "Um figurinha lendaria da computação, conhecido por suas desavenças com figuras acadêmicas.",
            "Sambambaia": "Samambaia dançarina, sempre pronta para uma festa de implementação.",
            "Pimentex": "Pimenta professora desaparecida do DC, dizem que a ultima vez que foi vista estava fazendo autovetores.",
            "Kung-ru": "Canguru mestre das artes marciais, sempre pronto para uma maratona de programação.",
            "Gorilove": "Gorila apaixonado do DC, dizem que seu amor contagiou alunos no ultimo semestre...",
            "Kichute": "Chute de conhecimento, sempre pronto para chutar a preguiça pra longe.",
            "Corujao": "Coruja noturna, dizem que elas sempre esta ao seu lado na madrugada antes de provas...",
            "Rockaveira": "Lider dos rockeiros do DC, sempre pronto para uma batalha.",
            "Codark": "Aliado do boss de ED2, foi capaz de abater dezenas de espartanos..",
            "Ilusiopato": "Pato ilusionista, capaz de prever o futuro do seu codigo.",
            "Psipanze": "Chimpanzé psiquico, sempre é visto pelas redondezas da UEL.",
            "Galouvor": "Galo do louvor, as vezes só a ele que se pode recorrer para te ajudar antes de uma prova...",
            "Escorpierva": "Escorpiao guerreiro, seu ferrão é capaz de destruir qualquer código mal implementado.",
            "Ratimbum": "Nosso castelo de areia, pronto para encarar uma batalha no compmon.",
            "Hermano": "Nosso amigo de todas as horas, sempre importante ter alguem do seu lado durante os 4 anos.",
            "Kinguim": "Pinguim rei, sempre pronto para uma batalha de conhecimento.",
            "Articao": "Cachorro de gelo, sempre gelado para resolver problemas quentes.",
            "Frioboi": "Boi gelado, o mais frio de todos os compmons.",
            "Pokemolden": "Compmon importantissimo do DC, sem ele o DC nunca funicionaria corretamente.",
            "Felinux": "Assim como Codark, aliado do boss, sempre presente no desenvolvimento da disciplina.",
            "Durashell": "Compmon pilha, dizem que é o responsável pela luz que nunca se apaga no DC.",
            "Silva": "Irmão do Souza e do Santos, todo ano aparece um novo no DC.",
            "Souza": "Irmão do Silva e do Santos, figurinha recorrente todos os anos.",
            "Santos": "Irmão do Souza e do Silva, seu loop while anual nunca deu igual a NULL...",

            # Adicione mais descrições conforme necessário
        }

        # Fonte para a descrição
        desc_font = pygame.font.Font(None, 30)

        # Percorre as posições e desenha as criaturas
        for index, (creature_data, pos) in enumerate(positions):
            image = self.pngs[index]  # Obtém a imagem da lista self.pngs pelo índice
            self.screen.blit(image, pos)  # Desenha a imagem na posição correta

        # Desenhar as descrições baseadas na posição do cursor
        
        for i, cursor in enumerate(cursors):
            cursor.draw(self.screen)  # Desenha as bordas ao redor das criaturas selecionadas

            # Obtém a posição do cursor
            col_index = cursor.position[0]  # Coluna
            row_index = cursor.position[1]  # Linha

            # Calcula o índice correto na lista positions
            index = col_index * 3 + (row_index)  # 3 criaturas por coluna

            # Verifica se o índice é válido
            if index < len(positions):
                creature_data = self.dados_criaturas[index]
                nome = creature_data['nome']
                descricao = descricoes.get(nome, "Descrição não disponível.")

                # Renderiza o nome da criatura
                nome_surface = desc_font.render(nome, True, (255, 255, 255))

            # Divide a descrição em várias linhas se for muito longa
                descricao_linhas = textwrap.wrap(descricao, width=40)

                if i == 0:  # Jogador WASD
                    nome_rect = nome_surface.get_rect(midbottom=(400, self.screen.get_height() - 190))
                    descricao_start_y = self.screen.get_height() - 180
                else:  # Jogador de Setas
                    nome_rect = nome_surface.get_rect(midbottom=(self.screen.get_width() - 400, self.screen.get_height() - 190))
                    descricao_start_y = self.screen.get_height() - 180

                self.screen.blit(nome_surface, nome_rect)

                # Renderiza cada linha da descrição abaixo da anterior
                for linha in descricao_linhas:
                    descricao_surface = desc_font.render(linha, True, (255, 255, 255))
                    descricao_rect = descricao_surface.get_rect(midtop=(nome_rect.centerx, descricao_start_y))
                    self.screen.blit(descricao_surface, descricao_rect)
                    descricao_start_y += desc_font.get_height()

        pygame.display.flip()

    def attack_selection(self, player1, player2):
        players = [player1, player2]
        current_player = 0

        Clock = pygame.time.Clock()
        FPS = 60

        # Carrega as imagens uma vez antes do loop
        pointer = pygame.image.load("images/util/pointer.png")
        pointer_grabbed = pygame.image.load("images/util/pointer_grabbed.png")

        button = pygame.image.load("images/battle/button.png")
        button_over = pygame.image.load("images/battle/buttonover.png")

        # Posições dos botões
        num_columns = 5
        num_rows = 6
        button_width = button.get_width()
        button_height = button.get_height()
        spacing_x = 20
        spacing_y = 20

        total_width = num_columns * button_width + (num_columns - 1) * spacing_x
        total_height = num_rows * button_height + (num_rows - 1) * spacing_y

        start_x = (1920 - total_width) // 2
        start_y = (1080 - total_height) // 2 + 150

        click_delay = 200
        last_click_time = pygame.time.get_ticks()

        pygame.mouse.set_visible(False)

        while current_player < 2:
            # <<< MODIFICAÇÃO PRINCIPAL AQUI >>>
            # Se o jogador atual for uma IA, escolhe os ataques aleatoriamente e pula a seleção manual
            if players[current_player].is_ai:
                print(f"A IA está escolhendo os ataques para {players[current_player].nome}...")
                attacks_dispo = filtrar_ataques(carregar_ataques(), players[current_player].tipo)
                
                # A IA escolhe 4 ataques aleatórios da lista de ataques disponíveis
                if len(attacks_dispo) >= 4:
                    players[current_player].ataques = random.sample(attacks_dispo, 4)
                else: # Caso a criatura tenha menos de 4 ataques disponíveis
                    players[current_player].ataques = attacks_dispo
                
                current_player += 1 # Move para o próximo jogador
                self.keys_pressed.clear() # Limpa as teclas para evitar seleção acidental do próximo jogador
                continue # Pula o resto do loop e vai para a próxima iteração

            # --- FIM DA MODIFICAÇÃO ---
            
            # O código abaixo só será executado se o jogador for humano
            selected_attacks = [None] * 4
            attacks_dispo = filtrar_ataques(carregar_ataques(), players[current_player].tipo)
            selecting = True

            player_image = pygame.image.load(players[current_player].image_path)
            player_image = pygame.transform.scale(player_image, (270, 250))

            while selecting:
                self.handle_key_events()
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()

                self.screen.blit(self.selection_background, (0, 0))
                self.screen.blit(player_image, (120, 120))

                font = pygame.font.Font(None, 40)
                select_message = font.render(f"Escolha os ataques para {players[current_player].nome}!", True, (255, 255, 255))
                self.screen.blit(select_message, (700, 250))

                small_font = pygame.font.Font(None, 30)
                count_ataques_diff = 0
                buttons = []
                for row in range(num_rows):
                    for col in range(num_columns):
                        index = row * num_columns + col
                        if index < len(attacks_dispo):
                            btn_x = start_x + col * (button_width + spacing_x)
                            btn_y = start_y + row * (button_height + spacing_y)
                            btn_rect = pygame.Rect(btn_x, btn_y, button_width, button_height)
                            buttons.append(btn_rect)

                            if btn_rect.collidepoint(mouse_pos):
                                if pygame.time.get_ticks() - last_click_time > click_delay:
                                    if mouse_click[0]:
                                        attack = attacks_dispo[index]
                                        if attack in selected_attacks:
                                            if attack['tipo'] != players[current_player].tipo and attack['tipo'] != 'normal':
                                                count_ataques_diff -= 1
                                            selected_attacks[selected_attacks.index(attack)] = None
                                        elif selected_attacks.count(None) > 0:
                                            if attack['tipo'] != players[current_player].tipo and attack['tipo'] != 'normal':
                                                if count_ataques_diff < 2:
                                                    count_ataques_diff += 1
                                                    selected_attacks[selected_attacks.index(None)] = attack
                                            else:
                                                selected_attacks[selected_attacks.index(None)] = attack
                                        last_click_time = pygame.time.get_ticks()

                            if btn_rect.collidepoint(mouse_pos) or attacks_dispo[index] in selected_attacks:
                                self.screen.blit(button_over, btn_rect.topleft)
                            else:
                                self.screen.blit(button, btn_rect.topleft)

                            tipo_Ataque = attacks_dispo[index]['tipo']
                            icon_type = pygame.image.load(f'images/battle/icons_types/{tipo_Ataque}.png')
                            icon_rect = icon_type.get_rect()
                            icon_rect.topleft = (btn_rect.x + 10, btn_rect.y + (btn_rect.height - icon_rect.height) // 2)
                            self.screen.blit(icon_type, icon_rect)

                            attack_name = small_font.render(attacks_dispo[index]['nome'], True, (255, 255, 255))
                            if attacks_dispo[index]['dano'] is not False:
                                attack_detail = small_font.render(str([attacks_dispo[index]['dano']]), True, (255, 255, 255))
                            else:
                                attack_detail = small_font.render(str([attacks_dispo[index]['efeito']]), True, (255, 255, 255))
                            
                            name_detail_rect = attack_name.get_rect()
                            name_detail_rect.topleft = (icon_rect.right + 10, btn_rect.y + (btn_rect.height - name_detail_rect.height) // 2)
                            
                            self.screen.blit(attack_name, name_detail_rect)
                            detail_rect = attack_detail.get_rect(midleft=(name_detail_rect.right + 10, name_detail_rect.centery))
                            self.screen.blit(attack_detail, detail_rect)

                if selected_attacks.count(None) == 0:
                    enter_message = font.render("Pressione Enter para prosseguir", True, (255, 255, 255))
                    enter_rect = enter_message.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
                    self.screen.blit(enter_message, enter_rect)

                if mouse_click[0]:
                    self.screen.blit(pointer_grabbed, mouse_pos)
                else:
                    self.screen.blit(pointer, mouse_pos)

                pygame.display.flip()
                Clock.tick(FPS)

                if pygame.K_RETURN in self.keys_pressed and selected_attacks.count(None) == 0:
                    players[current_player].ataques = selected_attacks
                    current_player += 1
                    selecting = False

            self.keys_pressed.clear()

        return players[0], players[1]

    def configurar_criatura(self, criatura_data):
        # Configura a criatura selecionada com seus atributos e ataques
        return criatura(criatura_data['nome'], criatura_data['tipo'], criatura_data['hp'], 
                        criatura_data['atk'], criatura_data['def'], criatura_data['spe'], 
                        criatura_data['ataques'], criatura_data['image_path'])
    
    def configurar_ataques(self, criatura1, criatura2):
        # Configura os ataques das criaturas selecionadas
        ataques1 = []
        ataques2 = []

        for ataque_data in criatura1.ataques:
            atak = ataque(ataque_data['nome'], ataque_data['tipo'], ataque_data['dano'], ataque_data['velocidade'], ataque_data['efeito'], ataque_data['quantidade'])
            ataques1.append(atak)

        for ataque_data in criatura2.ataques:
            atak = ataque(ataque_data['nome'], ataque_data['tipo'], ataque_data['dano'], ataque_data['velocidade'], ataque_data['efeito'], ataque_data['quantidade'])
            ataques2.append(atak)

        criatura1.ataques = ataques1
        criatura2.ataques = ataques2
