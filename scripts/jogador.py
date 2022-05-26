import pygame as pg
import socket, pickle
from scripts.uiComponentes import Botao
#from camera import Camera
from scripts.config import *

pg.init()

#pg.display.set_mode((1, 1))
class Jogador():#pg.sprite.Sprite):
	def __init__(self, x, y, jogo):
		#self.camera = Camera()
		self.pos = pg.math.Vector2(x*8, y*8)
		self.posMovendo = pg.math.Vector2(x*8, y*8)
		self.img = pg.image.load("recursos/sprites/jogador.png").convert()
		self.img.set_colorkey((0, 0, 0))
		
		self.botaoCima = Botao(16, DISPLAY_TAMANHO_REAL[1]-56)
		self.botaoCima.imgNormal = jogo.uiSpriteSheet.load(4, 0, 2, 2)
		self.botaoCima.imgPressionando = jogo.uiSpriteSheet.load(4, 2, 2, 2)
		
		self.botaoBaixo = Botao(16, DISPLAY_TAMANHO_REAL[1]-24)
		self.botaoBaixo.imgNormal = jogo.uiSpriteSheet.load(6, 0, 2, 2)
		self.botaoBaixo.imgPressionando = jogo.uiSpriteSheet.load(6, 2, 2, 2)
		
		self.botaoEsquerda = Botao(0, DISPLAY_TAMANHO_REAL[1]-40)
		self.botaoEsquerda.imgNormal = jogo.uiSpriteSheet.load(0, 0, 2, 2)
		self.botaoEsquerda.imgPressionando = jogo.uiSpriteSheet.load(0, 2, 2, 2)
		
		self.botaoDireita = Botao(32, DISPLAY_TAMANHO_REAL[1]-40)
		self.botaoDireita.imgNormal = jogo.uiSpriteSheet.load(2, 0, 2, 2)
		self.botaoDireita.imgPressionando = jogo.uiSpriteSheet.load(2, 2, 2, 2)
		
		self.movendo = [False, [0, 0]]
	
	def mover(self, x, y, jogo, continuarMovendo=False):
		if not self.podeMover(x, y, jogo): return
		if self.movendo[0] and not continuarMovendo: return
		self.posMovendo.x = self.pos.x
		self.posMovendo.y = self.pos.y
		self.movendo = [True, [x, y]]
		self.pos.x += x*8
		self.pos.y += y*8
	
	def podeMover(self, x, y, jogo):
		novaPos = pg.math.Vector2(self.pos.x+x*8, self.pos.y+y*8)
		novaPos.x //= 8
		novaPos.y //= 8
		multiplos = [self.img.get_width()//8, self.img.get_height()//8]
		if 0<=novaPos.x<len(jogo.mapaManager.grid[0][0])-multiplos[0]+1 and 0<=novaPos.y<len(jogo.mapaManager.grid[0])-multiplos[1]+1:
			
			for x in range(multiplos[0]):
				for y in range(multiplos[1]):
					 if jogo.mapaManager.colisoes[int(novaPos.y+y)][int(novaPos.x+x)]!=257:
					 	return False
			return True
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
#		if not self.movendo[0]:
#			pos = self.pos-camera.pos
#			#pos.x = int(pos.x)
#			pos.y = int(pos.y)-2
#		else:
		pos = self.posMovendo-camera.pos
			#pos.x = int(pos.x)
		#pos.y -= 2
		display.blit(self.img, pos)		