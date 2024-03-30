import pygame

#класс нло(противников)
class UFO(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(UFO, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('dist/data/ufo_2.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.start = 0
        self.speed = 2

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.rect.x += self.speed
        self.start += self.speed
        if self.start > 160 or self.start < -100:
            self.speed *= -1
            self.rect.y += 10