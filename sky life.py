import pygame
from pygame import *
import random

WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = pygame.Color('pink')
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "red"
MOVE_SPEED = 15
WIDTH = 22
HEIGHT = 32
COLOR = "#888888"
JUMP_POWER = 10
GRAVITY = 0.35


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xgo = 0  # начальная скорость 0
        self.startX = x
        self.startY = y
        self.ygo = 0
        self.onGround = False
        self.win = False
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.image.set_colorkey(Color(COLOR))

        self.image = image.load("unicorn2.png")
        self.image = pygame.transform.scale(self.image, (22, 32))
        self.startX = x
        self.startY = y
        self.win = False

    def update(self, left, right, up, platforms):

        if up:
            if self.onGround:
                self.ygo = -JUMP_POWER
            self.image.fill(Color(COLOR))
            self.image = image.load("unicorn2.png")
            self.image = pygame.transform.scale(self.image, (22, 32))

        if left:
            self.xgo = -MOVE_SPEED
            self.image.fill(Color(COLOR))
            self.image = image.load("unicorn3.png")
            self.image = pygame.transform.scale(self.image, (22, 32))

        if right:
            self.xgo = MOVE_SPEED
            self.image.fill(Color(COLOR))
            self.image = image.load("unicorn2.png")
            self.image = pygame.transform.scale(self.image, (22, 32))

        if not (left or right):
            self.xgo = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.image = image.load("unicorn2.png")
                self.image = pygame.transform.scale(self.image, (22, 32))

        if not self.onGround:
            self.ygo += GRAVITY

        self.onGround = False
        self.rect.y += self.ygo
        self.collide(0, self.ygo, platforms)

        self.rect.x += self.xgo
        self.collide(self.xgo, 0, platforms)

    def collide(self, xgo, ygo, platforms):
        for i in platforms:
            if sprite.collide_rect(self, i):
                if isinstance(i, Star):
                    self.win = True
                    self.move(self.startX, self.startY)
                elif isinstance(i, Bomb) or isinstance(i, Dark):
                    self.move(self.startX, self.startY)
                else:
                    if xgo > 0:
                        self.rect.right = i.rect.left

                    if xgo < 0:
                        self.rect.left = i.rect.right

                    if ygo > 0:
                        self.rect.bottom = i.rect.top
                        self.onGround = True
                        self.ygo = 0

                    if ygo < 0:
                        self.rect.top = i.rect.bottom
                        self.ygo = 0

    def move(self, teleportx, teleporty):
        self.rect.x = teleportx
        self.rect.y = teleporty


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("cloud.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Star(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("star.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Bomb(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(BACKGROUND_COLOR))
        self.image = image.load("bomb.png")
        self.image = pygame.transform.scale(self.image, (40, 40))

        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Dark(sprite.Sprite):
    def __init__(self, x, y, right):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(BACKGROUND_COLOR))
        self.image = image.load("storm.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = Rect(x, y, 40, 40)
        self.startX = x
        self.startY = y
        self.xgo = right

    def update(self, platforms):
        self.rect.x += self.xgo
        if abs(self.startX - self.rect.x) > 50:
            self.xgo = -self.xgo


def loadLevel():
    num = random.randint(1, 3)
    hero = Player(55, 55)
    if num == 1:
        level = [
            "#########################",
            "#                  ..   #",
            "##         *            #",
            "#                ###    #",
            "#  ###       ##         #",
            "#           .        *  #",
            "#    ##                 #",
            "#   *           #       #",
            "#                       #",
            "# .       #        @    #",
            "#              .        #",
            "#   ###              #  #",
            "#                  #    #",
            "#    ###        .       #",
            "#                       #",
            "#   *             ##    #",
            "#       ##              #",
            "#             .         #",
            "#  *              #     #",
            "#########################"]
        x = 0
        y = 0
        for row in level:
            for col in row:
                if col == '@':
                    star = Star(x, y)
                    entities.add(star)
                    platforms.append(star)
                if col == '.':
                    bomb = Bomb(x, y)
                    entities.add(bomb)
                    platforms.append(bomb)
                if col == '*':
                    dark = Dark(x, y, 4)
                    entities.add(dark)
                    platforms.append(dark)
                    darks.add(dark)

                if col == "#":
                    pf = Platform(x, y)
                    entities.add(pf)
                    platforms.append(pf)

                x += PLATFORM_WIDTH
            y += PLATFORM_HEIGHT
            x = 0


    elif num == 2:
        level = [
            "#########################",
            "#       *          ..   #",
            "##         *            #",
            "#    ##          ###    #",
            "#         ##       .    #",
            "#           .        *  #",
            "#    ##                 #",
            "#   *           #       #",
            "#                  ##   #",
            "# .       #             #",
            "#              .        #",
            "#   ###       #      #  #",
            "#   @              #    #",
            "#    ###        .       #",
            "#                       #",
            "#   *             ##   .#",
            "#       ###             #",
            "#             .         #",
            "#  *              #     #",
            "#########################"]
        x = 0
        y = 0
        for row in level:
            for col in row:
                if col == '@':
                    star = Star(x, y)
                    entities.add(star)
                    platforms.append(star)
                if col == '.':
                    bomb = Bomb(x, y)
                    entities.add(bomb)
                    platforms.append(bomb)
                if col == '*':
                    dark = Dark(x, y, 4)
                    entities.add(dark)
                    platforms.append(dark)
                    darks.add(dark)

                if col == "#":
                    pf = Platform(x, y)
                    entities.add(pf)
                    platforms.append(pf)

                x += PLATFORM_WIDTH
            y += PLATFORM_HEIGHT
            x = 0
    elif num == 3:
        level = [
            "#########################",
            "#       *          #.   #",
            "##         ..           #",
            "#    ##          ###    #",
            "#         ##       .    #",
            "#           .        *  #",
            "#   ###                 #",
            "#   *           #       #",
            "#                  ##   #",
            "# .       #             #",
            "#              .        #",
            "#   ###       #         #",
            "#         *         #   #",
            "#    ###        .       #",
            "#                       #",
            "#   *             ##   .#",
            "#       ###     #       #",
            "#             .         #",
            "#  .    @          *    #",
            "#########################"]
        x = 0
        y = 0
        for row in level:
            for col in row:
                if col == '@':
                    star = Star(x, y)
                    entities.add(star)
                    platforms.append(star)
                if col == '.':
                    bomb = Bomb(x, y)
                    entities.add(bomb)
                    platforms.append(bomb)
                if col == '*':
                    dark = Dark(x, y, 4)
                    entities.add(dark)
                    platforms.append(dark)
                    darks.add(dark)

                if col == "#":
                    pf = Platform(x, y)
                    entities.add(pf)
                    platforms.append(pf)

                x += PLATFORM_WIDTH
            y += PLATFORM_HEIGHT
            x = 0
    elif num == 4:
        level = [
            "#########################",
            "#       ..          #.  #",
            "##          *           #",
            "#    ###          ###   #",
            "#         ##       .    #",
            "#           .        *  #",
            "#   ###                 #",
            "#   .           #       #",
            "#         *        ##   #",
            "# .       #             #",
            "#              .        #",
            "#   ###       ##        #",
            "#         *         #   #",
            "#    ##         .       #",
            "#                   @   #",
            "#   *     #        ##  .#",
            "#       ###     #       #",
            "#             .         #",
            "#  .     #         *    #",
            "#########################"]
        x = 0
        y = 0
        for row in level:
            for col in row:
                if col == '@':
                    star = Star(x, y)
                    entities.add(star)
                    platforms.append(star)
                if col == '.':
                    bomb = Bomb(x, y)
                    entities.add(bomb)
                    platforms.append(bomb)
                if col == '*':
                    dark = Dark(x, y, 4)
                    entities.add(dark)
                    platforms.append(dark)
                    darks.add(dark)

                if col == "#":
                    pf = Platform(x, y)
                    entities.add(pf)
                    platforms.append(pf)

                x += PLATFORM_WIDTH
            y += PLATFORM_HEIGHT
            x = 0
    hero.update(left, right, up, platforms)
    darks.update(platforms)
    entities.draw(screen)
    pygame.display.update()
    screen.blit(screen1, (0, 0))


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("SKY LIFE")
    screen1 = Surface((WIN_WIDTH, WIN_HEIGHT))

    screen1.fill(Color(BACKGROUND_COLOR))

    hero = Player(55, 55)
    left = right = False
    up = False

    entities = pygame.sprite.Group()
    unicorn = pygame.sprite.Group()
    platforms = []
    darks = pygame.sprite.Group()
    unicorn.add(hero)

    level2 = [
        "#########################",
        "#               *       #",
        "##    ###               #",
        "#                  #    #",
        "#     .      ##         #",
        "#                      .#",
        "#    ##                 #",
        "#           *           #",
        "#                   ##  #",
        "# .                     #",
        "#              .        #",
        "#      ##               #",
        "#                  #    #",
        "#    ######             #",
        "#                       #",
        "#                ##     #",
        "#      ##           ##  #",
        "#             .         #",
        "#  *                 @  #",
        "#########################"]
    timer = pygame.time.Clock()
    Running = True
    x = 0
    y = 0

    for row in level2:
        for col in row:
            if col == '@':
                star = Star(x, y)
                entities.add(star)
                platforms.append(star)
            if col == '.':
                bomb = Bomb(x, y)
                entities.add(bomb)
                platforms.append(bomb)
            if col == '*':
                dark = Dark(x, y, 4)
                entities.add(dark)
                platforms.append(dark)
                darks.add(dark)

            if col == "#":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)

            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0

    while Running:
        timer.tick(60)
        if hero.win:
            mainfont = pygame.font.Font(None, 100)
            screen1.fill(Color(pygame.Color('green')))
            message = mainfont.render("CONGRATULATIONS", True, (255, 0, 0))
            message2 = mainfont.render("LEVEL PASSED ", True, (255, 0, 0))
            message3 = mainfont.render("PRESS ENTER", True, (255, 0, 0))
            message4 = mainfont.render("TO CONTINUE", True, (255, 0, 0))
            screen1.blit(message, (WIN_WIDTH * 0.07, WIN_HEIGHT * 0.35))
            screen1.blit(message2, (WIN_WIDTH * 0.1, WIN_HEIGHT * 0.45))
            screen1.blit(message3, (WIN_WIDTH * 0.1, WIN_HEIGHT * 0.55))
            screen1.blit(message4, (WIN_WIDTH * 0.1, WIN_HEIGHT * 0.75))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN and event.key == K_UP:
                up = True
            if event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            if event.type == KEYDOWN and event.key == K_RIGHT:
                right = True
            if event.type == KEYUP and event.key == K_UP:
                up = False
            if event.type == KEYUP and event.key == K_RIGHT:
                right = False
            if event.type == KEYUP and event.key == K_LEFT:
                left = False
            if event.type == pygame.KEYDOWN:
                if event.key == 13:
                    hero.win = False
                    screen1.fill(Color(pygame.Color('pink')))
                    level2 = []
                    platforms = []
                    darks = pygame.sprite.Group()
                    entities = pygame.sprite.Group()
                    hero.move(hero.startX, hero.startY)
                    loadLevel()

        screen.blit(screen1, (0, 0))

        hero.update(left, right, up, platforms)
        darks.update(platforms)
        entities.draw(screen)
        unicorn.draw(screen)
        pygame.display.update()

pygame.quit()
