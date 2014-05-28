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
ctCambridge1 = pygame.font.Font('CtCambridge.ttf',252)

resolutionX, resolutionY = pygame.display.list_modes()[0]
screen = pygame.display.set_mode((resolutionX,resolutionY),pygame.FULLSCREEN)

pygame.display.set_caption("Chadtech v5.00 : Knollmaster",)

longlines = pygame.image.load('longlines.PNG').convert()

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

class region:
	def __init__(self,itemType):
		self.lBou=''
		self.rBou=''
		self.tBou=''
		self.bBou=''
		self.itemType=itemType
		self.exists=False

table0 = knollZone('table.png')
surface=table0

leftBou=(resolutionX-surface.xSize)/2
rightBou=leftBou+surface.xSize

topBou=(resolutionY-surface.ySize)/2
botBou=topBou+surface.ySize

class itemType:
	def __init__(self,image):

		self.name=image[:len(image)-4]

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
		self.name=itemType.name
		self.xPos=xPos
		self.yPos=yPos
		self.angle=angle

def itemBlitter(what):
	global screen
	placee=pygame.transform.rotate(what.itemType.image,what.angle).convert()
	placeeX,placeeY = placee.get_size()
	screen.blit(placee,[what.xPos-(placeeX/2),what.yPos-(placeeY/2)])

def supercoolText(inputString,where,double=False):
	whereX,whereY = where
	global screen
	if not double:
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

	else:
		screen.blit(ctCambridge1.render(inputString,False,(24,13,170)),[whereX+16,whereY])
		screen.blit(ctCambridge1.render(inputString,False,(24,13,170)),[whereX-16,whereY])
		screen.blit(ctCambridge1.render(inputString,False,(24,13,170)),[whereX,whereY+16])
		screen.blit(ctCambridge1.render(inputString,False,(24,13,170)),[whereX,whereY-16])
		screen.blit(ctCambridge1.render(inputString,False,(24,13,170)),[whereX+8,whereY+8])
		screen.blit(ctCambridge1.render(inputString,False,(24,13,170)),[whereX-8,whereY+8])
		screen.blit(ctCambridge1.render(inputString,False,(24,13,170)),[whereX+8,whereY-8])
		screen.blit(ctCambridge1.render(inputString,False,(24,13,170)),[whereX-8,whereY-8])

		screen.blit(ctCambridge1.render(inputString,False,(63,72,204)),[whereX+8,whereY])
		screen.blit(ctCambridge1.render(inputString,False,(63,72,204)),[whereX-8,whereY])
		screen.blit(ctCambridge1.render(inputString,False,(63,72,204)),[whereX,whereY-8])
		screen.blit(ctCambridge1.render(inputString,False,(63,72,204)),[whereX,whereY+8])

		screen.blit(ctCambridge1.render(inputString,False,(191,240,234)),[whereX,whereY])


##### Check if regions overlap
##### Regions are quadtuples where (top boundary, right boundary, bottom boundary, left boundary)
##### The function Checks by seeing if two or more of the four boundaries cross each other
def checkForOverlap(regionOn,regionTw):

		tlIn = False
		trIn = False
		brIn = False
		blIn = False

		tOn,rOn,bOn,lOn = regionOn
		tTw,rTw,bTw,lTw = regionTw

		violationCou = 0

		corners=[
			(lOn,tOn),
			(rOn,tOn),
			(rOn,bOn),
			(lOn,bOn)
			]

		return not (bTw<tOn or bOn<tTw or rTw<lOn or rOn<lTw)

################################
###### Load all the items ######
################################
os.chdir(os.path.abspath('items'))
itemMapper = {}
for item in os.listdir(os.getcwd()):
	xSize, ySize = pygame.image.load(item).get_size()
	itemMapper[item[:len(item)-4]] = itemType(item)
	itemMapper[itemType(item)]=item[:len(item)-4]
os.chdir(os.path.dirname(os.getcwd()))

################################
### Declaring some Variables ###
################################

### While true the game runs
mainLoop = True
intro=True
quit = False
mouseDown = False
jusUp=False
anglin = False

carpetScroll = 0
bob = 0
itemSelected = ''
scoreTrigger = False

