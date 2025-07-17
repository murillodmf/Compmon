'''def attack_selection(self, player1, player2):
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

        click_delay = 200  # Delay de 200ms para evitar cliques duplos acidentais
        last_click_time = pygame.time.get_ticks()

        pygame.mouse.set_visible(False)  # Oculta o cursor padrão do mouse

        while current_player < 2:
            selected_attacks = [None] * 4
            attacks_dispo = functions.filtrar_ataques(carregar_ataques(), players[current_player].tipo)
            selecting = True

            # Carrega e redimensiona a imagem da criatura e o frame uma vez
            player_image = pygame.image.load(players[current_player].image_path)
            player_image = pygame.transform.scale(player_image, (270, 250))  # Redimensiona a imagem da criatura

            while selecting:
                self.handle_key_events()
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()

                # Limpa a tela desenhando o background
                self.screen.blit(self.selection_background, (0, 0))

                # Desenha a criatura e o frame no canto superior esquerdo
                
                self.screen.blit(player_image, (120, 120))  # Posiciona a criatura dentro do frame

                # Adiciona a mensagem ao lado da imagem da criatura
                font = pygame.font.Font(None, 40)
                select_message = font.render(f"Escolha os ataques para {players[current_player].nome}!", True, (255, 255, 255))
                self.screen.blit(select_message, (700, 250))

                # Desenha os botões de ataques
                buttons = []
                for row in range(num_rows):
                    for col in range(num_columns):
                        index = row * num_columns + col
                        if index < len(attacks_dispo):
                            btn_x = start_x + col * (button_width + spacing_x)
                            btn_y = start_y + row * (button_height + spacing_y)
                            btn_rect = pygame.Rect(btn_x, btn_y, button_width, button_height)
                            buttons.append(btn_rect)

                            # Verifica se o botão foi clicado (com delay para evitar cliques rápidos)
                            if btn_rect.collidepoint(mouse_pos):
                                if pygame.time.get_ticks() - last_click_time > click_delay:
                                    if mouse_click[0]:  # Se o botão esquerdo do mouse foi clicado
                                        attack = attacks_dispo[index]
                                        if attack in selected_attacks:
                                            selected_attacks[selected_attacks.index(attack)] = None  # Deseleciona o ataque
                                        elif selected_attacks.count(None) > 0:
                                            if attack['tipo'] != players[current_player].tipo and attack['tipo'] != 'normal':  # verifica se já foram escolhidos 2 ataques fora do tipo da criatura
                                                if selected_attacks.count(None) <= 2:
                                                    selected_attacks[selected_attacks.index(None)] = attack  # Seleciona o ataque
                                            else:
                                                selected_attacks[selected_attacks.index(None)] = attack  # Seleciona o ataque
                                        last_click_time = pygame.time.get_ticks()  # Atualiza o tempo do último clique

                            # Desenha o botão com o estado correto (normal, hover ou selecionado)
                            if btn_rect.collidepoint(mouse_pos) or attacks_dispo[index] in selected_attacks:
                                self.screen.blit(button_over, btn_rect.topleft)
                            else:
                                self.screen.blit(button, btn_rect.topleft)

                            # Desenha o nome do ataque no botão
                            attack_name = font.render(attacks_dispo[index]['nome'], True, (255, 255, 255))

                            # Carrega a imagem do ícone do ataque
                            tipo_Ataque = attacks_dispo[index]['tipo']
                            icon_type = pygame.image.load(f'images/battle/icons_types/{tipo_Ataque}.png')

                            # Pega os rects de ambos para calcular as posições
                            name_rect = attack_name.get_rect()
                            icon_rect = icon_type.get_rect()

                            # Ajusta a posição do icon_rect à esquerda do name_rect dentro do btn_rect
                            icon_rect.topleft = (btn_rect.x + 10, btn_rect.y + (btn_rect.height - icon_rect.height) // 2)
                            name_rect.topleft = (icon_rect.right + 10, btn_rect.y + (btn_rect.height - name_rect.height) // 2)

                            # Desenha o ícone e o texto na tela
                            self.screen.blit(icon_type, icon_rect)
                            self.screen.blit(attack_name, name_rect)

                # Desenha a mensagem para pressionar Enter
                if selected_attacks.count(None) == 0:
                    enter_message = font.render("Pressione Enter para prosseguir", True, (255, 255, 255))
                    enter_rect = enter_message.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
                    self.screen.blit(enter_message, enter_rect)

                # Desenha o ponteiro do mouse personalizado
                if mouse_click[0]:
                    self.screen.blit(pointer_grabbed, mouse_pos)
                else:
                    self.screen.blit(pointer, mouse_pos)

                pygame.display.flip()
                Clock.tick(FPS)

                # Verifica se o jogador pressionou Enter para confirmar sua seleção
                if pygame.K_RETURN in self.keys_pressed and selected_attacks.count(None) == 0:
                    players[current_player].ataques = selected_attacks
                    current_player += 1
                    selecting = False

            # Limpa as teclas pressionadas ao mudar de jogador
            self.keys_pressed.clear()

        # Após a seleção, retorna para a próxima fase do jogo
        return players[0], players[1]
'''