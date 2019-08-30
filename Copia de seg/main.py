import pygame
import random
import time
pygame.init()
window = pygame.display.set_mode((500,500))
pygame.display.set_caption("Asteroids")

#Sprites
bg=pygame.image.load('Img/bg.png')
shipSprite = [pygame.image.load('Img/standBy.png'),pygame.image.load('Img/burst1.png'),pygame.image.load('Img/burst2.png')] 
enemySprite = [pygame.image.load('Img/enemy01.png'),pygame.image.load('Img/enemy02.png'),pygame.image.load('Img/enemy03.png')]
projectiles = [pygame.image.load('Img/ship_ammo01.png'),pygame.image.load('Img/enemy_ammo01.png'),pygame.image.load('Img/enemy_ammo02.png')]
#Clock and sounds
clock = pygame.time.Clock()
spacePulse = pygame.mixer.Sound('Sounds/pulse02.wav')
spacePulse.set_volume(0.5)
#Class
class player(object):
	def __init__(self,x,y,width,height,projectile):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.speed = 5
		self.ammo = 10
		self.shotMode = 1
		self.projectile = projectile
		# self.mode = 0 #standby, burst1, burst2

	def draw(self,window):
		window.blit(shipSprite[0],(self.x,self.y))
	def change_shotMode(attribute,value):
		ship.shotMode=value

class projectile(object):
	def __init__(self,x,y,radius,color,speed,typeProjectile):
		self.x= x
		self.y= y
		self.radius = radius
		self.color = color
		self.speed = speed
		self.typeProjectile = typeProjectile
	def draw(self,window):
		window.blit(self.typeProjectile,(self.x,self.y))

def destroyed():
	global score
	global level
	score+=1
	level+=1
	ship.ammo+= score * 2
	enemy2.visible = True

class enemy(object):
	def __init__(self,x,y,width,height,end,typeProjectile):
		self.x= x
		self.y= y
		self.width = width
		self.height = height
		self.end = end
		self.speed = 5
		self.health = 3
		self.visible = True
		self.path = [self.x,self.end]
		self.walkCount = 0
		self.hitbox = (self.x + 17, self.y + 2,31,57)
		self.projectile = typeProjectile

	def draw(self,window,enemySprite):
		self.move()
		if self.visible:
			if self.walkCount >= 1:
				self.walkCount= 0
			window.blit(enemySprite,(self.x,self.y))
			self.walkCount+=1
			self.hitbox = (self.x + 7,self.y + 2, 50, 57)
			# pygame.draw.rect(window,(255,0,0),self.hitbox,2) HITBOX
	def move(self):
		if self.speed > 0:
			if self.x + self.speed < self.path[1]:
				self.x+=self.speed
			else:
				self.speed *= -1
				self.walkCount = 0
		else:
			if self.x - self.speed > self.path[0]:
				self.x+=self.speed
			else:
				self.speed *= -1
				self.walkCount = 0
	def hitted(self):
		global score
		if self.health > 1:
			self.health -=1
		else:
			self.visible=False
			destroyed()

class enemies(enemy):
	def __init__(self,x,y,width,height,end,level,typeProjectile):
		self.x= x
		self.y= y
		self.width = width
		self.height = height
		self.end = end
		self.speed = 2
		self.path = [self.x,self.end]
		self.walkCount = 0
		self.hitbox = (self.x + 17, self.y + 2,31,57)
		self.health = 1
		self.visible = False
		self.projectile = typeProjectile
# def setTrue(self):
# 	self.visible = True
def hitbox(character,munition,munitions):
	global shipMunitions
	global enemyMunitions
	if munition.y - munition.radius < character.hitbox[1] + character.hitbox[3] and munition.y + munition.radius > character.hitbox[1]:
		if munition.x + munition.radius > character.hitbox[0] and munition.x - munition.radius < character.hitbox[0] + character.hitbox[2]:
			character.hitted()
			munitions.pop(munitions.index(munition))

def enemyShots(enemy,enemyMunitions,shootLoop):
	randomNumb = random.randint(1,75)
	if (randomNumb == 2 or shootLoop==3) and enemy.visible==True:
		enemyMunitions.append(projectile(round(enemy.x + enemy.width // 2),round(enemy.y + enemy.height // 2),15,(255,0,255),10,enemy.projectile))
	for enemyMunition in enemyMunitions:
		if enemyMunition.y > 0:
			enemyMunition.y += enemyMunition.speed

def redrawGameWindow():
	def generate_enemies():
		enemy2.draw(window,enemySprite[1])
	window.blit(bg,(0,0))
	text = font.render("Score: " + str(score),1,(0,0,175))
	window.blit(text,(10,450))
	ammo = font.render(str(ship.ammo),1,(255,0,0))
	window.blit(ammo,(450,476))
	lv = font.render("Nivel: " + str(level),1,(0,200,0))
	window.blit(lv,(10,475))

	ship.draw(window)
	enemy1.draw(window,enemySprite[0]) 
	for shipMunition in shipMunitions:
		shipMunition.draw(window)
	for enemyMunition in enemyMunitions:
		enemyMunition.draw(window)
	if enemy2.visible == True:
		generate_enemies()
	pygame.display.update()

#mainloop
level = 1
font = pygame.font.SysFont('comicsans',30,True)
ship = player(225,415,64,60,projectiles[0]) 
enemy1 = enemy(0,25,64,60,450,projectiles[1])
enemy2 = enemies(0,10,64,60,400,level,projectiles[2])
shipMunitions = []
enemyMunitions = []
score = 0
run = True
shootLoop=0
shot=0
while run:
	clock.tick(60)
	#Colliders:

	if shootLoop>0:
		shootLoop+=1
	if shootLoop>1:
		shootLoop=0


	pressed=pygame.key.get_pressed()

	#Events
	for event in pygame.event.get(): #Close program
		if event.type==pygame.QUIT:
			run=False
		if event.type == pygame.KEYDOWN:	
			#Keyboard events
			if event.key == pygame.K_v:
				player.change_shotMode(ship.shotMode,ship.shotMode+1)
			if (event.key == pygame.K_UP or event.key == pygame.K_w) and shootLoop == 0:
				if ship.ammo<1:
					continue
				shotLimit = int(ship.shotMode)
				if len(shipMunitions) < shotLimit:
					ship.ammo-=1 
					spacePulse.play()
					shipMunitions.append(projectile(round(ship.x + ship.width // 2),round(ship.y + ship.height // 2),6,(255,255,255),20,ship.projectile))
				shootLoop=1			


	for shipMunition in shipMunitions:
		if shipMunition.y > 0:
			shipMunition.y -= shipMunition.speed
		else:
			shipMunitions.pop(shipMunitions.index(shipMunition))
		if enemy1.visible == True:
			hitbox(enemy1,shipMunition,shipMunitions)
		elif enemy2.visible == True:
			hitbox(enemy2,shipMunition,shipMunitions)	
	if enemy1.visible==True:
		enemyShots(enemy1,enemyMunitions,shootLoop)
	if enemy2.visible == True:
		enemyShots(enemy2,enemyMunitions,shootLoop)
	if (pressed[pygame.K_LEFT] or pressed[pygame.K_a]) and ship.x >ship.speed:
		ship.x -= ship.speed
	if (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]) and ship.x < 500 - ship.width - ship.speed:
		ship.x += ship.speed
	redrawGameWindow()

pygame.quit()