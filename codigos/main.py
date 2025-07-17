import pygame
from pygame.locals import *
from sys import exit
from button import Button
from gamemanager2 import GameManager
from data_loader import carregar_criaturas
from criatura import criatura
from batalha import batalha
from ia import PokemonAI
import time
import random
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
criaturas = carregar_criaturas()
dadoscriaturas = criaturas['criaturas']
print(dadoscriaturas)

def init_pygame():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Compmon')
    return screen

def load_image(path, scale_size=None):
    full_path = os.path.join(PROJECT_ROOT, path)
    try:
        image = pygame.image.load(full_path)
        if scale_size:
            image = pygame.transform.scale(image, scale_size)
        return image
    except pygame.error as e:
        print(f"Erro ao carregar a imagem: {full_path}")
        raise SystemExit(e)

def get_centered_rect(image, center_x, center_y):
    rect = image.get_rect(center=(center_x, center_y))
    return rect

def draw_menu(screen, background, compmonlogo_rect, startbutton):
    screen.blit(background, (0, 0))
    screen.blit(compmonlogo, compmonlogo_rect.topleft)
    startbutton.draw(screen)

def draw_mode_selection(screen, background, pvp_button, pve_button):
    screen.blit(background, (0, 0))
    pvp_button.draw(screen)
    pve_button.draw(screen)

def load_creatures_png(dados):
    pngs = []
    for creature in dados:
        png = load_image(creature['image_path'], (100, 100))
        pngs.append(png)
    return pngs

def handle_key_events(keys_pressed):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            keys_pressed.add(event.key)
        elif event.type == pygame.KEYUP:
            keys_pressed.discard(event.key)
    return True

def flip_image(image):
    return pygame.transform.flip(image, True, False)

def draw_images_creatures_battle(screen, criatura1, criatura2):
    creature1_image = load_image(criatura1.image_path, (400, 400))
    creature2_image = load_image(criatura2.image_path, (400, 400))
    creature1_name = criatura1.nome
    creature2_name = criatura2.nome

    if creature1_name not in ("Camarujo", "Codark", "Galouvor", "Ilusiopato", "Pokemolden"):
        creature1_image = flip_image(creature1_image)
    if creature2_name in ("Camarujo", "Codark", "Galouvor", "Ilusiopato", "Pokemolden"):
        creature2_image = flip_image(creature2_image)
        
    screen.blit(creature1_image, (230, 80))
    screen.blit(creature2_image, (1200, 550))

def draw_game(screen, criatura1, criatura2):
    screen.fill(WHITE)
    screen.blit(battleimage, (0, 0))
    draw_images_creatures_battle(screen, criatura1, criatura2)
    pygame.display.flip()
    pygame.time.wait(3000)

def draw_difficulty_selection(screen, background, easy_button, medium_button, hard_button):
    screen.blit(background, (0, 0))
    easy_button.draw(screen)
    medium_button.draw(screen)
    hard_button.draw(screen)