itemsOnSurface=[]

timer = 500
groupBlink = 0 

################################
##### Load items in level ######
################################

itemsOnSurface.append(itemInstance(itemMapper['drill0'],leftBou+itemMapper['drill0'].xSize,botBou-itemMapper['drill0'].ySize,60))

itemsOnSurface.append(itemInstance(itemMapper['calculator0'],leftBou+itemMapper['calculator0'].xSize+200,botBou-itemMapper['calculator0'].ySize,160))

itemsOnSurface.append(itemInstance(itemMapper['pokeball0'],itemMapper['pokeball0'].xSize+300+leftBou,topBou+itemMapper['pokeball0'].ySize+27,166))
itemsOnSurface.append(itemInstance(itemMapper['pokeball0'],itemMapper['pokeball0'].xSize+440+leftBou,topBou+itemMapper['pokeball0'].ySize+127,180))

itemsOnSurface.append(itemInstance(itemMapper['clamp0'],itemMapper['clamp0'].xSize+leftBou+50,topBou+itemMapper['clamp0'].ySize,66))
itemsOnSurface.append(itemInstance(itemMapper['clamp0'],itemMapper['clamp0'].xSize+leftBou+500,topBou+itemMapper['clamp0'].ySize+200,315))

################################
### Make region for itemtypes ##
################################

itemRegions = {}
itemTypeChecker =[]

for item in itemsOnSurface:
	itemRegions[item.itemType.name]=('','','','')

