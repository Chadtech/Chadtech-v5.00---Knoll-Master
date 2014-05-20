import sys
import pygame
import os
import pygame.midi
import pygame.mixer
import math
import random

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.midi.init()
clock = pygame.time.Clock()

ctCambridge = pygame.font.Font('CtCambridge.ttf',126)

print pygame.display.list_modes()
resolutionX, resolutionY = pygame.display.list_modes()[0]
screen = pygame.display.set_mode((resolutionX,resolutionY),pygame.FULLSCREEN)

pygame.display.set_caption("Chadtech v5.00 : Knollmaster",)

knollTable = pygame.image.load('table.png').convert()
tableX,tableY = knollTable.get_size()
tableX,tableY = tableX*2,tableY*2
knollTable = pygame.transform.scale(knollTable,(tableX,tableY))
knollTable.set_colorkey((255,255,255,255))

carpetTile = pygame.image.load('carpettile0.PNG').convert()
carpetX, carpetY = carpetTile.get_size()

class knollZone:
	def __init__(self,image):
		image=pygame.image.load(image).convert()
		xSize,ySize=image.get_size()
		xSize,ySize=xSize*2,ySize*2
		self.image=pygame.transform.scale(image,(xSize,ySize))
		self.image=image.set_colorkey((255,255,255),255)

		self.image=image
		self.xSize=xSize
		self.ySize=ySize

table0 = knollZone('table.png')
surface=table0

leftBou=(resolutionX-surface.xSize)/2
rightBou=leftBou+surface.xSize

topBou=(resolutionY-surface.ySize)/2
botBou=topBou+surface.ySize

class itemType:
	def __init__(self,image):
		image=pygame.image.load(image).convert()
		xSize,ySize=image.get_size()
		xSize,ySize=xSize*2,ySize*2
		image=pygame.transform.scale(image,(xSize,ySize))
		self.image=image.set_colorkey((255,255,255),255)

		self.image=image
		self.xSize=xSize
		self.ySize=ySize

class itemInstance:
	def __init__(self,itemType,xPos,yPos,angle):
		self.itemType=itemType
		self.xPos=xPos
		self.yPos=yPos
		self.angle=angle

def blitter(what):
	global screen
	placee=pygame.transform.rotate(what.itemType.image,what.angle).convert()
	placeeX,placeeY = placee.get_size()
	screen.blit(placee,[what.xPos-(placeeX/2),what.yPos-(placeeY/2)])

################################
###### Load all the items ######
################################
os.chdir(os.path.abspath('items'))
itemMapper = {}
listOfItems = []
for item in os.listdir(os.getcwd()):
	xSize, ySize = pygame.image.load(item).get_size()
	itemMapper[item[:len(item)-4]] = itemType(item)
	listOfItems.append(item[:len(item)-4])
os.chdir(os.path.dirname(os.getcwd()))

################################
#### 'Chadtech Knollmaster' ####
################################
title=pygame.image.load('chadtechknollmastertitle.png').convert()
titleX,titleY=title.get_size()
titleX,titleY=titleX*4,titleY*4
title = pygame.transform.scale(title,(titleX,titleY))
title.set_colorkey((255,255,255,255))


################################
### Declaring some Variables ###
################################

### While true the game runs
mainLoop = True
quit = False
mouDown = False
jusUp=False
anglin = False

carpetScroll = 0
titleBob = 0
itemSelected = ''

itemsOnSurface=[]

timer = 500




#for item in range(random.randint(1,14)):
#	xPosition = random.randint(leftBou,rightBou)
#	yPosition = random.randint(topBou,botBou)
#	itsAngle = random.randint(0,359)
#	itemsOnSurface.append(itemInstance(itemMapper[listOfItems[random.randint(0,len(listOfItems)-1)]],xPosition,yPosition,itsAngle))

itemsOnSurface.append(itemInstance(itemMapper['drill0'],leftBou+itemMapper['drill0'].xSize,botBou-itemMapper['drill0'].ySize,60))
itemsOnSurface.append(itemInstance(itemMapper['drill0'],itemMapper['drill0'].xSize+leftBou,topBou+itemMapper['drill0'].ySize,66))

