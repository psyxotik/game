import pygame

#класс кнопок(описание их поведения)
class Buttons:
    def __init__(self, x, y, width, height, text, path, hover=None, sound=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = self.image
        if hover:
            self.hover_image = pygame.image.load(hover)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        if sound:
            self.sound = pygame.mixer.Sound(sound)
        self.is_hovered = False

    def draw(self, screen):
        cur_image = self.hover_image if self.is_hovered else self.image
        screen.blit(cur_image, self.rect.topleft)

        font = pygame.font.Font(None, 36)
        text_sur = font.render(self.text, True, 'white')
        text_rect = text_sur.get_rect(center=self.rect.center)
        screen.blit(text_sur, text_rect.center)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def hand_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
            