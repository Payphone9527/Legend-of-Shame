import pygame
import random
import os

FPS = 60
WIDTH = 500
HEIGHT = 525
RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

#遊戲初始化 & 創建視窗
pygame.init() 
pygame.mixer.init()
screen =  pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("神獸之恥")
clock = pygame.time.Clock()

#載入圖片
background_img = pygame.image.load(os.path.join("img", "grassland.png")).convert()
suicune_img = pygame.image.load(os.path.join("img", "pokemon.png")).convert()
who_img = pygame.image.load(os.path.join("img", "who.png")).convert()
pokemonball_img = pygame.image.load(os.path.join("img", "pokemon_ball.png")).convert()
water_img = pygame.image.load(os.path.join("img", "water.png")).convert()
disk_img = pygame.image.load(os.path.join("img", "disk.png")).convert()
hydro_pump_img = pygame.image.load(os.path.join("img", "hydro_pump.png")).convert()
catch_img = pygame.image.load(os.path.join("img", "catch.png")).convert()
win_img = pygame.image.load(os.path.join("img", "win.png")).convert()
pygame.display.set_icon(suicune_img)

#載入音效
boom_sound = pygame.mixer.Sound(os.path.join("sound", "boom.wav"))
boom_sound.set_volume(0.8)
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.mp3"))
shoot2_sound = pygame.mixer.Sound(os.path.join("sound", "shoot2.mp3"))
suicune_sound = pygame.mixer.Sound(os.path.join("sound", "suicune_sound.wav"))
get_sound = pygame.mixer.Sound(os.path.join("sound", "get.mp3"))
win_sound = pygame.mixer.Sound(os.path.join("sound", "win.mp3"))
lose_sound = pygame.mixer.Sound(os.path.join("sound", "lose.mp3"))
pygame.mixer.music.load(os.path.join("sound", "background.mid"))
pygame.mixer.music.set_volume(0.25)

#分數顯示
font_name = os.path.join("font.ttf")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
#初始畫面
def draw_init():
    screen.blit(who_img, (0,0))
    draw_text(screen, '神獸之恥', 64, WIDTH/2, HEIGHT/8)
    draw_text(screen, '方向鍵↑↓←→操控水君躲避精靈球', 26, WIDTH/2, (HEIGHT/2)-60)
    draw_text(screen, '空白鍵向前發射水槍破壞精靈球', 26, WIDTH/2, (HEIGHT/2)-30)
    draw_text(screen, '破壞1顆精靈球會得到1分', 26, WIDTH/2, HEIGHT/2)
    draw_text(screen, '獲得招式紀錄則能夠在5秒內增幅水槍', 26, WIDTH/2, (HEIGHT/2)+30)
    draw_text(screen, '達成245分即可完成挑戰獲得勝利', 26, WIDTH/2, (HEIGHT/2)+60)
    draw_text(screen, '被精靈球碰到則直接失敗', 26, WIDTH/2, (HEIGHT/2)+90)
    draw_text(screen, '按任意鍵開始遊戲', 18, WIDTH/2, HEIGHT*6/7)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False