itemsOnSurface.append(itemInstance(itemMapper['pokeball0'],itemMapper['pokeball0'].xSize+300+leftBou,topBou+itemMapper['pokeball0'].ySize+27,166))
itemsOnSurface.append(itemInstance(itemMapper['pokeball0'],itemMapper['pokeball0'].xSize+440+leftBou,topBou+itemMapper['pokeball0'].ySize+127,180))

itemsOnSurface.append(itemInstance(itemMapper['clamp0'],itemMapper['clamp0'].xSize+leftBou+700,topBou+itemMapper['clamp0'].ySize+200,315))



while mainLoop and not quit:

	for yit in range((resolutionX/carpetX)+1):
		for vapp in range((resolutionY/carpetY)+2):
			screen.blit(carpetTile,[(carpetX*yit)+carpetScroll-48,(carpetY*vapp)+carpetScroll-48])
	carpetScroll+=1
	carpetScroll=carpetScroll%48

	screen.blit(knollTable,((resolutionX-tableX)/2,(resolutionY-tableY)/2))
	screen.blit(title,((resolutionX-titleX)/2,100+(8*(math.sin(titleBob/2.)))))
	titleBob+=1

	for item in itemsOnSurface:
		blitter(item)

	screen.blit(ctCambridge.render('Time : '+str(timer),False,(0,0,255)),[63,resolutionY-63])

	if not timer<1:
		timer-=1
	else:
		angleAve=0
		for item in itemsOnSurface:
			print item.angle
			angleAve+=math.fabs(item.angle)
		angleAve=float(angleAve)/float(len(itemsOnSurface))
		angleAve=(180.-angleAve)/180.
		angleAve=angleAve**(100)
		angleAve=100.*angleAve

		screen.blit(ctCambridge.render('Score : '+str(angleAve)[:4]+'%',False,(0,0,255)),[367,resolutionY-63])
		screen.blit(ctCambridge.render('Score : '+str(angleAve)[:4]+'%',False,(0,0,255)),[359,resolutionY-63])
		screen.blit(ctCambridge.render('Score : '+str(angleAve)[:4]+'%',False,(0,0,255)),[363,resolutionY-59])
		screen.blit(ctCambridge.render('Score : '+str(angleAve)[:4]+'%',False,(0,0,255)),[363,resolutionY-67])
		screen.blit(ctCambridge.render('Score : '+str(angleAve)[:4]+'%',False,(255,255,255)),[363,resolutionY-63])

	for event in pygame.event.get():

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				mainLoop=False

		if event.type==pygame.MOUSEBUTTONDOWN:
			mouX,mouY = event.pos
			mouDown = True
			itemFound = False
			for item in itemsOnSurface:
				if (item.xPos-(item.itemType.xSize/2))<mouX<(item.xPos+(item.itemType.xSize/2)) and (item.yPos-(item.itemType.xSize/2))<mouY<(item.yPos+(item.itemType.ySize/2)):
					itemFound = True
					itemSelected=item
			if not itemFound:
				itemSelected=''

		if event.type==pygame.MOUSEBUTTONUP:
			mouDown = False
			if type(itemSelected)!=str:
				anglin = True

		if event.type == pygame.QUIT:
			mainLoop=False
			quit=True

	if mouDown:
		if type(itemSelected)!=str:
			mouX,mouY = pygame.mouse.get_pos()
			itemSelected.xPos,itemSelected.yPos = mouX,mouY

	if anglin:
		mouX,mouY = pygame.mouse.get_pos()
		if type(itemSelected)!=str:
			relX = mouX-itemSelected.xPos
			relY = mouY-itemSelected.yPos
			if relY>0:
				itemSelected.angle=(math.degrees(math.atan(float(relX)/float(relY))))+180
			elif 0>relY:
				itemSelected.angle=(math.degrees(math.atan(float(relX)/float(relY))))

	

	pygame.display.flip()
	clock.tick(30)

	screen.fill((0,0,0))

pygame.quit()