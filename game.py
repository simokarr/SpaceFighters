import pygame, random, os

pygame.init()

buttonColor = pygame.Color(30, 40, 120)
buttonHover = pygame.Color(0, 90, 50)
white = pygame.Color(255, 255, 255)

width = 600
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Samih's Fighters")
clock = pygame.time.Clock()

background_img = pygame.image.load(os.path.join('resources', 'background.png'))
enemy1_img = pygame.image.load(os.path.join('resources', 'enemy_1.png'))
enemy2_img = pygame.image.load(os.path.join('resources', 'enemy_2.png'))
space_img = pygame.image.load(os.path.join('resources', 'spaceship.png'))
shoot_img = pygame.image.load(os.path.join('resources', 'shoot.png'))
explosion_img = pygame.image.load(os.path.join('resources', 'explosion.png'))
background_sound = pygame.mixer.Sound(os.path.join('resources', 'background_sound.ogg'))

# use of list
enemies = []
bullets = []
highScores = []

# use of dictionaries
GameStats = {
    "score": 0,
    "lives": 3
}


# use of class
class Spaceship():
    def __init__(self, pos):
        self.pos = pos
        self.img = space_img

    def Shoot(self):
        x = self.pos[0] + 45
        y = self.pos[1] + 10
        bullets.append(Bullet([x, y]))

    def Draw(self):
        display.blit(self.img, self.pos)

    def Update(self, move):
        if 0 <= self.pos[0] + move <= width - 100:
            self.pos[0] += move


class Bullet(object):
    def __init__(self, pos):
        self.pos = pos
        self.img = shoot_img

    def Draw(self):
        display.blit(self.img, self.pos)

    def Update(self):
        self.pos[1] -= 5


class Enemy():
    def __init__(self, pos, img):
        self.pos = pos
        self.img = img
        self.life = 2

    def Draw(self):
        display.blit(self.img, self.pos)

    def Update(self):
        self.pos[1] += 5


# use of function
def AddText(text, size, pos):
    font = pygame.font.SysFont("comicsansms", size)
    renderedText = font.render(text, True, white)
    display.blit(renderedText, pos)


def QuitGame():
    pygame.quit()
    exit()


def Button(name, x, y):
    pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < pos[0] < x + 100 and y < pos[1] < y + 60:
        pygame.draw.rect(display, buttonHover, [x, y, 100, 60])
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(display, buttonColor, [x, y, 100, 60])
    AddText(name, 20, (x + 30, y + 15))


def IntroMenu():
    display.blit(background_img, (0, 0))
    AddText("Samih's Fighters", 50, (120, 200))
    exit = False
    # loop
    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
        exit = Button("Play", 250, 300)
        pygame.display.update()
        clock.tick(15)
    NewGame()


def DrawElements():
    global enemies, bullets, GameStats, Player
    # loop and search
    for e in enemies:
        e.Draw()
        e.Update()
        if e.pos[1] > height:
            enemies.remove(e)
            continue
        if e.life <= 0:
            display.blit(explosion_img, e.pos)
            enemies.remove(e)
            continue
        if Player.pos[0] + 10 < e.pos[0] + 10 < Player.pos[0] + 90 or Player.pos[0] + 10 < e.pos[0] + 40 < Player.pos[
            0] + 90:
            if e.pos[1] + 40 > Player.pos[1]:
                newlives = GameStats["lives"] - 1
                GameStats["lives"] = newlives
                display.blit(explosion_img, e.pos)
                enemies.remove(e)
    # loop and search
    for b in bullets:
        b.Draw()
        b.Update()
        if b.pos[1] < -10:
            bullets.remove(b)
            continue
        for e in enemies:
            if e.pos[0] < b.pos[0] < e.pos[0] + 45 or e.pos[0] < b.pos[0] + 10 < e.pos[0] + 45:
                if e.pos[1] < b.pos[1] < e.pos[1] + 45:
                    e.life -= 1
                    newScores = GameStats["score"] + 5
                    GameStats["score"] = newScores
                    bullets.remove(b)


# recursion
def AddEnemy(count, pos, style):
    if count > 5:
        return count
    r = random.randrange(0, 100)
    img = enemy1_img
    if r > 50:
        img = enemy2_img
    enemies.append(Enemy(pos, img))
    if style == 'left':
        x = pos[0] - 70
        y = pos[1] - 70
    elif style == 'right':
        x = pos[0] + 70
        y = pos[1] - 70
    else:
        x = pos[0] + 70
        y = pos[1]
    return AddEnemy(count + 1, [x, y], style)


def ScoreAndLives():
    global GameStats
    scoreText = "Score: " + str(GameStats["score"])
    AddText(scoreText, 20, (10, 5))
    livesText = "Lives: " + str(GameStats["lives"])
    AddText(livesText, 20, (500, 5))


# class object
Player = Spaceship([200, 500])


def NewGame():
    background_sound.play(-1)
    background_sound.set_volume(0.1)
    global GameStats
    play = True
    move = 0
    y = -680
    # loop
    while play:
        display.blit(background_img, (0, y))
        y += 1
        if y >= 0:
            y = -680
        # loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move = -5
                if event.key == pygame.K_RIGHT:
                    move = 5
                if event.key == pygame.K_SPACE:
                    Player.Shoot()
            if event.type == pygame.KEYUP:
                move = 0

        Player.Draw()
        if move != 0:
            Player.Update(move)
        DrawElements()
        if len(enemies) == 0:
            r = random.randrange(0, 100)
            if 0 < r < 33:
                style = 'right'
                pos = [100, -5]
            elif 33 < r < 67:
                style = 'left'
                pos = [500, -5]
            else:
                style = 'default'
                pos = [100, -5]
            AddEnemy(0, pos, style)
        ScoreAndLives()
        if GameStats["lives"] < 0:
            play = False
        pygame.display.update()
        clock.tick(20)
    GameOver()


# sorting
def Sort(arr):
    n = len(arr)
    if n < 2:
        return
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j], arr[j]


def GameOver():
    global GameStats, highScores
    display.blit(background_img, (0, 0))
    AddText("Game Over", 50, (120, 100))
    AddText("Your Score: " + str(GameStats["score"]), 50, (100, 200))
    AddText("High Score:", 30, (100, 320))
    # file output
    with open(os.path.join("resources", "score.txt"), "r") as file:
        for line in file:
            num = int(line.rstrip('\n'))
            highScores.append(num)
    if (GameStats["score"] > 0):
        highScores.append(GameStats["score"])
    Sort(highScores)
    i = 0
    pos = [300, 330]
    # file input
    with open(os.path.join("resources", "score.txt"), "w") as file:
        while i < len(highScores):
            if i == 3:
                break
            text = str(i + 1) + ") " + str(highScores[i])
            AddText(text, 25, pos)
            file.write(str(highScores[i]) + '\n')
            pos[1] += 50
            i += 1
    exit = False
    # loop
    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
        exit = Button("Exit", 420, 500)
        pygame.display.update()
        clock.tick(15)
    QuitGame()


if __name__ == '__main__':
    IntroMenu()
