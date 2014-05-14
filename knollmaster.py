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
pygame.display.set_caption("Chadtech v5.00 : Knoll Master",)

knollTable = pygame.image.load('tableB.png').convert()

os.chdir(os.path.abspath('items'))

drill0=pygame.image.load('drill0.png').convert()
drill0.set_colorkey((255,255,255,255))

calculator0=pygame.image.load('calculator0.png').convert()
calculator0.set_colorkey((255,255,255,255))

knife0=pygame.image.load('knife0.png').convert()
knife0.set_colorkey((255,255,255,255))

pokeball0=pygame.image.load('pokeball0.png').convert()
pokeball0.set_colorkey((255,255,255,255))

clamp0=pygame.image.load('clamp0.png').convert()
clamp0.set_colorkey((255,255,255,255))

glasses0=pygame.image.load('glasses0.png').convert()
glasses0.set_colorkey((255,255,255,255))

title=pygame.image.load('chadtechnknollmastertitle.png').convert()
title.set_colorkey((255,255,255,255))

os.chdir(os.path.dirname(os.getcwd()))

mainLoop = True
quit = False

angle = 0

while mainLoop and not quit:

	screen.blit(knollTable,[0,0])
	screen.blit(pygame.transform.scale(title,(564,124)),[225,5])
	angle+=1

	drillX, drillY = pygame.transform.rotate(pygame.transform.scale(drill0,(130,130)),angle).get_size()
	screen.blit(pygame.transform.rotate(pygame.transform.scale(drill0,(130,130)),angle),[200-(drillX/2),300-(drillY/2)])

	calcX, calcY = pygame.transform.rotate(pygame.transform.scale(calculator0,(48,88)),angle*2.12).get_size()
	screen.blit(pygame.transform.rotate(pygame.transform.scale(calculator0,(48,88)),angle*2.12),[400-(calcX/2),400-(calcY/2)])

	knifeX, knifeY = pygame.transform.rotate(pygame.transform.scale(knife0,(16,80)),angle*7.13).get_size()
	screen.blit(pygame.transform.rotate(pygame.transform.scale(knife0,(16,80)),angle*7.13),[800-(knifeX/2),400-(knifeY/2)])

	pokeballX, pokeballY = pygame.transform.rotate(pygame.transform.scale(pokeball0,(42,42)),angle*4.53).get_size()
	screen.blit(pygame.transform.rotate(pygame.transform.scale(pokeball0,(42,42)),angle*4.53),[600-(pokeballX/2),500-(pokeballY/2)])

	clampX, clampY = pygame.transform.rotate(pygame.transform.scale(clamp0,(58,206)),angle*0.73).get_size()
	screen.blit(pygame.transform.rotate(pygame.transform.scale(clamp0,(58,206)),angle*0.73),[600-(clampX/2),250-(clampY/2)])

	glassesX, glassesY = pygame.transform.rotate(pygame.transform.scale(glasses0,(96,30)),angle*1.73).get_size()
	screen.blit(pygame.transform.rotate(pygame.transform.scale(glasses0,(96,30)),angle*1.73),[150-(glassesX/2),470-(glassesY/2)])

	#screen.blit(pygame.transform.rotate(theWorld.background,-lander.angle),[(800-worldX),400-worldY])
	for event in pygame.event.get():
		#if event.type == pygame.KEYDOWN:
		#	if event.key == pygame.K_a:

		if event.type == pygame.QUIT:
			mainLoop = False

	pygame.display.flip()
	clock.tick(30)

	screen.fill((0,0,0))

pygame.quit()