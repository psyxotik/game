def update(self):
    self.rect.x += self.speed
    self.start += self.speed
    if self.start > 160 or self.start < -100:
        self.speed *= -1
        self.rect.y += 10