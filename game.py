import pygame, loop
from ship import Ship
from pygame.sprite import Group
from score import Scores
from menu_buttons import Buttons
from player import Information
from io import BytesIO
import base64
from cryptography.fernet import Fernet
import hashlib


pygame.init()

WIDTH, HEIGHT = 700, 800
max_fps = 60


screen_menu = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('settings')
bg = pygame.image.load('dist/data/space.png')
bg2 = pygame.image.load('dist/data/space_2.png')
clock = pygame.time.Clock()
namehints = {'p':'png','j':'jpg','o':'ogg','m':'mp3','w':'wav','t':'txt'}
f = Fernet(base64.urlsafe_b64encode(hashlib.md5('<password here>'.encode()).hexdigest().encode("utf-8")))
info = Information()

#игра
def start():
    pygame.display.set_caption('Space Conqueror')
    ship = Ship(screen_menu)
    bullets = Group()
    ufos = Group()
    loop.create_ufos(screen_menu, ufos)

    sc = Scores(screen_menu, info)
    bg_y = 0
    running = True
    amo_bullets = 3
    while running:
        screen_menu.blit(bg2, (0, bg_y))
        screen_menu.blit(bg2, (0, bg_y + 800))
        bg_y -= 2
        if bg_y == -800:
            bg_y = 0
        loop.events(ship, bullets, screen_menu, amo_bullets)
        clock.tick(max_fps)
        if info.run_game:

            loop.update_screen(screen_menu, ship, bullets, ufos, info, sc)
            loop.remove_bullets(bullets, ufos, screen_menu, sc, info)
            loop.update_ufos(info, screen_menu, ship, ufos, bullets, sc)
            ship.update_ship()
        else:
            running = False
            fade()
            game_over()
        if loop.events(ship, bullets, screen_menu, amo_bullets):
            fade()
            running = False
    main_menu()

#главное меню(начальное окно)
def main_menu():
    play_button = Buttons(WIDTH / 2 - (252 / 2), 100, 252, 74, '', 'dist/data/play_button.png', 'dist/data/shiny_play_button.png',
                          'dist/data/button_sound.mp3')
    settings_button = Buttons(WIDTH / 2 - (252 / 2), 200, 252, 74, '', 'dist/data/options_button.png',
                              'dist/data/shiny_options.png',
                              'dist/data/button_sound.mp3')
    quit_button = Buttons(WIDTH / 2 - (252 / 2), 300, 252, 74, '', 'dist/data/exit_button.png',
                          'dist/data/shiny_exit_button.png',
                          'dist/data/button_sound.mp3')
    buttons = [play_button, settings_button, quit_button]

    run = True
    while run:
        screen_menu.fill('black')
        screen_menu.blit(bg, (0, 0))
        font = pygame.font.Font(None, 72)
        text_surface = font.render('Space Conqueror', True, 'purple')
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 50))
        screen_menu.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                loop.terminate()

            if event.type == pygame.USEREVENT and event.button == play_button:
                fade()
                start()

            if event.type == pygame.USEREVENT and event.button == settings_button:
                fade()
                settings_menu()

            if event.type == pygame.USEREVENT and event.button == quit_button:
                loop.terminate()

            play_button.hand_event(event)
            settings_button.hand_event(event)
            quit_button.hand_event(event)

        for but in buttons:
            but.check_hover(pygame.mouse.get_pos())
            but.draw(screen_menu)

        pygame.display.flip()

#меню настроек
def settings_menu():
    music = [True, False]

    audio_button = Buttons(WIDTH / 2 - (252 / 2), 350, 252, 74, '', 'dist/data/audio_button.png',
                               'dist/data/shiny_audio_button.png',
                              'dist/data/button_sound.mp3')

    set_btns = [audio_button]
    m_value = 2

    run = True
    while run:

        screen_menu.fill('black')
        screen_menu.blit(bg2, (0, 0))

        font = pygame.font.Font(None, 72)
        text_surface = font.render('Options', True, 'purple')
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 50))
        screen_menu.blit(text_surface, text_rect)

        size = pygame.font.Font(None, 31)
        info_text = font.render('Для выхода нажмите: esc', True, 'White')
        info_text_rect = info_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        screen_menu.blit(info_text, info_text_rect)

        font = pygame.font.Font(None, 35)
        text_surface = font.render('Управление: A и D чтобы двигаться, пробел - стрелять', True, 'white')
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 100))
        screen_menu.blit(text_surface, text_rect)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                loop.terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fade()
                    run = False
            if event.type == pygame.USEREVENT and event.button == audio_button:
                m_value += 1
                info.cur_music = music[m_value % 2]
                is_music()

            for btn in set_btns:
                btn.hand_event(event)

        for btn in set_btns:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen_menu)

        pygame.display.flip()




#окно поражения(последнее)
def game_over():
    exit_button = Buttons(WIDTH / 2 - (252 / 2), 300, 252, 74, '', 'dist/data/exit_button.png',
                               'dist/data/shiny_exit_button.png',
                              'dist/data/button_sound.mp3')

    restart_button = Buttons(WIDTH / 2 - (252 / 2), 200, 252, 74, '', 'dist/data/restart_button.png',
                               'dist/data/shiny_restart_button.png',
                              'dist/data/button_sound.mp3')
    set_buttons = [exit_button, restart_button]
    run = True
    while run:

        screen_menu.fill('black')
        font = pygame.font.Font(None, 72)
        text_surface = font.render('Game Over', True, 'White')
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 50))
        screen_menu.blit(text_surface, text_rect)

        size = pygame.font.Font(None, 47)
        info_text = size.render(f'Ваш рекорд:{info.hi_score}', True, 'White')
        info_text_rect = info_text.get_rect(center=(WIDTH // 2, 97))
        screen_menu.blit(info_text, info_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                loop.terminate()
            if event.type == pygame.USEREVENT and event.button == exit_button:
                run = False
                fade()
                main_menu()
            if event.type == pygame.USEREVENT and event.button == restart_button:
                run = False
                fade()
                start()

            for btn in set_buttons:
                btn.hand_event(event)

        for btn in set_buttons:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen_menu)

        pygame.display.flip()


#загрузка музыки
def load_dat(filename):


    enc_data = open(filename + '.dat', 'rb').read()
    dec_data = BytesIO(f.decrypt(enc_data))
    return (dec_data, namehints[filename[-1:]])


def is_music():
    if info.cur_music:
        (fileobj, namehint) = load_dat('dist/data/music theme o')
        pygame.mixer.music.load(fileobj)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops=-1)
    else:
        pygame.mixer.music.stop()

#плавные переходы
def fade():
    run = True
    fade_level = 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                loop.terminate()
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill('black')
        fade_surface.set_alpha(fade_level)
        screen_menu.blit(fade_surface, (0, 0))

        fade_level += 5
        if fade_level >= 105:
            fade_level = 255
            run = False

        pygame.display.flip()
        clock.tick(max_fps)


is_music()
main_menu()
