import pygame
import random
import math
pygame.init()

win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Board Collection")
my_image = pygame.image.load('ghiasi.png').convert()
smaller = pygame.transform.scale(my_image, (100, 125))
board = pygame.image.load('CC3200.png').convert()
smallr = pygame.transform.scale(board, (50, 50))
gary = pygame.image.load('gary.png').convert()
small = pygame.transform.scale(gary, (100, 100))
heart = pygame.image.load('heart.png').convert()
heart = pygame.transform.scale(heart, (40, 40))

title = pygame.image.load('title.png').convert()
# defining a font
smallfont = pygame.font.SysFont('Corbel', 35)
text = smallfont.render('quit', True, (255, 0, 0))
x = 100
y = 100
baddyX = 300
baddyY = 300
vel = 6
baddyVel = 2

ctr = 0
# stores the width of the
# screen into a variable
width = win.get_width()

# stores the height of the
# screen into a variable
height = win.get_height()

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 25)

maxHP = 100

health = maxHP


def score():
    text = font.render("Boards Collected: "+str(ctr), True, (255, 255, 255))
    win.blit(text, (0, 0))
    text = font.render("Health: "+str(health), True, (255, 255, 255))
    # top right of screen
    win.blit(text, (1280-text.get_width(), 0))


def draw_game():
    win.fill((0, 0, 0))
    win.blit(smaller, (x, y))
    win.blit(smallr, boardCoor)
    score()
    # draw a floating health bar
    #win.blit(small, (1280-baddyX, 720-baddyY))
    #pygame.draw.rect(win, (255, 0, 0), (baddyX, baddyY, 40, 40))


def randomBox():
    return (random.randint(0, 1000), random.randint(0, 600))


def generateBoard():
    win.blit(smallr, randomBox())


def checkCollision(x, y, size1, boardX, boardY, size2):
    if x + size1[0] > boardX and x < boardX + size2[0] and y + size1[1] > boardY and y < boardY + size2[1]:
        return True
    return False


boardCoor = randomBox()

playing = True


class Gary:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.i = random.randint(0, 50)
        self.health = 100

    def update(self):
        if(self.health <= 0):
            garys.remove(self)
        self.i += 1
        if(self.i == 100):
            self.i = random.randint(0, 50)
            norm = math.sqrt((self.x-x)**2 + (self.y-y)**2)
            vector = ((x-self.x)/norm*10, (y-self.y)/norm*10)
            bullet = Bullet(self.x+100/2, self.y+100/2, vector, "baddy")
            bullets.append(bullet)
        if self.x < x - 110:
            self.x = self.x + baddyVel

        elif self.x > x + 110:
            self.x = self.x - baddyVel

        elif self.y < y - 110:
            self.y = self.y + baddyVel

        elif self.y > y + 110:
            self.y = self.y - baddyVel
        else:
            pass

    def draw(self):
        win.blit(small, (self.x, self.y))
        # display health bar under gary
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y+100, 100, 10))
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.y +
                         100, 100*(self.health/100), 10))


class Heart:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        win.blit(heart, (self.x, self.y))

    def update(self):
        # chek collision with sohail
        if checkCollision(self.x, self.y, heart.get_size(), x, y, smaller.get_size()):
            global health
            health += 10
            hearts.remove(self)


class Bullet:
    def __init__(self, x, y, vel, owner):
        self.owner = owner
        self.x = x
        self.y = y
        self.vel = vel

    def draw(self):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, 10, 10))

    def update(self):
        global x, y, baddyX, baddyY
        self.x += self.vel[0]
        self.y += self.vel[1]
        if self.x > width or self.x < 0 or self.y > height or self.y < 0:
            if(self.owner == "sohail"):
                sohailBullets.remove(self)
            elif(self.owner == "baddy"):
                bullets.remove(self)
            print("removed")
        # check if bullet is in
        # check for collision with baddy or player
        for gary in garys:
            if checkCollision(self.x, self.y, (10, 10), gary.x, gary.y, (100, 100)):
                # delete bullet
                if(self.owner == "sohail"):
                    sohailBullets.remove(self)
                    gary.health -= 10
                    break
                    print("collision")
        if checkCollision(self.x, self.y, (10, 10), x, y, (100, 125)):
            # delete bullet
            if(self.owner == "baddy"):
                global health
                health -= 5
                global hearts
                # 5% chance of generating a heart
                if(random.randint(0, 100) <= 5):
                    if(len(hearts) < 5):
                        hearts.append(Heart(random.randint(0, width),
                                            random.randint(0, height)))
                bullets.remove(self)
                print("collision with sohail")
                if(health <= 0):
                    print("game over")
                    global page
                    page = "mainMenu"
                    init()


bullets = []
sohailBullets = []

hearts = []

garys = []


def init():
    global garys, bullets, sohailBullets, hearts
    hearts = []
    garys = []
    bullets = []
    sohailBullets = []
    for i in range(0, 5):
        garys.append(Gary(random.randint(0, width), random.randint(0, height)))
    global health
    health = maxHP
    global ctr
    ctr = 0


init()

page = "mainMenu"

run = True

counter = 0


def mainGame():
    global page, run
    global ctr, boardCoor, baddyX, baddyY, vel, baddyVel, x, y, width, height, win
    global counter
    counter += 1
    if(counter == 500):
        counter = 0
        if(len(garys) < 5):
            garys.append(Gary(random.randint(0, width),
                         random.randint(0, height)))
    clock.tick(60)
    mouse = pygame.mouse.get_pos()
    pygame.time.delay(50)
    if checkCollision(x, y, (100, 125), boardCoor[0], boardCoor[1], (50, 50)):
        boardCoor = randomBox()
        ctr = ctr + 1
        print(ctr)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            norm = math.sqrt((mouse[0]-x)**2 + (mouse[1]-y)**2)
            vector = (-(x-mouse[0])/norm*20, -(y-mouse[1])/norm*20)
            bullet = Bullet(x+100/2, y+125/2, vector, "sohail")
            if len(sohailBullets) < 2:
                sohailBullets.append(bullet)
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
    for gary in garys:
        gary.update()
        gary.draw()
    for bullet in bullets:
        bullet.update()
        bullet.draw()
    for bullet in sohailBullets:
        bullet.update()
        bullet.draw()
    for heart in hearts:
        heart.update()
        heart.draw()
    pygame.display.update()


def mainMenu():
    global page, run
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
                # mainGame()
                page = "game"
            if width/2 - 140 <= mouse[0] <= width/2 - 140 + 280 and height/2 + 100 <= mouse[1] <= height/2 + 100 + 40:
                run = False


while run:
    if(page == "mainMenu"):
        mainMenu()
    elif(page == "game"):
        mainGame()
mainMenu()
