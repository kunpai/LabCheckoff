import pygame
import random
pygame.init()

win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Board Collection")
my_image = pygame.image.load('ghiasi.png').convert()
smaller = pygame.transform.scale(my_image, (100, 125))
board = pygame.image.load('CC3200.png').convert()
smallr = pygame.transform.scale(board, (50, 50))
gary = pygame.image.load('gary.png').convert()
small = pygame.transform.scale(gary, (100, 100))

title = pygame.image.load('title.png').convert()
# defining a font
smallfont = pygame.font.SysFont('Corbel', 35)
text = smallfont.render('quit', True, (255, 0, 0))
x = 100
y = 100
baddyX = 300
baddyY = 300
vel = 6
baddyVel = 4
run = True
ctr = 0
# stores the width of the
# screen into a variable
width = win.get_width()

# stores the height of the
# screen into a variable
height = win.get_height()


def score():
    font = pygame.font.SysFont(None, 25)
    text = font.render("Boards Collected: "+str(ctr), True, (255, 255, 255))
    win.blit(text, (0, 0))


def draw_game():
    win.fill((0, 0, 0))
    win.blit(smaller, (x, y))
    win.blit(smallr, boardCoor)
    score()
    win.blit(small, (baddyX, baddyY))
    win.blit(small, (1280-baddyX, 720-baddyY))
    #pygame.draw.rect(win, (255, 0, 0), (baddyX, baddyY, 40, 40))
    pygame.display.update()


def randomBox():
    return (random.randint(0, 1000), random.randint(0, 600))


def generateBoard():
    win.blit(smallr, randomBox())
    pygame.display.update()


def checkCollision(x, y, boardX, boardY):
    ghiasiSize = (100, 125)
    boardSize = (50, 50)
    if x + ghiasiSize[0] > boardX and x < boardX + boardSize[0] and y + ghiasiSize[1] > boardY and y < boardY + boardSize[1]:
        return True
    return False


boardCoor = randomBox()


def mainGame():
    run = True
    global ctr, boardCoor, baddyX, baddyY, vel, baddyVel, x, y, width, height, win
    while run:
        mouse = pygame.mouse.get_pos()
        pygame.time.delay(50)
        if baddyX < x - 110:
            baddyX = baddyX + baddyVel

        elif baddyX > x + 110:
            baddyX = baddyX - baddyVel

        elif baddyY < y - 110:
            baddyY = baddyY + baddyVel

        elif baddyY > y + 110:
            baddyY = baddyY - baddyVel
        else:
            run = False

        if checkCollision(x, y, boardCoor[0], boardCoor[1]):
            boardCoor = randomBox()
            ctr = ctr + 1
            print(ctr)
            # draw_game()
        #   if ctr == 10:
        #       print("You win!")
        #       run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # if the mouse is clicked on the
                # button the game is terminated
                if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
                    run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            x -= vel
            if (x <= 0):
                x = 0
            if (x >= 1155):
                x = 1155

        if keys[pygame.K_RIGHT]:
            x += vel
            if (x <= 0):
                x = 0
            if (x >= 1155):
                x = 1155

        if keys[pygame.K_UP]:
            y -= vel
            if (y <= 0):
                y = 0
            if (y >= 620):
                y = 620

        if keys[pygame.K_DOWN]:
            y += vel
            if (y <= 0):
                y = 0
            if (y >= 620):
                y = 620

        draw_game()

    pygame.quit()


def mainMenu():
    run = True
    while run:
        mouse = pygame.mouse.get_pos()
        win.fill((0, 0, 0))
        # display title in center of screen
        win.blit(title, (width/2 - title.get_width() /
                 2, height/2 - title.get_height()))
        # print Play Game and Quit buttons
        pygame.draw.rect(win, (255, 0, 0), (width/2 -
                         140, height/2 + 40, 280, 40))
        pygame.draw.rect(win, (255, 0, 0), (width/2 -
                         140, height/2 + 100, 280, 40))
        play = smallfont.render('Play', True, (0, 0, 0))
        quit = smallfont.render('Quit', True, (0, 0, 0))
        win.blit(play, (width/2 - play.get_width() /
                        2, height/2 + 40))
        win.blit(quit, (width/2 - quit.get_width() /
                        2, height/2 + 100))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if width/2 - 140 <= mouse[0] <= width/2 - 140 + 280 and height/2 + 40 <= mouse[1] <= height/2 + 40 + 40:
                    mainGame()
                if width/2 - 140 <= mouse[0] <= width/2 - 140 + 280 and height/2 + 100 <= mouse[1] <= height/2 + 100 + 40:
                    run = False


mainMenu()
