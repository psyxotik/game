import pygame.font
from ship import Ship
from pygame.sprite import Group

#класс для отоброжения очков
class Scores():
    def __init__(self, screen, info):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.info = info
        self.text_color = 'green'
        self.font = pygame.font.SysFont(None, 20)
        self.create_score()
        self.create_hi_score()
        self.show_lives()

    def create_score(self):
        self.score_feed = self.font.render(str(self.info.score), True, self.text_color, 'black')
        self.score_rect = self.score_feed.get_rect()
        self.score_rect.right = self.screen_rect.right - 30
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_feed, self.score_rect)
        self.screen.blit(self.hi_score_feed, self.hi_score_rect)
        self.lives.draw(self.screen)

    def create_hi_score(self):
        self.hi_score_feed = self.font.render(str(self.info.hi_score), True, self.text_color, 'black')
        self.hi_score_rect = self.hi_score_feed.get_rect()
        self.hi_score_rect.left = self.screen_rect.left + 30
        self.score_rect.top = 20

    def show_lives(self):
        self.lives = Group()
        for life_amount in range(self.info.ship_left):
            life = Ship(self.screen)
            life.rect.x = 15 + life_amount * life.rect.width
            life.rect.y = 20
            self.lives.add(life)