import pygame as pg
from scripts.config import *

class Inventario:
	def __init__(self, spriteManager):
		self.spriteManager = spriteManager
		self.slots = [[None for x in range(10)] for y in range(9)]
		self.aberto = False
#		self.slotIMG = 
	
	def toggle(self):
		self.aberto = not self.aberto
		
	def show(self, display):
		if not self.aberto:	return
		img = self.spriteManager.load("spritesheets/ui", (14, 0, 2, 2))
		for y in range(9):
			for x in range(10):
				display.blit(img, (48+x*16, y*16))