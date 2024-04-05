import pygame
from pygame.sprite import Sprite

#класс корабль(игрок)
class Ship(Sprite):
    def __init__(self, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('dist/data/ship_1.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.center_x = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom
        self.move_up = False
        self.move_down = False
        self.move_right = False
        self.move_left = False

    def draw_ship(self):
        self.screen.blit(self.image, self.rect)

    def update_ship(self):
        if self.move_left and self.rect.left > 0:
            self.center_x -= 2.5

        if self.move_right and self.rect.right < self.screen_rect.right:
            self.center_x += 2.5

        if self.move_up and self.rect.top > 0:
            self.rect.centery -= 2.5

        if self.move_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.centery += 2.5

        self.rect.centerx = self.center_x

    def create_ship(self):
        self.rect.bottom = self.screen_rect.bottom
