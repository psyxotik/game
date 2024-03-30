import pygame

#класс пуля
class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 2, 12)
        self.color = 'Red'
        self.speed = 6
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y_coord = float(self.rect.y)

    def update(self):
        self.y_coord -= self.speed
        self.rect.y = self.y_coord

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
