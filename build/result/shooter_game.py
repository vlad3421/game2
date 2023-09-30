
#Создай собственный Шутер!
from random import *
from pygame import *
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (0,255,0))
lose = font1.render('YOU LOSE!', True, (180,0,0))
Reload = font1.render('Reload', True, (180,0,0))
font2  = font.SysFont('Arial', 36)
img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_bullet = "bullet.png"
img_enemy = "ufo.png"
img_aste = "asteroid.png" 
score = 0
lost = 0
max_lost = 3

class GameSprite(sprite.Sprite):
    def __init__(self , player_image, player_x , player_y,size_x,size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
class Game(sprite.Sprite):
    def __init__(self , player_image, player_x , player_y,size_x,size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet,self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)
class Aste(Game):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
                    

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0
            lost += 1
class Enem(Game):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0
            lost += 0
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500

window = display.set_mode((win_width,win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back),(win_width,win_height))
run = True
finish = False
ship = Player(img_hero,5,win_height-100,80,100,10)
monsters = sprite.Group()
astes = sprite.Group()
for i in range(1,2):
    aste = Enem(img_aste,randint(80,win_width - 80), -40, 80, 50,randint(1,5))
    astes.add(aste)
bullets = sprite.Group()
for i in range(1,5):
    monster = Enemy(img_enemy,randint(80,win_width - 80), -40, 80, 50,randint(1,5))
    monsters.add(monster)
bullets = sprite.Group()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    if not finish:
        window.blit(background,(0,0))
        text = font2.render("Счет:" + str(score),1,(255,255,255))
        window.blit(text,(10,20))
        text_lose = font2.render("Пропущено:" + str(lost),1,(255,255,255))
        
        
        window.blit(text_lose,(10,50))
        ship.update()
        astes.update()
        monsters.update()
        bullets.update()
        ship.reset()
        monsters.draw(window)
        astes.draw(window)
        bullets.draw(window)
        if sprite.groupcollide(monsters,bullets,True,True):
            score += 1
            monster = Enemy(img_enemy,randint(80,win_width - 80), -40, 80, 50,randint(1,5))
            monsters.add(monster)
        if sprite.groupcollide(astes,bullets,True,True):
            score += 0
            aste = Enem(img_aste,randint(80,win_width - 80), -40, 80, 50,randint(1,5))
            astes.add(aste)
        if sprite.spritecollide(ship,monsters,False) or lost >= max_lost:
            window.blit(lose,(200,200))
            finish = True
        if sprite.spritecollide(ship,astes,False) or lost >= max_lost:
            window.blit(lose,(200,200))
            finish = True
        if score >= 10:
            window.blit(win,(200,200))
            finish = True

    display.update()

    time.delay(50)