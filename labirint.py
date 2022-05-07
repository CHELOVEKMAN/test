
from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self,picture,x,y,w,h):
        super().__init__()
        self.image = transform.scale(image.load(picture),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player (GameSprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_x_speed,player_y_speed):
        GameSprite.__init__(self, player_image,player_x,player_y,size_x,size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    def update(self):
        self.rect.x += self.x_speed         
        platforms_touched = sprite.spritecollide(self, barriers,False) 
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right,p.rect.left)
        elif self.x_speed < 0 :
            for p in platforms_touched:
                self.rect.left = max(self.rect.left,p.rect.right)


        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self,barriers,False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top,p.rect.bottom)
    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx,self.rect.top,15,20,15)
        bullets.add(bullet)

class Enemy (GameSprite):
    def __init__ (self,player_image,player_x,player_y,size_x,size_y,player_speed):
        GameSprite.__init__(self, player_image,player_x,player_y,size_x,size_y)
        self.speed =player_speed
        self.dir =  1
    def update(self):
        xmin= 50
        xmax = 400

        if self.rect.x >= xmax:
            self.dir -= 1
        if self.rect.x <= xmin:
            self.dir = 1
        self.rect.x += self.dir* self.speed
class Bullet(GameSprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        GameSprite.__init__(self, player_image,player_x,player_y,size_x,size_y)
        self.speed = player_speed
    def update(self):
        
        self.rect.x += self.speed
        if self.rect.x > win_width+20:
            self.kill()

        
                
win_width =700
win_height = 500

window = display.set_mode((win_width, win_height))
back = (0,50,23)
display.set_caption("Первая игра")

wall_1 = GameSprite("platform2_v.png",500,100,90,400)
wall_3 = GameSprite("platform2.png",200,0,90,400)

barriers = sprite.Group()
barriers.add(wall_1)
barriers.add(wall_3)

bullets = sprite.Group()
monsters = sprite.Group()

packman = Player("hero.png",5,100,80,80 ,0, 0)
monster = Enemy("cyborg.png",5,400,80,80,10)

monsters.add(monster)

final = GameSprite("pac-1.png",win_width - 80,win_height - 80,80,80)
finish = False

run = True

while run:
   
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
        





    if not finish:
        window.fill(back)
        barriers.draw(window)
        packman.reset()
        final.reset()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        packman.update()
        

    
        if sprite.collide_rect(packman, monster):
            finish = True
            img = image.load("game-over_1.png")
            d = img.get_width() // img.get_height()
            window.fill((255,255,255))
            window.blit(transform.scale(img,(win_height * d,win_height)) ,(90, 0))
        if sprite.collide_rect(packman , final):
            finish = True
            img = image.load("thumb.jpg")
            window.fill((255,255,255))
            window.blit(transform.scale(img,(win_width, win_height)), (0,0))            

    
    display.update()
    








