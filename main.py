import sys
import pygame
from pygame.locals import *
from piece import Piece
from piece import Board
from piece import Mark

pygame.init()

fps = 200
fpsClock = pygame.time.Clock()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Game variables
board = []  # p - pawn, r - rook, n - knight, b - bishop, q - queen, k - king, 0 - white, 1 - black
board_sprite = Board()
all_sprites = pygame.sprite.Group()
selected = 0
dot_places = []
dot_sprites = []


def pos_to_cords(x, y):
    return 176 + 64 * y, 76 + 64 * x


def cords_to_pos(x, y):
    return int((y - 176) / 64)+2, int((x - 76) / 64)-1


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

    if selected != 0:
        dot_sprites.clear()
        for place in dot_places:
            dot_sprites.append(Mark(pos_to_cords(place[0], place[1])[0], pos_to_cords(place[0], place[1])[1]))
        for sprite in dot_sprites:
            all_sprites.add(sprite)

    all_sprites.update()
    all_sprites.draw(screen)


def move(od, do):
    if od != do:
        if board[od[0]][od[1]] != '':
            if board[do[0]][do[1]] == '' or board[do[0]][do[1]].model[1] != board[od[0]][od[1]].model[1]:
                board[do[0]][do[1]] = board[od[0]][od[1]]
                board[od[0]][od[1]] = ''