#失敗畫面
def draw_lose():
    screen.blit(catch_img, (0,0))
    draw_text(screen, '你有夠爛', 70, WIDTH/2, (HEIGHT/4)-100)
    draw_text(screen, '你就是神獸之恥', 70, WIDTH/2, HEIGHT/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
#失敗畫面2
def draw_lose1():
    screen.blit(catch_img, (0,0))
    draw_text(screen, '還是很爛', 70, WIDTH/2, (HEIGHT/4)-100)
    draw_text(screen, '你還是神獸之恥', 70, WIDTH/2, HEIGHT/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
#失敗畫面3
def draw_lose2():
    screen.blit(catch_img, (0,0))
    draw_text(screen, '可憐哪', 60, WIDTH/2, (HEIGHT/4)-140)
    draw_text(screen, '明明就快贏了', 60, WIDTH/2, (HEIGHT/4)-70)
    draw_text(screen, '你依然是神獸之恥', 60, WIDTH/2, HEIGHT/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
#成功畫面
def draw_win():
    screen.blit(win_img, (0,0))
    draw_text(screen, '你就是傳說中的北風之神！', 40, WIDTH/2, HEIGHT*3/4)
    draw_text(screen, '恭喜你！', 40, WIDTH/2, (HEIGHT*3/4)-50)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
#創建水君(Player)
class Suicune(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(suicune_img,(60,60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.center = (WIDTH/2,400)
        self.water = 1
        self.water_time = 0
    def update(self):
        if self.water > 1 and pygame.time.get_ticks() - self.water_time > 5000:
            self.water -= 1
            self.water_time = pygame.time.get_ticks()

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x = self.rect.x+3
        if key_pressed[pygame.K_LEFT]:
            self.rect.x = self.rect.x-3
        if key_pressed[pygame.K_UP]:
            self.rect.y = self.rect.y-3
        if key_pressed[pygame.K_DOWN]:
            self.rect.y = self.rect.y+3
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0 :
            self.rect.left = 0
        if self.rect.top < 0 :
            self.rect.top = 0
        if self.rect.bottom > HEIGHT :
            self.rect.bottom = HEIGHT
    def shoot(self):
        if self.water == 1:
            water = Water(self.rect.centerx , self.rect.top)
            all_sprites.add(water)
            waters.add(water)
            shoot_sound.play()
        elif self.water >= 2:
            hydro_pump = Hydro_pump(self.rect.centerx , self.rect.top)
            all_sprites.add(hydro_pump)
            waters.add(hydro_pump)
            shoot2_sound.play()
    def waterup(self):
        self.water += 1
        self.water_time = pygame.time.get_ticks()
#創建精靈球(障礙物)
class Ball(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pokemonball_img,(50,32))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 13
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(3,10)
        self.speedx = random.randrange(-3,3)
        self.rot_degree = 2
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0,WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(2,10)
            self.speedx = random.randrange(-3,3)
#創建水槍(發射物)
class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(water_img,(13,60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
#創建水炮(升級版發射物)
class Hydro_pump(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(hydro_pump_img,(30,150))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
#創建招式紀錄(掉落寶物)
class Disk(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = disk_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()
waters = pygame.sprite.Group()
disks = pygame.sprite.Group()
suicune = Suicune()
all_sprites.add(suicune)
for i in range(8):
    ball = Ball()
    all_sprites.add(ball)
    balls.add(ball)
score = 0
pygame.mixer.music.play(-1)
#遊戲迴圈
show_init = True
running = True
show_lose = False
show_lose1 = False
show_lose2 = False
show_win = False
while running:
    if show_init:
        close = draw_init() 
        if close:
            break
        show_init = False
    elif show_lose:
        close = draw_lose()
        if close:
            break
        show_lose = True
    elif show_win:
        close = draw_win()
        if close:
            break
        show_win = True
    elif show_lose1:
        close = draw_lose1()
        if close:
            break
        show_lose1 = True
    elif show_lose2:
        close = draw_lose2()
        if close:
            break
        show_lose2 = True
    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                suicune.shoot()
    #更新遊戲
    all_sprites.update()
    #判斷水槍跟精靈球相撞
    hits = pygame.sprite.groupcollide(balls, waters , True, True)
    for hit in hits:
        boom_sound.play()
        score = score + 1
        ball = Ball()
        all_sprites.add(ball)
        if random.random() > 0.95:
            dis = Disk(hit.rect.center)
            all_sprites.add(dis)
            disks.add(dis)
        balls.add(ball)
    #判斷精靈球跟水君相撞
    hits = pygame.sprite.spritecollide(suicune, balls, True, pygame.sprite.collide_circle)
    if hits:
        if score >= 0 and score <= 99:
            show_init = False
            show_lose = True
        elif score >= 100 and score <= 200:
            show_init = False
            show_lose = False
            show_lose1 = True
        elif score >=201 and score <= 244:
            show_init = False
            show_lose = False
            show_lose1 = False
            show_lose2 = True
        suicune_sound.play()
        pygame.mixer.music.pause()
        lose_sound.play()
    #判斷招式紀錄與水君相撞
    hits = pygame.sprite.spritecollide(suicune, disks, True)
    for hit in hits:
        get_sound.play()
        suicune.waterup()
    #判斷分數達到245分
    if score >= 245:
        show_init = False
        show_lose = False
        show_lose1 = False
        show_lose2 = False
        show_win = True
        pygame.mixer.music.pause()
        win_sound.play()
    #畫面顯示
    screen.blit(background_img, (0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 30, WIDTH/2, 20)
    pygame.display.update()
#關閉遊戲
pygame.quit()