def main_loop(screen, background, compmonlogo_rect, startbutton, pvp_button, pve_button, easy_button, medium_button, hard_button):
    game_state = 'main_menu'
    game_mode = None
    difficulty = None
    clock = pygame.time.Clock()

    pygame.mouse.set_visible(False)
    keys_pressed = set()
    
    click_cooldown = 300
    last_click_time = 0
    
    pygame.mixer.music.load(os.path.join(PROJECT_ROOT, 'sounds/battle_music_1.ogg'))
    pygame.mixer.music.play(-1)

    running = True
    while running:
        running = handle_key_events(keys_pressed)
        
        current_time = pygame.time.get_ticks()

        if game_state == "main_menu":
            if current_time - last_click_time > click_cooldown:
                if startbutton.Click():
                    game_state = "mode_selection"
                    last_click_time = current_time
                elif pygame.K_RETURN in keys_pressed:
                    game_state = "mode_selection"
                    last_click_time = current_time
            draw_menu(screen, background, compmonlogo_rect, startbutton)

        elif game_state == "mode_selection":
            if current_time - last_click_time > click_cooldown:
                if pvp_button.Click():
                    game_mode = 'pvp'
                    game_state = "selection_menu"
                    last_click_time = current_time
                elif pve_button.Click():
                    game_mode = 'pve'
                    game_state = "difficulty_selection"
                    last_click_time = current_time
            draw_mode_selection(screen, background, pvp_button, pve_button)

        elif game_state == "difficulty_selection":
            if current_time - last_click_time > click_cooldown:
                if easy_button.Click():
                    difficulty = "iniciante"
                    game_state = "selection_menu"
                    last_click_time = current_time
                elif medium_button.Click():
                    difficulty = "intermediario"
                    game_state = "selection_menu"
                    last_click_time = current_time
                elif hard_button.Click():
                    difficulty = "avancado"
                    game_state = "selection_menu"
                    last_click_time = current_time
            draw_difficulty_selection(screen, background, easy_button, medium_button, hard_button)

        elif game_state == "selection_menu":
            game_manager = GameManager(screen, selectionbackground, dadoscriaturas, pngs)
            criatura1, criatura2 = game_manager.selecionar_criaturas()
            
            if game_mode == 'pve':
                criatura2.is_ai = True
                criatura2.ai = PokemonAI(nivel_dificuldade=difficulty)

            game_manager.attack_selection(criatura1, criatura2)
            game_manager.configurar_ataques(criatura1, criatura2)

            game_state = "playing"
            pygame.mixer.music.stop()
            
            music_path = os.path.join(PROJECT_ROOT, random.choice(['sounds/battle_music_3.ogg', 'sounds/battle_music_2.ogg']))
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)

        elif game_state == "playing":
            draw_game(screen, criatura1, criatura2)
            game_state = "battle"

        elif game_state == "battle":
            battle = batalha(criatura1, criatura2, battlebackground, screen)
            battle.iniciar_batalha()

            # <-- ADIÇÃO PARA SALVAR A MEMÓRIA DA IA -->
            # Se o oponente era uma IA, manda ela salvar o que aprendeu
            if criatura2.is_ai:
                criatura2.ai.salvar_memoria_da_batalha()
            # -----------------------------------------

            game_state = "main_menu" 
            last_click_time = pygame.time.get_ticks()

            pygame.mixer.music.stop()
            pygame.mixer.music.load(os.path.join(PROJECT_ROOT, 'sounds/battle_music_1.ogg'))
            pygame.mixer.music.play(-1)

        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            screen.blit(pointer_grabbed, mouse_pos)
        else:
            screen.blit(pointer, mouse_pos)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    exit()

if __name__ == "__main__":
    screen = init_pygame()
    
    background = load_image('images/background/background3.png', (SCREEN_WIDTH, SCREEN_HEIGHT))
    compmonlogo = load_image('images/background/compmonlogo.png', (900, 450))
    start_button_image = load_image('images/background/start.png', (480, 400))
    button_image = load_image('images/battle/button.png', (300, 100))

    pointer = load_image('images/util/pointer.png')
    pointer_grabbed = load_image('images/util/pointer_grabbed.png')

    compmonlogo_rect = get_centered_rect(compmonlogo, SCREEN_WIDTH // 2, 150)
    startbutton_rect = start_button_image.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 4) * 2))
    startbutton = Button(startbutton_rect.x, startbutton_rect.y, start_button_image)

    pvp_button_rect = button_image.get_rect(center=(SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 150))
    pve_button_rect = button_image.get_rect(center=(SCREEN_WIDTH // 2 + 160, SCREEN_HEIGHT // 2 + 150))
    pvp_button = Button(pvp_button_rect.x, pvp_button_rect.y, button_image, "Player vs Player")
    pve_button = Button(pve_button_rect.x, pve_button_rect.y, button_image, "Player vs IA")

    easy_button_rect = button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
    medium_button_rect = button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    hard_button_rect = button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
    easy_button = Button(easy_button_rect.x, easy_button_rect.y, button_image, "Fácil")
    medium_button = Button(medium_button_rect.x, medium_button_rect.y, button_image, "Médio")
    hard_button = Button(hard_button_rect.x, hard_button_rect.y, button_image, "Difícil")

    selectionbackground = load_image('images/background/background.png', (SCREEN_WIDTH, SCREEN_HEIGHT))
    pngs = load_creatures_png(dadoscriaturas)
    battleimage = load_image('images/battle/versus2.png', (SCREEN_WIDTH, SCREEN_HEIGHT))
    battlebackground = load_image('images/battle/fundobattlenovo.png', (SCREEN_WIDTH, SCREEN_HEIGHT))

    main_loop(screen, background, compmonlogo_rect, startbutton, pvp_button, pve_button, easy_button, medium_button, hard_button)