def show_legal_moves(x, y):
    color = board[x][y].model[1]
    kind = board[x][y].model[0]
    places = []
    if kind == 'p':  # Pawn
        if color == '0':  # White
            if board[x - 1][y] == '':
                places.append((x - 1, y))
                if x == 6 and board[x - 2][y] == '':
                    places.append((x - 2, y))

            if x > 0 and y > 0 and board[x - 1][y - 1] != '' and board[x - 1][y - 1].model[1] == '1':
                places.append((x - 1, y - 1))
            if x > 0 and y < 7 and board[x - 1][y + 1] != '' and board[x - 1][y + 1].model[1] == '1':
                places.append((x - 1, y + 1))
        else:  # Black
            if board[x + 1][y] == '':
                places.append((x + 1, y))
                if x == 1 and board[x + 2][y] == '':
                    places.append((x + 2, y))

            if y > 0 and board[x + 1][y - 1] != '' and board[x + 1][y - 1].model[1] == '0':
                places.append((x + 1, y - 1))
            if y < 7 and board[x + 1][y + 1] != '' and board[x + 1][y + 1].model[1] == '0':
                places.append((x + 1, y + 1))

    elif kind == 'r':  # Rock
        for i in range(x):
            if board[x - i - 1][y] == '':
                places.append((x - i - 1, y))
            else:
                if board[x - i - 1][y].model[1] != board[x][y].model[1]:
                    places.append((x - i - 1, y))
                break
        for i in range(y):
            if board[x][y - i - 1] == '':
                places.append((x, y - i - 1))
            else:
                if board[x][y - i - 1].model[1] != board[x][y].model[1]:
                    places.append((x, y - i - 1))
                break

        for i in range(7 - x):
            if board[x + i + 1][y] == '':
                places.append((x + i + 1, y))
            else:
                if board[x + i + 1][y].model[1] != board[x][y].model[1]:
                    places.append((x + i + 1, y))
                break
        for i in range(7 - y):
            if board[x][y + i + 1] == '':
                places.append((x, y + i + 1))
            else:
                if board[x][y + i + 1].model[1] != board[x][y].model[1]:
                    places.append((x, y + i + 1))
                break

    elif kind == 'n':  # Knight
        # board[x-2][y-1], board[x-2][y+1], board[x-1][y+2], board[x+1][y+2], board[x+2][y+1], board[x+2][y-1], board[x+1][y-2], board[x-1][y-2]
        if x >= 2 and y >= 1:
            if board[x - 2][y - 1] == '' or board[x - 2][y - 1].model[1] != board[x][y].model[1]:
                places.append((x - 2, y - 1))
        if x >= 2 and y <= 6:
            if board[x - 2][y + 1] == '' or board[x - 2][y + 1].model[1] != board[x][y].model[1]:
                places.append((x - 2, y + 1))
        if x >= 1 and y <= 5:
            if board[x - 1][y + 2] == '' or board[x - 1][y + 2].model[1] != board[x][y].model[1]:
                places.append((x - 1, y + 2))
        if x <= 6 and y <= 5:
            if board[x + 1][y + 2] == '' or board[x + 1][y + 2].model[1] != board[x][y].model[1]:
                places.append((x + 1, y + 2))
        if x <= 5 and y <= 6:
            if board[x + 2][y + 1] == '' or board[x + 2][y + 1].model[1] != board[x][y].model[1]:
                places.append((x + 2, y + 1))
        if x <= 5 and y >= 1:
            if board[x + 2][y - 1] == '' or board[x + 2][y - 1].model[1] != board[x][y].model[1]:
                places.append((x + 2, y - 1))
        if x <= 6 and y >= 2:
            if board[x + 1][y - 2] == '' or board[x + 1][y - 2].model[1] != board[x][y].model[1]:
                places.append((x + 1, y - 2))
        if x >= 1 and y >= 2:
            if board[x - 1][y - 2] == '' or board[x - 1][y - 2].model[1] != board[x][y].model[1]:
                places.append((x - 1, y - 2))

    elif kind == 'b':
        for i in range(x):
            if y >= i + 1:
                if board[x - i - 1][y - i - 1] == '':
                    places.append((x - i - 1, y - i - 1))
                else:
                    if board[x - i - 1][y - i - 1].model[1] != board[x][y].model[1]:
                        places.append((x - i - 1, y - i - 1))
                    break
            else:
                break

        for i in range(x):
            if y <= 6 - i:
                if board[x - i - 1][y + i + 1] == '':
                    places.append((x - i - 1, y + i + 1))
                else:
                    if board[x - i - 1][y + i + 1].model[1] != board[x][y].model[1]:
                        places.append((x - i - 1, y + i + 1))
                    break
            else:
                break

        for i in range(7 - x):
            if y >= i + 1:
                if board[x + i + 1][y - i - 1] == '':
                    places.append((x + i + 1, y - i - 1))
                else:
                    if board[x + i + 1][y - i - 1].model[1] != board[x][y].model[1]:
                        places.append((x + i + 1, y - i - 1))
                    break
            else:
                break

        for i in range(7 - x):
            if y <= 6 - i:
                if board[x + i + 1][y + i + 1] == '':
                    places.append((x + i + 1, y + i + 1))
                else:
                    if board[x + i + 1][y + i + 1].model[1] != board[x][y].model[1]:
                        places.append((x + i + 1, y + i + 1))
                    break
            else:
                break

    elif kind == 'q':  # Queen
        for i in range(x):
            if board[x - i - 1][y] == '':
                places.append((x - i - 1, y))
            else:
                if board[x - i - 1][y].model[1] != board[x][y].model[1]:
                    places.append((x - i - 1, y))
                break
        for i in range(y):
            if board[x][y - i - 1] == '':
                places.append((x, y - i - 1))
            else:
                if board[x][y - i - 1].model[1] != board[x][y].model[1]:
                    places.append((x, y - i - 1))
                break

        for i in range(7 - x):
            if board[x + i + 1][y] == '':
                places.append((x + i + 1, y))
            else:
                if board[x + i + 1][y].model[1] != board[x][y].model[1]:
                    places.append((x + i + 1, y))
                break
        for i in range(7 - y):
            if board[x][y + i + 1] == '':
                places.append((x, y + i + 1))
            else:
                if board[x][y + i + 1].model[1] != board[x][y].model[1]:
                    places.append((x, y + i + 1))
                break

        for i in range(x):
            if y >= i + 1:
                if board[x - i - 1][y - i - 1] == '':
                    places.append((x - i - 1, y - i - 1))
                else:
                    if board[x - i - 1][y - i - 1].model[1] != board[x][y].model[1]:
                        places.append((x - i - 1, y - i - 1))
                    break
            else:
                break

        for i in range(x):
            if y <= 6 - i:
                if board[x - i - 1][y + i + 1] == '':
                    places.append((x - i - 1, y + i + 1))
                else:
                    if board[x - i - 1][y + i + 1].model[1] != board[x][y].model[1]:
                        places.append((x - i - 1, y + i + 1))
                    break
            else:
                break

        for i in range(7 - x):
            if y >= i + 1:
                if board[x + i + 1][y - i - 1] == '':
                    places.append((x + i + 1, y - i - 1))
                else:
                    if board[x + i + 1][y - i - 1].model[1] != board[x][y].model[1]:
                        places.append((x + i + 1, y - i - 1))
                    break
            else:
                break

        for i in range(7 - x):
            if y <= 6 - i:
                if board[x + i + 1][y + i + 1] == '':
                    places.append((x + i + 1, y + i + 1))
                else:
                    if board[x + i + 1][y + i + 1].model[1] != board[x][y].model[1]:
                        places.append((x + i + 1, y + i + 1))
                    break
            else:
                break

    elif kind == 'k':  # King
        if x >= 1:
            if board[x-1][y] == '' or board[x-1][y].model[1] != board[x][y].model[1]:
                places.append((x-1, y))
            if y >= 1:
                if board[x-1][y-1] == '' or board[x-1][y-1].model[1] != board[x][y].model[1]:
                    places.append((x-1, y-1))
            if y <= 6:
                if board[x-1][y+1] == '' or board[x-1][y+1].model[1] != board[x][y].model[1]:
                    places.append((x-1, y+1))

        if x <= 6:
            if board[x+1][y] == '' or board[x+1][y].model[1] != board[x][y].model[1]:
                places.append((x+1, y))
            if y >= 1:
                if board[x+1][y-1] == '' or board[x+1][y-1].model[1] != board[x][y].model[1]:
                    places.append((x+1, y-1))
            if y <= 6:
                if board[x+1][y+1] == '' or board[x+1][y+1].model[1] != board[x][y].model[1]:
                    places.append((x+1, y+1))

        if y >= 1:
            if board[x][y-1] == '' or board[x][y-1].model[1] != board[x][y].model[1]:
                places.append((x, y-1))
        if y <= 6:
            if board[x][y+1] == '' or board[x][y+1].model[1] != board[x][y].model[1]:
                places.append((x, y+1))

    return places


resetBoard()
# Game loop.:
while True:
    screen.fill((209, 170, 111))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if selected == 0:
                for i in range(8):
                    for j in range(8):
                        if board[i][j] != '':
                            if board[i][j].rect.collidepoint(x, y):
                                dot_places = show_legal_moves(i, j)
                                if dot_places:
                                    selected = (i, j)

            else:
                for sprite in dot_sprites:
                    if sprite.rect.collidepoint(x, y):
                        move(selected, cords_to_pos(sprite.x, sprite.y))
                        print(sprite.x, sprite.y)
                selected = 0

    # Update.
    draw_board()
    # Draw.

    pygame.display.flip()
    fpsClock.tick(fps)
