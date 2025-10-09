import pygame
import math
pygame.init()
#set dimensions of the screen
width = 900
height = 900
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
            r = math.radians(self.angle - 90)
            self.rect.x += math.cos(r) * self.speed
            self.rect.y += math.sin(r) * self.speed
        if keys[pygame.K_DOWN]:
            r = math.radians(self.angle - 90)
            self.rect.x -= math.cos(r) * self.speed
            self.rect.y -= math.sin(r) * self.speed
        self.image = pygame.transform.rotate(pic2,self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)
        if self.rect.right < 100:
            self.rect.right = 100
        if self.rect.left > 800:
            self.rect.left = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 900:
            self.rect.bottom = 900
    def shoot(self, group, all_sprites):
        bullet = Bullet(self.rect.center, self.angle - 90)
        group.add(bullet)
        all_sprites.add(bullet)
        shoot.play()
class Bullet (pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = pygame.Surface((4,4))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect(center = pos)
        rad = math.radians(angle)
        self.vx = math.cos(rad) * 10
        self.vy = math.sin(rad) * 10
    def update(self, *_):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if not screen.get_rect().colliderect(self.rect):
            self.kill()
ship = Ship(450,450)
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(ship)
run = True
while run:
    screen.fill("Blue")
    screen.blit(pic1,(0,0))
    keys = pygame.key.get_pressed()
    all_sprites.update(keys)
    all_sprites.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            ship.shoot(bullets, all_sprites)
    pygame.display.update()
