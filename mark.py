import pygame

pygame.display.set_mode((800, 600))
pygame.init()
dot = pygame.image.load('img/dot.png').convert_alpha()


class Mark(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = dot
        self.rect = self.image.get_rect(center=(x, y))
