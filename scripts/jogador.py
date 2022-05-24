import pygame as pg
import socket, pickle
#from camera import Camera
from scripts.config import *

pg.init()

#pg.display.set_mode((1, 1))
class Jogador():#pg.sprite.Sprite):
	def __init__(self, x, y):
		#self.camera = Camera()
		self.pos = pg.math.Vector2(x*16, 2*16)
		self.posMovendo = pg.math.Vector2(x*16, y*16)
		self.img = pg.image.load("recursos/sprites/jogador.png").convert()
		self.img.set_colorkey((0, 0, 0))
		self.botaoCima = Botao(24, DISPLAY_TAMANHO[1]-55, "mover_cima")
		self.botaoBaixo = Botao(24, DISPLAY_TAMANHO[1]-21, "mover_baixo")
		self.botaoEsquerda = Botao(7, DISPLAY_TAMANHO[1]-38, "mover_esquerda")
		self.botaoDireita = Botao(41, DISPLAY_TAMANHO[1]-38, "mover_direita")
		self.movendo = [False, [0, 0]]
	
	def mover(self, x, y, jogo, continuarMovendo=False):
		if not self.podeMover(x, y, jogo): return
		if self.movendo[0] and not continuarMovendo: return
		self.posMovendo.x = self.pos.x
		self.posMovendo.y = self.pos.y
		self.movendo = [True, [x, y]]
		self.pos.x += x*16
		self.pos.y += y*16
	
	def podeMover(self, x, y, jogo):
		novaPos = pg.math.Vector2(self.pos.x+x*16, self.pos.y+y*16)
		novaPos.x //= 16
		novaPos.y //= 16
		if 0<=novaPos.x<len(jogo.mapaManager.grid[0][0]) and 0<=novaPos.y<len(jogo.mapaManager.grid[0]):

			return jogo.mapaManager.colisoes[int(novaPos.y)][int(novaPos.x)]==65

		return False
	
	def update(self, jogo):
		
		
		if self.botaoCima.pressionado:
			self.mover(0, -1, jogo)
		elif self.botaoBaixo.pressionado:
			self.mover(0, 1, jogo)
		elif self.botaoDireita.pressionado:
			self.mover(1, 0, jogo)
		elif self.botaoEsquerda.pressionado:
			self.mover(-1, 0, jogo)
		
		if self.movendo[0]:
			movendo = True
			#continuarMovendo = False
			self.posMovendo.x += self.movendo[1][0]*2
			self.posMovendo.y += self.movendo[1][1]*2
			
			if self.arrumarPosMovendo():
				self.movendo = [False, [0, 0]]
				self.posMovendo.x = self.pos.x
				self.posMovendo.y = self.pos.y
				if self.emWarp(jogo):
					self.movendo = [False, [0, 0]]
					jogo.mapaManager.entrarWarp(pg.Rect((self.pos.x, self.pos.y, 16, 16)))
					self.pos = pg.math.Vector2(3*16, 8*16)
					self.posMovendo = pg.math.Vector2(3*16, 8*16)
					jogo.camera.pos = pg.math.Vector2(3*16, 8*16)
				return 
			if self.posMovendo.x==self.pos.x and self.posMovendo.y==self.pos.y:
				continuarMovendo = False
				for index, botao in enumerate([self.botaoEsquerda, self.botaoDireita, self.botaoCima, self.botaoBaixo]):
					if [[-1, 0], [1, 0], [0, -1], [0, 1]][index]==self.movendo[1] and botao.pressionado:
						continuarMovendo = True
						break

				if not continuarMovendo:
					if self.emWarp(jogo):
						self.movendo = [False, [0, 0]]
						jogo.mapaManager.entrarWarp(pg.Rect((self.pos.x, self.pos.y, 16, 16)))
						self.pos = pg.math.Vector2(3*16, 8*16)
						self.posMovendo = pg.math.Vector2(3*16, 8*16)
						jogo.camera.pos = pg.math.Vector2(3*16, 8*16)
					movendo = False
					self.movendo = [False, [0, 0]]
					self.posMovendo.x = self.pos.x
					self.posMovendo.y = self.pos.y
				else:
					self.mover(self.movendo[1][0], self.movendo[1][1], jogo, True)
	#				self.posMovendo.x += 1
#			if movendo:

	def emWarp(self, jogo):
		return jogo.mapaManager.emWarp(pg.Rect(self.pos.x, self.pos.y, 16, 16))
					
	def arrumarPosMovendo(self):
		if self.movendo[1][0]==1 and self.posMovendo.x>self.pos.x: return True
		if self.movendo[1][0]==-1 and self.posMovendo.x<self.pos.x: return True
		if self.movendo[1][1]==1 and self.posMovendo.y>self.pos.y: return True
		if self.movendo[1][1]==-1 and self.posMovendo.y<self.pos.y: return True
		
	def show(self, display, camera):
		if not self.movendo[0]:
			pos = self.pos-camera.pos
			pos.x = int(pos.x)
			pos.y = int(pos.y)-2
		else:
			pos = self.posMovendo-camera.pos
			pos.x = int(pos.x)
			pos.y = int(pos.y)-2
		display.blit(self.img, pos)
		
			
	def showUi(self, display):
		self.botaoCima.show(display)
		self.botaoBaixo.show(display)
		self.botaoDireita.show(display)
		self.botaoEsquerda.show(display)
		
class Botao():
	def __init__(self, x, y, img):
		self.img = pg.image.load("recursos/sprites/botoes/"+img+".png").convert()
		self.img.set_colorkey((0, 0, 0))
		self.Rect = pg.Rect((x, y), self.img.get_size())
		self.pressionado = False

	def pressionandoMouse(self, mousePos):
		if self.Rect.collidepoint(mousePos):
			self.pressionado = True
		else:
			self.pressionado = False
	
	def tirandoMouse(self, mousePos):
		if self.Rect.collidepoint(mousePos):
			self.pressionado = False
			
	def show(self, display):
		display.blit(self.img, self.Rect)
#		if self.pressionado:
#			pg.draw.rect(display, (224, 123, 44), self.Rect)