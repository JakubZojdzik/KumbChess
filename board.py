import pygame

pygame.display.set_mode((800, 600))
pygame.init()
board_img = pygame.image.load('img/board.png').convert_alpha()


class Board(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = board_img
        self.rect = self.image.get_rect(center=(400, 300))
