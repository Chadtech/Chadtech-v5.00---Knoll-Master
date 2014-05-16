import sys
import pygame
import os
import pygame.midi
import pygame.mixer
import math

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.midi.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1000,750),pygame.RESIZABLE)
pygame.display.set_caption("Chadtech v5.00 : Knollmaster",)

knollTable = pygame.image.load('tableB.png').convert()

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
for item in os.listdir(os.getcwd()):
	xSize, ySize = pygame.image.load(item).get_size()
	itemMapper[item[:len(item)-4]] = itemType(pygame.transform.scale(pygame.image.load(item),(xSize*2,ySize*2)).convert(),xSize*2,ySize*2)
	itemMapper[item[:len(item)-4]].image.set_colorkey((255,255,255,255))
os.chdir(os.path.dirname(os.getcwd()))


#firstDrill = itemInstance(itemMapper['drill0'],400,400,45)



title=pygame.image.load('chadtechknollmastertitle.png').convert()
title.set_colorkey((255,255,255,255))

mainLoop = True
quit = False
mouDown = False
anglin = False

itemSelected = ''

angle = 0

itemsOnSurface=[]

itemsOnSurface.append(itemInstance(itemMapper['drill0'],400,400,45))

while mainLoop and not quit:

	screen.blit(knollTable,[0,0])
	screen.blit(pygame.transform.scale(title,(564,124)),[225,5])
	angle+=1

	for item in itemsOnSurface:
		blitter(item)

	for event in pygame.event.get():
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
				item.angle=(math.degrees(math.atan(float(relX)/float(relY))))+180
			elif 0>relY:
				item.angle=(math.degrees(math.atan(float(relX)/float(relY))))

	if event.type == pygame.QUIT:
		mainLoop = False

	pygame.display.flip()
	clock.tick(30)

	screen.fill((0,0,0))

pygame.quit()