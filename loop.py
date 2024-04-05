import pygame
import sys
from weapon import Bullet
from aliens import UFO
import time
from window import math_quiz


pygame.mixer.init()
shoot = pygame.mixer.Sound('dist/data/laser_shot.mp3')
ufo_boom = pygame.mixer.Sound('dist/data/ufo_dead.mp3')
ship_boom = pygame.mixer.Sound('dist/data/ship_boom.mp3')
shoot.set_volume(0.3)

amo_bullets = 3
def terminate():
    pygame.quit()
    sys.exit()

#обработка событий игры
def events(ship, bullets, screen):
    menu = 0
    global amo_bullets
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                ship.move_right = True
            elif event.key == pygame.K_a:
                ship.move_left = True
            elif event.key == pygame.K_w:
                ship.move_up = True
            elif event.key == pygame.K_s:
                ship.move_down = True
            elif event.key == pygame.K_SPACE:
                shoot.play()
                amo_bullets -= 1
                print(amo_bullets)
                if amo_bullets <= 0:
                    math_quiz(amo_bullets)

                    amo_bullets = 3
                new_bullet = Bullet(screen, ship)
                bullets.add(new_bullet)
            if event.key == pygame.K_ESCAPE:
                menu += 1
                return menu

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                ship.move_right = False
            elif event.key == pygame.K_a:
                ship.move_left = False
            elif event.key == pygame.K_w:
                ship.move_up = False
            elif event.key == pygame.K_s:
                ship.move_down = False


#обновление экрана
def update_screen(screen, ship, bullets, ufos, info, sc):
    sc.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.draw_ship()
    ufos.draw(screen)
    pygame.display.flip()

#убираем лишние объекты, еслли они вышли за экран
def remove_bullets(bullets, ufos, screen, sc, info):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    collision = pygame.sprite.groupcollide(bullets, ufos, True, True)
    if collision:
        for uf in collision.values():
            info.score += 100 * len(uf)
            ufo_boom.play()
        sc.create_score()
        is_hi_score(info, sc)
        sc.show_lives()
    if len(ufos) == 0:
        bullets.empty()
        create_ufos(screen, ufos)

#создаём группу противников
def create_ufos(screen, ufos):
    ufo = UFO(screen)
    ufo_width = ufo.rect.width
    ufo_row = int((700 - 2 * ufo_width) / ufo_width)
    ufo_height = ufo.rect.height
    ufo_column = int((800 - 100 - 2 * ufo_height) / ufo_height)
    for ufo_c in range(ufo_column - 4):
        for ufo_r in range(ufo_row):
            ufo = UFO(screen)
            ufo.x = ufo_width + ufo_width * ufo_r
            ufo.y = ufo_height + ufo_height * ufo_c
            ufo.rect.x = ufo.x
            ufo.rect.y = ufo.rect.height + ufo.rect.height * ufo_c
            ufos.add(ufo)

#проверяем взаимодействия нло с другими объектами
def update_ufos(info, screen, ship, ufos, bullets, sc):
    ufos.update()
    if pygame.sprite.spritecollideany(ship, ufos):
        ship_dead(info, screen, ship, ufos, bullets, sc)
    ufos_has_passed(info, screen, ship, ufos, bullets, sc)

#игрок потерял жизнь
def ship_dead(info, screen, ship, ufos, bullets, sc):
    if info.ship_left > 0:
        ship_boom.play()
        info.ship_left -= 1
        sc.show_lives()
        ufos.empty()
        bullets.empty()
        create_ufos(screen, ufos)
        ship.create_ship()
        time.sleep(1)
    else:
        info.run_game = False

#проверка на прохождение нло всего экарна
def ufos_has_passed(info, screen, ship, ufos, bullets, sc):
    screen_rect = screen.get_rect()
    for uf in ufos.sprites():
        if uf.rect.bottom >= screen_rect.bottom:
            ship_dead(info, screen, ship, ufos, bullets, sc)
            break

#проверка на новый рекорд
def is_hi_score(info, sc):
    if info.score > info.hi_score:
        info.hi_score = info.score
        sc.create_hi_score()
        with open('dist/data/score.txt', 'w') as f:
            f.write(str(info.hi_score))

