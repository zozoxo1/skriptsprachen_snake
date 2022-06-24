from SnakeGame import SnakeGame
from enums.PlaygroundTile import PlaygroundTile
import pygame
import sys
from pandas import *

game = SnakeGame(20, 20)
game.playground.setTile(1, 5, PlaygroundTile.SNAKE)
game.playground.setRandomFood()
matrix = game.playground.getPlaygroundMatrix()


pygame.init()
display = pygame.display.set_mode((len(matrix) * 20,
                                   len(matrix[0]) * 20))

clock = pygame.time.Clock()
dt = 0

while True:
    display.fill((255, 255, 255))

    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            # width - height - endwidth - endheight
            if matrix[row][col] == PlaygroundTile.VOID:
                pygame.draw.rect(display, (0, 0, 0), (col * 20 , row*20, col*20 + 20, row*20 + 20))
            elif matrix[row][col] == PlaygroundTile.SNAKE:
                pygame.draw.rect(display, (248, 255, 4), (col * 20, row*20, col*20 + 20, row*20 + 20))
            elif matrix[row][col] == PlaygroundTile.FOOD:
                pygame.draw.rect(display, (255, 4, 21), (col * 20, row*20, col*20 + 20, row*20 + 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                game.player.moveUp()
            if event.key == pygame.K_s:
                game.player.moveDown()
            if event.key == pygame.K_a:
                game.player.moveLeft()
            if event.key == pygame.K_d:
                game.player.moveRight()

    game.player.move()

    pygame.display.update()

    dt = clock.tick(5)
