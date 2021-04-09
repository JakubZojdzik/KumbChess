import sys
import pygame
from pygame.locals import *
from piece import Piece
from piece import Board

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Game variables
board = []  # p - pawn, r - rook, n - knight, b - bishop, q - queen, k - king, 0 - white, 1 - black
board_sprite = Board()
all_sprites = pygame.sprite.Group()


def pos_to_cords(x, y):
    return 176 + 64 * y, 76 + 64 * x


def resetBoard():
    global board
    board.clear()
    board = [[], [], [], [], [], [], [], []]
    for i in range(8):
        for j in range(8):
            board[i].append('')

    # Pawns
    for i in range(8):
        board[1][i] = Piece('p1')
        board[6][i] = Piece('p0')

    # Rocks
    board[0][0] = Piece('r1')
    board[0][7] = Piece('r1')
    board[7][0] = Piece('r0')
    board[7][7] = Piece('r0')

    # Knights
    board[0][1] = Piece('n1')
    board[0][6] = Piece('n1')
    board[7][1] = Piece('n0')
    board[7][6] = Piece('n0')

    # Bishops
    board[0][2] = Piece('b1')
    board[0][5] = Piece('b1')
    board[7][2] = Piece('b0')
    board[7][5] = Piece('b0')

    # Queens
    board[0][3] = Piece('q1')
    board[7][3] = Piece('q0')

    # Kings
    board[0][4] = Piece('k1')
    board[7][4] = Piece('k0')


def draw_board():
    global all_sprites
    global board
    all_sprites = pygame.sprite.Group()
    all_sprites.add(board_sprite)
    for i in range(8):
        for j in range(8):
            if board[i][j] != '':
                board[i][j].rect = board[i][j].image.get_rect(center=pos_to_cords(i, j))
                all_sprites.add(board[i][j])

    all_sprites.update()
    all_sprites.draw(screen)


def move(od, do):
    if board[od[0]][od[1]] != '':
        if board[do[0]][do[1]] == '' or board[do[0]][do[1]].model[1] != board[od[0]][od[1]].model[1]:
            board[do[0]][do[1]] = board[od[0]][od[1]]
            board[od[0]][od[1]] = ''


resetBoard()
# Game loop.:
while True:
    screen.fill((209, 170, 111))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update.
    draw_board()
    # Draw.
    all_sprites.draw(screen)
    pygame.display.flip()
    fpsClock.tick(fps)
