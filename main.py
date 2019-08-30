import pygame
import random
import time
pygame.init()
window = pygame.display.set_mode((500,500))
pygame.display.set_caption("The Game")

#Sprites
bg=pygame.image.load('Img/bg.png')
shipSprite = [pygame.image.load('Img/standBy.png'),pygame.image.load('Img/burst1.png'),pygame.image.load('Img/burst2.png')] 
enemySprite = [pygame.image.load('Img/enemy01.png'),pygame.image.load('Img/enemy02.png'),pygame.image.load('Img/enemy03.png')]
projectilesShip = [pygame.image.load('Img/ship_ammo01.png')]
projectilesEnemy = [pygame.image.load('Img/enemy_ammo01.png'),pygame.image.load('Img/enemy_ammo02.png'),pygame.image.load('Img/enemy_ammo03.png')]
#Clock and sounds
clock = pygame.time.Clock()
mainTheme = pygame.mixer.music.load("Sounds/SpaceInvadersMain1.wav")
spacePulse = pygame.mixer.Sound('Sounds/pulse02.wav')
spacePulse.set_volume(0.5)
shipDestroyed = pygame.mixer.Sound('Sounds/shipDestroyed.wav')
enemyDestroyed = pygame.mixer.Sound('Sounds/enemyDestroyed.wav')
#Class
class player(object):
	def __init__(self,x,y,width,height,projectile):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.speed = 5
		self.ammo = 100
		self.shotMode = 1
		self.projectile = projectile
		self.health = 1
		self.healths = 1
		self.visible = True
		# self.mode = 0 #standby, burst1, burst2
		self.hitbox = [self.x+17,self.y +2,31,57]
	def draw(self,window):
		window.blit(shipSprite[0],(self.x,self.y))
		self.hitbox = (self.x + 7,self.y, 50, 57)
		# pygame.draw.rect(window,(255,0,0),self.hitbox,2) #HITBOX
	def change_shotMode(attribute,value):
		ship.shotMode=value
	def hitted(self):
		global score
		if self.health > 1:
			score -= 1
			self.health -= 1
		elif self.healths > 1:
			self.health+=1
			self.healths-=1
		else:
			self.health -= 1
			self.healths -= 1
			ship.visible = False
			shipDestroyed.play()

class projectile(object):
	def __init__(self,x,y,radius,color,speed,typeProjectile,origin):
		self.x= x
		self.y= y
		self.radius = radius
		self.color = color
		self.speed = speed
		self.typeProjectile = typeProjectile
		self.origin = origin
	def draw(self,window):
		window.blit(self.typeProjectile,(self.x,self.y))

def destroyedEnemy():
	global score
	global globalLevel
	score+=1
	globalLevel+=1
	ship.ammo+= score * 2

class enemy(object):
	def __init__(self,x,y,width,height,end,health,speed,typeProjectile,level):
		global globalLevel
		self.x= x
		self.y= y
		self.width = width
		self.height = height
		self.end = end
		self.health = health
		self.speed = speed
		self.projectile = typeProjectile
		self.level = level
		self.munSpeed = level * 0.5
		self.visible=False
		self.path = [self.x,self.end]
		self.walkCount = 0
		self.hitbox = (self.x + 17, self.y + 2,31,57)

	def draw(self,window,enemySprite):
		self.move()
		if self.visible:
			if self.walkCount >= 1:
				self.walkCount= 0
			window.blit(enemySprite,(self.x,self.y))
			self.walkCount+=1
			self.hitbox = (self.x + 7,self.y + 2, 50, 57)
			# pygame.draw.rect(window,(255,0,0), self.hitbox,2) #HITBOX
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
			enemyDestroyed.play()
			self.visible=False
			destroyedEnemy()
def hitbox(character,munition,munitions):
	global shipMunitions
	if munition.y - munition.radius < character.hitbox[1] + character.hitbox[3] and munition.y + munition.radius > character.hitbox[1]:
		if munition.x + munition.radius > character.hitbox[0] and munition.x - munition.radius < character.hitbox[0] + character.hitbox[2]:
			character.hitted()
			munitions.pop(munitions.index(munition))
