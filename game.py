from turtle import screensize
import pygame
import random
import math
pygame.init()

win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Board Collection")
my_image = pygame.image.load('game/assets/ghiasi.png').convert_alpha()
smaller = pygame.transform.scale(
    my_image, (my_image.get_width()/4, my_image.get_height()/4))
board = pygame.image.load('game/assets/CC3200.png').convert_alpha()
# scale the width to 50%
board = pygame.transform.scale(
    board, (board.get_width()/4, board.get_height()/4))
gary = pygame.image.load('game/assets/gary.png').convert_alpha()
small = pygame.transform.scale(gary, (gary.get_width()/4, gary.get_height()/4))
heart = pygame.image.load('game/assets/heart.png').convert_alpha()
heart = pygame.transform.scale(heart, (40, 40))

title = pygame.image.load('game/assets/title.png').convert_alpha()
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


def randomBox():
    return (random.randint(0, 1000), random.randint(0, 600))


def generateBoard():
    win.blit(board, randomBox())


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
        self.health = 200
        self.gary = small

    def shoot(self):
        norm = math.sqrt((self.x-x)**2 + (self.y-y)**2)
        vector = ((x-self.x)/norm*10, (y-self.y)/norm*10)
        bullet = Bullet(self.x+100/2, self.y+100/2, vector, "baddy")
        bullets.append(bullet)

    def die(self):
        garys.remove(self)
        global deaths
        deaths.append(Death(self.x, self.y))

    def update(self):
        if(self.health <= 0):
            self.die()
        self.i += 1
        if(self.i == 100):
            self.i = random.randint(0, 50)
            self.shoot()
        # move gary in the direction of sohail
        if self.x < x - 110:
            self.x = self.x + baddyVel
            self.gary = pygame.transform.flip(small, True, False)

        elif self.x > x + 110:
            self.x = self.x - baddyVel
            self.gary = small

        if self.y < y - 110:
            self.y = self.y + baddyVel

        elif self.y > y + 110:
            self.y = self.y - baddyVel

    def draw(self):

        win.blit(self.gary, (self.x, self.y))
        # display health bar under gary
        pygame.draw.rect(win, (255, 0, 0),
                         (self.x, self.y+small.get_height(), small.get_width(), 10))
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.y +
                         small.get_height(), small.get_width()*(self.health/200), 10))


think = pygame.image.load('game/assets/garythink.png').convert_alpha()
think = pygame.transform.scale(
    think, (think.get_width()/4, think.get_height()/4))

deaths = []


class Death:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.i = 10
        self.death = think.copy()

    def draw(self):
        self.i -= 1
        # change opacity of death image
        self.death.fill((255, 255, 255, 255*self.i/10),
                        None, pygame.BLEND_RGBA_MULT)
        win.blit(self.death, (self.x, self.y))
        if(self.i <= 0):
            deaths.remove(self)


class Heart:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        win.blit(heart, (self.x, self.y))

    def update(self):
        # chek collision with sohail
        global x, y
        if checkCollision(self.x, self.y, heart.get_size(), x, y, smaller.get_size()):
            global health
            health += 10
            hearts.remove(self)


pow = pygame.image.load('game/assets/pow.png').convert_alpha()
pow = pygame.transform.scale(pow, (40, 40))


class Pow:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        win.blit(pow, (self.x, self.y))

    def update(self):
        global x, y
        # chek collision with sohail
        if checkCollision(self.x, self.y, pow.get_size(), x, y, smaller.get_size()):
            for gary in garys:
                gary.die()
            hearts.remove(self)


gun = pygame.image.load('game/assets/gun.png').convert_alpha()
gun = pygame.transform.scale(gun, (gun.get_width()/8, gun.get_height()/8))


class Bandook:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        win.blit(gun, (self.x, self.y))

    def update(self):
        global x, y
        # chek collision with sohail
        if checkCollision(self.x, self.y, gun.get_size(), x, y, smaller.get_size()):
            for i in range(0, 360, 10):
                bullet = Bullet(x+100/2, y+125/2,
                                (math.cos(math.radians(i))*20, math.sin(math.radians(i))*20), "sohail")
                sohailBullets.append(bullet)
            hearts.remove(self)