while intro and not quit:

	screen.fill((73,147,182))
	lx,ly=longlines.get_size()
	screen.blit(longlines,[0,resolutionY-ly])

	supercoolText('CHADTECH :',(resolutionX/2-700,resolutionY/2-400),double=True)
	supercoolText('v5.00 -- KNOLLMASTER',(resolutionX/2-700,resolutionY/2-260),double=True)

	supercoolText('Press Any Key To Start',(resolutionX/2,resolutionY/2))

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			intro=False

	pygame.display.flip()
	clock.tick(30)


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
	supercoolText("Press Q to quit",((resolutionX-485),20+(8*math.sin(bob/4.))))
	if scoreTrigger:
		lineNumber=3
		supercoolText('Penalties : ',(20,73*lineNumber+(8*math.sin(bob/4.))))
		lineNumber+=1
		supercoolText('Out of Bounds = '+str(outOfBoundCou),(93,73*lineNumber+(8*math.sin(bob/4.))))
		lineNumber+=1
		supercoolText('Overlapping = '+str(overlapCou),(93,73*lineNumber+(8*math.sin(bob/4.))))
		lineNumber+=1
		supercoolText('Excess size = '+str(excessSizeCou),(93,73*lineNumber+(8*math.sin(bob/4.))))
		lineNumber+=1
		supercoolText('Total penalties = -'+str(excessSizeCou+overlapCou+outOfBoundCou)+' x 25%',(93,73*lineNumber+(8*math.sin(bob/4.))))
		lineNumber+=1
		supercoolText('                = -'+str(((excessSizeCou)*10)+(overlapCou+outOfBoundCou)*25)+'%',(93,73*lineNumber+(8*math.sin(bob/4.))))
		lineNumber+=1
		supercoolText('Final Score = '+str(angleAve)[:6]+'%',(20,73*lineNumber+(8*math.sin(bob/4.))))
		lineNumber+=1


		if groupBlink<80:
			if ((groupBlink/5)%2) == 1:
				for item in itemsOnSurface:
					t,r,b,l = itemRegions[item.itemType.name]
					pygame.draw.rect(screen, (255,192,192),(l,t,r-l,b-t),4)
					pygame.draw.rect(screen, (255,0,0),(l,t,r-l,b-t),2)
			groupBlink+=1
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

			##### outOfBoundCou is the penalty of exceeding the knoll zone (the table)
			outOfBoundCou=0
			#### overlapCou is the penalty of overlapping item regions
			overlapCou=0
			itemZones = []
			
			##### Define the boundaries for the region
			for item in itemsOnSurface:
				tBou,rBou,bBou,lBou = itemRegions[item.itemType.name]
				if type(tBou)==str or (type(tBou)==int and (item.yPos-(item.itemType.ySize/2))<tBou):
					tBou=item.yPos-(item.itemType.ySize/2)
				if type(rBou)==str or (type(rBou)==int and rBou<(item.xPos+(item.itemType.xSize/2))):
					rBou=item.xPos+(item.itemType.xSize/2)
				if type(bBou)==str or (type(bBou)==int and bBou<(item.yPos+(item.itemType.ySize/2))):
					bBou=item.yPos+(item.itemType.ySize/2)
				if type(lBou)==str or (type(lBou)==int and (item.xPos-(item.itemType.xSize/2))<lBou):
					lBou=item.xPos-(item.itemType.xSize/2)

				itemRegions[item.itemType.name]=(tBou,rBou,bBou,lBou)

			##### See if the region exceeds the boundaries of the table
			for region in itemRegions:
				tBou,rBou,bBou,lBou = itemRegions[region]
				if tBou<topBou:
					outOfBoundCou+=1
				if botBou<bBou:
					outOfBoundCou+=1
				if rightBou<rBou:
					outOfBoundCou+=1
				if lBou<leftBou:
					outOfBoundCou+=1

			##### For every item region on the table, see if it overlaps with the other regions
			overlapCou=0
			setOfItemTypes =set([])
			for item in itemsOnSurface:
				setOfItemTypes.add(item.itemType.name)
			print setOfItemTypes
			for itemType in setOfItemTypes:
				for anotherItemType in setOfItemTypes:
					if itemType!=anotherItemType:
						if checkForOverlap(itemRegions[itemType],itemRegions[anotherItemType]):
							overlapCou+=1
			#### The code double counts every over lap, so I divide it by 2 (region a and b overlapping is a single over lap, but when counting, the code counts a overlapping b, and b overlapping a as distinct)
			overlapCou=overlapCou/2

			##### For every item region on the table, see if its excessively large
			excessSizeCou=0
			setOfItemTypes =set([])
			for item in itemsOnSurface:
				setOfItemTypes.add(item.itemType.name)
			for itemType in setOfItemTypes:
				tSide,rSide,bSide,lSide = itemRegions[itemType]
				regionWidth,regionHeight = rSide-lSide,bSide-tSide
				halfItsPerimeter=regionWidth+regionHeight
				numberOfInstances=0
				for item in itemsOnSurface:
					if item.itemType.name==itemType:
						numberOfInstances+=1

				numberTall=(regionHeight/itemMapper[itemType].ySize)
				numberWide=(regionWidth/itemMapper[itemType].xSize)
				amountCouldFit = numberTall*numberWide
				excessSizeCou+=(amountCouldFit-numberOfInstances)


			angleAve-=excessSizeCou*10
			angleAve-=outOfBoundCou*25
			angleAve-=overlapCou*25

			scoreTrigger = True



	for event in pygame.event.get():

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				mainLoop=False

		##### If they click down
		if event.type==pygame.MOUSEBUTTONDOWN:
			##### Get mouse position
			mouX,mouY = event.pos		
			mouseDown = True
			itemFound = False
			##### Run through every item, and see if you clicked within its boundaries
			for item in itemsOnSurface:
				if (item.xPos-(item.itemType.xSize/2))<mouX<(item.xPos+(item.itemType.xSize/2)) and (item.yPos-(item.itemType.ySize/2))<mouY<(item.yPos+(item.itemType.ySize/2)):
					itemFound = True
					itemSelected=item
			if not itemFound:
				itemSelected=''

		if event.type==pygame.MOUSEBUTTONUP:
			mouX,mouY = event.pos
			mouseDown = False
			if type(itemSelected)!=str:
				if leftBou<mouX-(itemSelected.itemType.xSize/2) and mouX+(itemSelected.itemType.xSize/2)<rightBou and topBou<mouY-(itemSelected.itemType.ySize/2) and mouY+(itemSelected.itemType.ySize/2)<botBou:
					anglin = True
				else:
					mouseDown=True

		if event.type == pygame.QUIT:
			mainLoop=False
			quit=True

	if mouseDown:
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