import pygame

class SelectionCursor:
    def __init__(self, start_pos, grid_size, controls, color):
        self.position = start_pos
        self.grid_size = grid_size
        self.controls = controls
        self.rect = pygame.Rect(0, 0, grid_size[0], grid_size[1])
        self.color = color
        self.selected = False
        self.keys_held = {key: False for key in controls.values()}  # Rastreia se a tecla está pressionada

    def move(self, keys_pressed, creature_positions):
        if not self.selected:
            if self.controls['up'] in keys_pressed and not self.keys_held[self.controls['up']]:
                self.position[1] = max(self.position[1] - 1, 0)
                self.keys_held[self.controls['up']] = True
            elif self.controls['down'] in keys_pressed and not self.keys_held[self.controls['down']]:
                self.position[1] = min(self.position[1] + 1, 2)  # 2 é o número máximo de linhas (0, 1, 2)
                self.keys_held[self.controls['down']] = True
            elif self.controls['left'] in keys_pressed and not self.keys_held[self.controls['left']]:
                self.position[0] = max(self.position[0] - 1, 0)
                self.keys_held[self.controls['left']] = True
            elif self.controls['right'] in keys_pressed and not self.keys_held[self.controls['right']]:
                self.position[0] = min(self.position[0] + 1, 9)  # 9 é o número máximo de colunas (0 a 9)
                self.keys_held[self.controls['right']] = True
            else:
                # Libera a tecla quando não está mais sendo pressionada
                for key in self.keys_held:
                    if key not in keys_pressed:
                        self.keys_held[key] = False

            # Calcula o índice com base na nova posição, considerando o layout em colunas
            index = self.position[0] * 3 + self.position[1]  # Multiplicamos pela quantidade de linhas (3)
            
            # Atualiza a posição do rect do cursor com base nas coordenadas da criatura
            self.rect.topleft = creature_positions[index][1]

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False
