import pygame

pygame.display.set_mode((800, 600))
pygame.init()
p0 = pygame.image.load('img/pawn_white.png').convert_alpha()
p1 = pygame.image.load('img/pawn_black.png').convert_alpha()
r0 = pygame.image.load('img/rock_white.png').convert_alpha()
r1 = pygame.image.load('img/rock_black.png').convert_alpha()
n0 = pygame.image.load('img/knight_white.png').convert_alpha()
n1 = pygame.image.load('img/knight_black.png').convert_alpha()
b0 = pygame.image.load('img/bishop_white.png').convert_alpha()
b1 = pygame.image.load('img/bishop_black.png').convert_alpha()
q0 = pygame.image.load('img/queen_white.png').convert_alpha()
q1 = pygame.image.load('img/queen_black.png').convert_alpha()
k0 = pygame.image.load('img/king_white.png').convert_alpha()
k1 = pygame.image.load('img/king_black.png').convert_alpha()


class Piece(pygame.sprite.Sprite):
    def __init__(self, model):
        super().__init__()
        self.model = model
        pygame.sprite.Sprite.__init__(self)
        self.image = p0
        if model == 'p0':
            self.image = p0
        elif model == 'p1':
            self.image = p1
        elif model == 'r0':
            self.image = r0
        elif model == 'r1':
            self.image = r1
        elif model == 'n0':
            self.image = n0
        elif model == 'n1':
            self.image = n1
        elif model == 'b0':
            self.image = b0
        elif model == 'b1':
            self.image = b1
        elif model == 'q0':
            self.image = q0
        elif model == 'q1':
            self.image = q1
        elif model == 'k0':
            self.image = k0
        elif model == 'k1':
            self.image = k1
        self.rect = 0