pew = pygame.image.load('game/assets/bullet.png').convert_alpha()
pew = pygame.transform.scale(pew, (pew.get_width()/8, pew.get_height()/8))


class Bullet:
    def __init__(self, x, y, vel, owner):
        self.owner = owner
        self.x = x
        self.y = y
        self.vel = vel
        # set direction of bullet to velocity
        self.pew = pygame.transform.rotate(
            pew, 180-math.degrees(math.atan2(self.vel[1], self.vel[0])))

    def draw(self):
        # draw pew with angle in direction of velocity
        win.blit(self.pew, (self.x, self.y))
        # pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, 10, 10))

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
            if checkCollision(self.x, self.y, (10, 10), gary.x, gary.y, (small.get_width(), small.get_height())):
                # delete bullet
                if(self.owner == "sohail"):
                    sohailBullets.remove(self)
                    gary.health -= 10
                    break
        if checkCollision(self.x, self.y, (10, 10), x, y, (smaller.get_width(), smaller.get_height())):
            # delete bullet
            if(self.owner == "baddy"):
                global health
                health -= 5
                global hearts
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


def generatePowerups():
    if(len(hearts) <= 7):
        if(random.randint(0, 100) <= 2):
            hearts.append(Heart(random.randint(0, width),
                                random.randint(0, height)))
        if(random.randint(0, 200) <= 1):
            hearts.append(Pow(random.randint(0, width),
                              random.randint(0, height)))

        if(random.randint(0, 100) <= 5):
            hearts.append(Bandook(random.randint(0, width),
                                  random.randint(0, height)))


reloadSpeed = 0


def mainGame():
    global page, run
    global ctr, boardCoor, baddyX, baddyY, vel, baddyVel, x, y, width, height, win
    global counter, reloadSpeed
    counter += 1
    if(counter == 200):
        counter = random.randint(0, 200*len(garys)/10)
        garys.append(Gary(random.randint(0, width),
                          random.randint(0, height)))
    clock.tick(60)
    mouse = pygame.mouse.get_pos()
    pygame.time.delay(50)
    if checkCollision(x, y, smaller.get_size(), boardCoor[0], boardCoor[1], board.get_size()):
        boardCoor = randomBox()
        ctr = ctr + 1
        print(ctr)
    reloadSpeed -= 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 5% chance of generating a heart
            generatePowerups()
            if(reloadSpeed <= 0):
                reloadSpeed = 4
                norm = math.sqrt((mouse[0]-x)**2 + (mouse[1]-y)**2)
                vector = (-(x-mouse[0])/norm*20, -(y-mouse[1])/norm*20)
                bullet = Bullet(x+100/2, y+125/2, vector, "sohail")
                # if len(sohailBullets) < 2:
                sohailBullets.append(bullet)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x -= vel
        if (x <= 0):
            x = 0
        if (x >= 1155):
            x = 1155
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x += vel
        if (x <= 0):
            x = 0
        if (x >= 1155):
            x = 1155
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        y -= vel
        if (y <= 0):
            y = 0
        if (y >= 620):
            y = 620
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        y += vel
        if (y <= 0):
            y = 0
        if (y >= 620):
            y = 620
    win.set_clip(None)
    win.fill(0)
    areaRadius = 400
    areaTopleft = (x+100/2-areaRadius, y+125/2-areaRadius)
    clipRect = pygame.Rect(areaTopleft, (areaRadius*2, areaRadius*2))
    win.set_clip(clipRect)
    win.blit(board, boardCoor)

    for gary in garys:
        gary.update()
        gary.draw()
    b = bullets.copy()
    for bullet in b:
        bullet.update()
        bullet.draw()
    b = sohailBullets.copy()
    for bullet in b:
        bullet.update()
        bullet.draw()
    h = hearts.copy()
    for heart in h:
        heart.update()
        heart.draw()

    for death in deaths:
        death.draw()

    screensize = (areaRadius*4, areaRadius*4)
    circularArea = pygame.Surface(
        screensize, pygame.SRCALPHA)
    circularArea.fill((0, 0, 0, 255))
    pygame.draw.circle(circularArea, (255, 0, 0, 25),
                       (areaRadius, areaRadius), areaRadius)
    win.blit(circularArea, areaTopleft)
    win.set_clip(None)
    win.blit(smaller, (x, y))
    score()
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
