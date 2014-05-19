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
	def __init__(self,image,xSize,ySize,xPos,yPos):
		self.image=image
		self.xSize=xSize
		self.ySize=ySize
		self.xPos=xPos
		self.yPos=yPos
		self.angle=angle

class itemType:
	def __init__(self,image,xSize,ySize):
		self.image = image
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
	itemMapper[item[:len(item)-4]] = itemType(pygame.transform.scale(pygame.image.load(item),(xSize*2,ySize*2)).convert(),xSize*2,ySize*2)
	itemMapper[item[:len(item)-4]].image.set_colorkey((255,255,255,255))
	listOfItems.append(item[:len(item)-4])
os.chdir(os.path.dirname(os.getcwd()))

title=pygame.image.load('chadtechknollmastertitle.png').convert()
titleX,titleY=title.get_size()
titleX,titleY=titleX*4,titleY*4
title = pygame.transform.scale(title,(titleX,titleY))
title.set_colorkey((255,255,255,255))


mainLoop = True
quit = False
mouDown = False
anglin = False

carpetScroll = 0
titleBob = 0
itemSelected = ''

angle = 0

itemsOnSurface=[]

for item in range(random.randint(1,14)):
	xPosition = random.randint(100,900)
	yPosition = random.randint(200,550)
	itsAngle = random.randint(0,359)
	itemsOnSurface.append(itemInstance(itemMapper[listOfItems[random.randint(0,len(listOfItems)-1)]],xPosition,yPosition,itsAngle))

while mainLoop and not quit:

	for yit in range((resolutionX/carpetX)+1):
		for vapp in range((resolutionY/carpetY)+2):
			screen.blit(carpetTile,[(carpetX*yit)+carpetScroll-48,(carpetY*vapp)+carpetScroll-48])
	carpetScroll+=1
	carpetScroll=carpetScroll%48

	screen.blit(knollTable,((resolutionX-tableX)/2,(resolutionY-tableY)/2))
	screen.blit(title,((resolutionX-titleX)/2,100+(8*(math.sin(titleBob/2.)))))
	titleBob+=1

#	for item in itemsOnSurface:
#		blitter(item)

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

	if event.type == pygame.QUIT:
		mainLoop = False

	pygame.display.flip()
	clock.tick(30)

	screen.fill((0,0,0))

pygame.quit()