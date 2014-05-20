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

def itemBlitter(what):
	global screen
	placee=pygame.transform.rotate(what.itemType.image,what.angle).convert()
	placeeX,placeeY = placee.get_size()
	screen.blit(placee,[what.xPos-(placeeX/2),what.yPos-(placeeY/2)])

def supercoolText(inputString,where):
	whereX,whereY = where
	global screen
	screen.blit(ctCambridge.render(inputString,False,(24,13,170)),[whereX+8,whereY])
	screen.blit(ctCambridge.render(inputString,False,(24,13,170)),[whereX-8,whereY])
	screen.blit(ctCambridge.render(inputString,False,(24,13,170)),[whereX,whereY+8])
	screen.blit(ctCambridge.render(inputString,False,(24,13,170)),[whereX,whereY-8])
	screen.blit(ctCambridge.render(inputString,False,(24,13,170)),[whereX+4,whereY+4])
	screen.blit(ctCambridge.render(inputString,False,(24,13,170)),[whereX-4,whereY+4])
	screen.blit(ctCambridge.render(inputString,False,(24,13,170)),[whereX+4,whereY-4])
	screen.blit(ctCambridge.render(inputString,False,(24,13,170)),[whereX-4,whereY-4])


	screen.blit(ctCambridge.render(inputString,False,(63,72,204)),[whereX+4,whereY])
	screen.blit(ctCambridge.render(inputString,False,(63,72,204)),[whereX-4,whereY])
	screen.blit(ctCambridge.render(inputString,False,(63,72,204)),[whereX,whereY-4])
	screen.blit(ctCambridge.render(inputString,False,(63,72,204)),[whereX,whereY+4])

	screen.blit(ctCambridge.render(inputString,False,(191,240,234)),[whereX,whereY])

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
bob = 0
itemSelected = ''
scoreTrigger = False

itemsOnSurface=[]

timer = 500

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

	for item in itemsOnSurface:
		itemBlitter(item)

	supercoolText('CHADTECH:KNOLLMASTER',(20,20+(8*math.sin(bob/4.))))
	supercoolText('Time:'+str(timer),(20,93+(8*math.sin(bob/4.))))
	if scoreTrigger:
		supercoolText('Score:'+str(angleAve)[:6]+'%',(20,166+(8*math.sin(bob/4.))))
	bob+=1

	if not timer<1:
		timer-=1
	else:
		if not scoreTrigger:
			angleAve=0
			for item in itemsOnSurface:
				angleAve+=math.fabs(item.angle)
			angleAve=float(angleAve)/float(len(itemsOnSurface))
			angleAve=(180.-angleAve)/180.
			angleAve=angleAve**(100)
			angleAve=100.*angleAve

			penaltyCou=0
			for item in itemsOnSurface:


			scoreTrigger = True



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