def enemyShots(enemy,enemyMunitions,shootLoop):
	i=0
	randomNumb = random.randint(1,75)
	if (randomNumb == 2 or shootLoop==3) and enemy.visible==True:
		#									           X                                 Y                  radius   Color          Speed        type      origin
		enemyMunitions.append(projectile(round(enemy.x + enemy.width // 2),round(enemy.y + enemy.height // 2),15,(255,0,255),enemy.munSpeed,enemy.projectile,enemy))
	for enemyMunition in enemyMunitions:
		if enemyMunition.y > 0:
			enemyMunition.y += enemyMunition.speed
		if enemyMunition.y > 500:
			enemyMunitions.pop(enemyMunitions.index(enemyMunition))
		if ship.visible:
			hitbox(ship,enemyMunition,enemyMunitions)
def textoScreen():
	window.blit(bg,(0,0))
	text = font.render("Score: " + str(score),1,(0,0,175))
	ammo = font.render(str(ship.ammo),1,(255,0,0))
	lv = font.render("Nivel: " + str(globalLevel),1,(0,200,0))
	healths = font.render("Vidas: "+str(ship.healths),1,(255,30,0))
	healthPoints = font.render("HP: "+str(ship.health),1,(255,30,0))
	window.blit(text,(10,450))
	window.blit(ammo,(450,476))
	window.blit(lv,(10,475))
	window.blit(healths,(400,450))
	window.blit(healthPoints,(400,430))

#LOOP---------------------------
def redrawGameWindow(shootLoop):
	global globalLevel
	textoScreen()

	if ship.visible == True:
		ship.draw(window)
	for shipMunition in shipMunitions:
		shipMunition.draw(window)
	for enemyMunition in enemyMunitions:
		enemyMunition.draw(window)
	for i in range(0,len(enemies)):
		if enemies[i].level == globalLevel:
			enemies[i].visible = True
			enemies[i].draw(window,enemySprite[i])
		else:
			enemies[i].visible = False
		enemyShots(enemies[i],enemyMunitions,shootLoop)
	pygame.display.update()

#mainloop
globalLevel = 1
font = pygame.font.SysFont('comicsans',30,True)

#              x   y  W  H    Munition
ship = player(225,415,64,60,projectilesShip[0]) 


#			     x y  W  H  END HP/SP   MUNITION        LV
enemies = [enemy(0,25,64,60,450,3,5,projectilesEnemy[0],1),enemy(0,10,64,60,400,5,3,projectilesEnemy[1],2),enemy(0,40,68,64,350,3,5,projectilesEnemy[2],3)]
shipMunitions = []
enemyMunitions = []
score = 0
run = True
shootLoop=0
shot=0
pygame.mixer.music.play(-1,0.0)

#RUN---------------------------------------------------------------------------------------------------------
while run:
	clock.tick(60)
	if shootLoop>0:
		shootLoop+=1
	if shootLoop>1:
		shootLoop=0

	#Events
	for event in pygame.event.get(): #Close program
		#Keyboard events
		shotLimit = int(ship.shotMode)
		if ship.ammo<1 or len(shipMunitions)>shotLimit:
			continue
		if event.type == pygame.KEYDOWN and shootLoop == 0:	
			if (event.key == pygame.K_UP or event.key == pygame.K_w):
				ship.ammo-=1 
				spacePulse.play()
				shipMunitions.append(projectile(round(ship.x + ship.width // 2),round(ship.y + ship.height // 2),6,(255,255,255),20,ship.projectile,ship))
			shootLoop=1		
			if event.key == pygame.K_v:
				player.change_shotMode(ship.shotMode,ship.shotMode+1)

		if event.type==pygame.QUIT:
			run=False

	#KEYBOARD PRESSED	
	pressed=pygame.key.get_pressed()	
	if (pressed[pygame.K_LEFT] or pressed[pygame.K_a]) and ship.x >ship.speed:
		ship.x -= ship.speed
	if (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]) and ship.x < 500 - ship.width - ship.speed:
		ship.x += ship.speed
	for shipMunition in shipMunitions:
		if shipMunition.y > 0:
			shipMunition.y -= shipMunition.speed
		else:
			shipMunitions.pop(shipMunitions.index(shipMunition))
		for enemy in enemies:
			if enemy.visible == True:
				hitbox(enemy,shipMunition,shipMunitions)

	redrawGameWindow(shootLoop)

pygame.quit()