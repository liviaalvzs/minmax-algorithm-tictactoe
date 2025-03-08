import pygame
import sys
import time

import tictactoe as ttt

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
lilac = (150, 100, 200)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic-Tac-Toe")

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
board = ttt.initial_state()
ai_turn = False

def draw_button(rect, text, hover=False):
    color = (180, 130, 220) if hover else lilac
    pygame.draw.rect(screen, color, rect, border_radius=10)
    label = mediumFont.render(text, True, black)
    label_rect = label.get_rect()
    label_rect.center = rect.center
    screen.blit(label, label_rect)

while True:
    screen.fill(black)
    mouse = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Let user choose a player.
    if user is None:
        title = largeFont.render("Play Tic-Tac-Toe", True, lilac)
        titleRect = title.get_rect(center=(width / 2, 50))
        screen.blit(title, titleRect)

        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        draw_button(playXButton, "Play as X", playXButton.collidepoint(mouse))
        draw_button(playOButton, "Play as O", playOButton.collidepoint(mouse))
        
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

    else:
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size), height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(tile_origin[0] + j * tile_size, tile_origin[1] + i * tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, lilac, rect, 3, border_radius=5)
                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, lilac)
                    moveRect = move.get_rect(center=rect.center)
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        if game_over:
            winner = ttt.winner(board)
            title_text = "Game Over: Tie." if winner is None else f"Game Over: {winner} wins."
        elif user == player:
            title_text = f"Play as {user}"
        else:
            title_text = "Computer thinking..."
        title = largeFont.render(title_text, True, lilac)
        screen.blit(title, title.get_rect(center=(width / 2, 30)))

        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse):
                        board = ttt.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            draw_button(againButton, "Play Again", againButton.collidepoint(mouse))
            if click == 1 and againButton.collidepoint(mouse):
                time.sleep(0.2)
                user = None
                board = ttt.initial_state()
                ai_turn = False

    pygame.display.flip()
