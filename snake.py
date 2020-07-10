import sys
import math
import random
import pygame
import tkinter
from tkinter import messagebox

pygame.init()

WIN_HEIGHT = 600
WIN_WIDTH = 800

score = 0

highscore = []

f = open("score.txt").readlines()

for line in f:
    highscore.append(int(line))

if len(highscore) > 0:
    maxV = max(highscore)


win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

pygame.display.set_icon(pygame.image.load("snake.png"))

if len(highscore) == 0:
    pygame.display.set_caption("Snake" + " " * 85 + "High-Score: 0")
elif len(highscore) > 0:
    pygame.display.set_caption("Snake" + " " * 85 + "High-Score: " + str(maxV))

clock = pygame.time.Clock()


squares = []

snake_list = []

snake_length = 1


class Grid:

    def __init__(self, color, x, y, width, height, border_width):
        if color == None and x == None and y == None and width == None and height == None and border_width == None:
            self.color = ""
            self.x = ""
            self.y = ""
            self.width = ""
            self.height = ""
            self.border_width = ""
        else:
            self.color = color
            if x == None and y == None:
                self.x = ""
                self.y = ""
            else:
                self.x = x
                self.y = y
            self.width = width
            self.height = height
            self.border_width = border_width
            self.direction = None

    def append(self):
        for col in range(WIN_WIDTH // 20):
            for row in range(WIN_HEIGHT // 20):
                squares.append([col * 20, row * 20])

    def drawGrid(self):
        for i in range(len(squares)):
            for j in range(len(squares[i]) - 1):
                for k in range(1, len(squares[i])):
                    pygame.draw.rect(win, self.color,
                                     (squares[i][j], squares[i][k], self.width, self.height), self.border_width)
        pygame.display.update()


class Player:

    def __init__(self, color, x, y, x_change, y_change, width, height, border_width):
        self.color = color
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change
        self.width = width
        self.height = height
        self.border_width = border_width
        self.snake_length = snake_length
        self.direction = None
        self.score = score

    def append(self):
        global head
        head = []
        head.append(self.x)
        head.append(self.y)
        snake_list.append(head)
        if len(snake_list) > self.snake_length:
            del snake_list[0]

    def player(self):
        win.fill((0, 0, 0))
        for i in range(len(snake_list)):
            pygame.draw.rect(win, self.color, (snake_list[i][0], snake_list[i][1],
                                               self.width, self.height), self.border_width)
            pygame.draw.rect(win, (0, 0, 0), (snake_list[-1][
                             0] + 3, snake_list[-1][1] + 2, self.width - 15, self.height - 15), self.border_width)
            pygame.draw.rect(win, (0, 0, 0), (snake_list[-1][
                             0] + 12, snake_list[-1][1] + 2, self.width - 15, self.height - 15), self.border_width)
        clock.tick(15)

    def control(self):
        if event.type == pygame.KEYDOWN:
            if self.snake_length == 1:
                if event.key == pygame.K_UP:
                    self.x_change = 0
                    self.y_change = -20
                    self.direction = "Up"
                if event.key == pygame.K_DOWN:
                    self.y_change = +20
                    self.x_change = 0
                    self.direction = "Down"
                if event.key == pygame.K_LEFT:
                    self.x_change = -20
                    self.y_change = 0
                    self.direction = "Left"
                if event.key == pygame.K_RIGHT:
                    self.x_change = +20
                    self.y_change = 0
                    self.direction = "Right"
            else:
                if self.direction == "Left" or self.direction == "Right":
                    if event.key == pygame.K_UP:
                        self.x_change = 0
                        self.y_change = -20
                        self.direction = "Up"
                if self.direction == "Left" or self.direction == "Right":
                    if event.key == pygame.K_DOWN:
                        self.y_change = +20
                        self.x_change = 0
                        self.direction = "Down"
                if self.direction == "Up" or self.direction == "Down":
                    if event.key == pygame.K_LEFT:
                        self.x_change = -20
                        self.y_change = 0
                        self.direction = "Left"
                if self.direction == "Up" or self.direction == "Down":
                    if event.key == pygame.K_RIGHT:
                        self.x_change = +20
                        self.y_change = 0
                        self.direction = "Right"

    def increment(self):
        self.x += self.x_change
        self.y += self.y_change

    def border(self):
        if self.x > 805:
            self.x = 0
        if self.x < -5:
            self.x = 780
        if self.y > 605:
            self.y = 0
        if self.y < -5:
            self.y = 580

    def tail(self):
        if player.x == fruit.x and player.y == fruit.y:
            self.snake_length += 1
            self.score += 1


class Fruit:

    def __init__(self, color, x, y, x_change, y_change, width, height, border_width):
        self.color = color
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change
        self.width = width
        self.height = height
        self.border_width = border_width

    def fruit(self):
        pygame.draw.rect(win, self.color, (self.x, self.y,
                                           self.width, self.height), self.border_width)

    def collision(self):
        if self.x == player.x and self.y == player.y:
            self.x = (random.randint(1, 29) * 20)
            self.y = (random.randint(1, 29) * 20)
            self.color = (random.randint(100, 255), random.randint(
                10, 255), random.randint(0, 255))


append = Grid("", "", "", "", "", "")
grid = Grid((255, 255, 255), "", "", 20, 20, 1)

player = Player((255, 0, 0), random.randint(1, 29) * 20,
                random.randint(1, 29) * 20, 0, 0, 20, 20, 0)

fruit = Fruit((255, 128, 0), random.randint(1, 29) * 20,
              random.randint(1, 29) * 20, 0, 0, 20, 20, 0)

running = True

append.append()


def game_over(snake_list, maxV):
    for x in snake_list[:-1]:
        if x == head:
            tkinter.Tk().wm_withdraw()
            if player.score > maxV:
                messagebox.showinfo(
                    "Game Over!", "Congratulations! You have set the new high score which is " + str(player.score))
            else:
                messagebox.showinfo(
                    "Game Over!", "Your score is " + str(player.score))
            f = open("score.txt", "a")
            f.write("\n" + str(player.score))
            f.close
            pygame.quit()


while running:
    player.append()
    player.player()
    fruit.fruit()
    fruit.collision()
    grid.drawGrid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        player.control()

    player.increment()
    player.border()
    player.tail()
    game_over(snake_list, maxV)
    pygame.display.update()

pygame.quit()
