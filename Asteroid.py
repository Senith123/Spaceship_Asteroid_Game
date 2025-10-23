import pygame
import math
import random
import time
pygame.init()
#set dimensions of the screen
width = 900
height = 900
font = pygame.font.SysFont("Agency FB",36)
score = 0
health = 3
text = font.render("Score : " + str(score),True,(255,255,255))
htext = font.render("Health : " + str(health),True,(255,255,255))
screen = pygame.display.set_mode((900,900))
pic1 = pygame.image.load("Space_BG.png")
pic1 = pygame.transform.scale(pic1,(900,900))
pic2 = pygame.image.load("Blue_Spaceship.png")
pic3 = pygame.image.load("small_asteroid.png")
pic4 = pygame.image.load("medium_asteroid.png")
pic5 = pygame.image.load("large_asteroid.png")
pic6 = pygame.image.load("UFO.png")
pic7 = pygame.image.load("Star.png")
shoot = pygame.mixer.Sound("shoot.wav")
banglarge = pygame.mixer.Sound("bangLarge.wav")
bangsmall = pygame.mixer.Sound("bangSmall.wav")
asteroid_images = [pic3,pic4,pic5]
class Ship(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pic2
        self.rect = self.image.get_rect(center = (width/2, height/2))
        self.angle = 0
        self.speed = 6
    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle += 5
        if keys[pygame.K_RIGHT]:
            self.angle -= 5
        if keys[pygame.K_UP]:
            r = math.radians(self.angle + 90)
            self.rect.x += math.cos(r) * self.speed
            self.rect.y -= math.sin(r) * self.speed
        # if keys[pygame.K_DOWN]:
        #     r = math.radians(self.angle - 90)
        #     self.rect.x -= math.cos(r) * self.speed
        #     self.rect.y -= math.sin(r) * self.speed
        self.image = pygame.transform.rotate(pic2,self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)
        if self.rect.right < 0:
            self.rect.left = 900
        if self.rect.left > 900:
            self.rect.right = 0
        if self.rect.top < 0:
            self.rect.bottom = 900
        if self.rect.bottom > 900:
            self.rect.top = 0
    def shoot(self, group, all_sprites):
        bullet = Bullet(self.rect.center, self.angle)
        group.add(bullet)
        all_sprites.add(bullet)
        shoot.play()
class Bullet (pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = pygame.Surface((4,4))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect(center = pos)
        rad = math.radians(angle + 90)
        self.vx = math.cos(rad) * 30
        self.vy = -math.sin(rad) * 30
    def update(self, *_):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if not screen.get_rect().colliderect(self.rect):
            self.kill()
class Asteroids (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rank = random.randint(0,2)
        self.image = asteroid_images[self.rank]
        self.rect = self.image.get_rect(center = (random.choice([-90,850,90,50,100,800,750,150,900,200]), random.choice([-90,850,90,50,100,800,750,150,900,200])))
        self.vx = random.randint(-5,5)
        self.vy = random.randint(-5,5)
    def update(self, *_):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if not screen.get_rect().colliderect(self.rect):
            self.kill()

ship = Ship(450,450)
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(ship)
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)
    screen.fill("Blue")
    screen.blit(pic1,(0,0))
    text = font.render("Score : " + str(score),True,(255,255,255))
    htext = font.render("Health : " + str(health),True,(255,255,255))
    screen.blit(text,(50,50))
    screen.blit(htext,(725,50))
    if random.randint(1,60) == 1:
        a = Asteroids()
        asteroids.add(a)
        all_sprites.add(a)
    keys = pygame.key.get_pressed()
    hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
    #if pygame.sprite.groupcollide(bullets, asteroids, True, True):
    for items in hits:
        bangsmall.play()
        print(items.rank)
        if items.rank == 0:
            score = score + 10
        if items.rank == 1:
            score = score + 20
        if items.rank == 2:
            score = score + 30
    #score += len(hits) * 10
    if pygame.sprite.spritecollide(ship, asteroids, True):
        banglarge.play()
        health -= 1 
    if health <= 0:
        rwt=font.render("Game Over! You Scored " + str(score),True,(255,0,0))
        screen.blit(rwt,(300,400))
        pygame.display.update()
        time.sleep(5)
        break
    all_sprites.update(keys)
    all_sprites.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            ship.shoot(bullets, all_sprites)
    pygame.display.update()
