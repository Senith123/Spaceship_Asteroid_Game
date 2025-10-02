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
            r = math.radians(self.angle + 90)
            self.rect.x += math.cos(r) * self.speed
            self.rect.y -= math.cos(r) * self.speed
        self.image = pygame.transform.rotate(pic2,self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)
ship = Ship(450,450)
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
    pygame.display.update()
