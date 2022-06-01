from pygame import event# as event
from pygame import Surface
from pygame.transform import scale
from pygame.locals import (QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP)
#from pygame import ()
#import pygame as pg
import pickle, copy
from enum import Enum
from scripts.uiComponentes import Botao
from scripts.inventario import Inventario
from scripts.spriteManager import SpriteManager
from scripts.spritesheet import SpriteSheet
from scripts.mapaManager import MapaManager
from scripts.camera import Camera
from scripts.jogador import Jogador
from scripts.config import *

class CenaManager():
	
	"""classe principal que cuida do jogo atual"""	
	def __init__(self):
		self.estado = ESTADOS.MENUPRINCIPAL
		self.spriteManager = SpriteManager()
		#self.fade = Fade1()
		self.deltatime = 0
		self.jogoAntigo = None
		self.jogo = None
		self.rodando = 1
		self.eventos = []
		self.setJogo(ESTADOS.OVERWORLD)
		event.set_blocked(None)
		event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION])
		
	"""decide o jogo atual"""
	def setJogo(self, ESTADO):
		self.estado  = ESTADO
		self.setUp()
		
	"""reinicia o jogo atual"""	
	def setUp(self):
		self.jogoAntigo = self.jogo
		self.jogo = ESTADOS.estados.value[self.estado.value](self)
		
#		if self.jogoAntigo:
#			self.fade.fadeOut()
#		else:
#			self.jogo.setUp(self)
	"""updatea o jogo atual"""
	def update(self):
		if not self.rodando: return
#		if self.fade.fading:
#			if self.fade.fadeout:
#				self.fade.update(self)
#				if self.fade.fadein:
#					self.jogo.setUp(self)
#					self.jogo.show()					
#				return
#			else:
#				self.fade.update(self)
		self.eventos = event.get()
		self.jogo.update(self)

	
	"""desenha na tela o display do jogo atual"""
	def show(self, tela):
		if not self.rodando: return
#		if self.fade.fading:			
#			if self.fade.fadeout:
#				displayCopia = self.jogoAntigo.display.copy()
#			else:
#				self.jogo.show()
#				displayCopia = self.jogo.display.copy()

#			self.fade.show(displayCopia)
#			tela.blit(transform.scale(displayCopia, tela.get_size()), (0, 0))
#			return
		self.jogo.show()
		scale(self.jogo.display, TELA_TAMANHO, tela)
		#print(555)

class Overworld():
	def __init__(self, cenaManager):
		self.spriteManager = cenaManager.spriteManager
		self.inventario = Inventario(self.spriteManager)
		self.spriteManager.load("spritesheets/ui")
		self.deltaTime = 0
		self.camera = Camera()
		
		self.jogador = Jogador(5, 5, self)
		self.display = Surface((256, 144)).convert()
		self.mapaDisplay = Surface((DISPLAY_TAMANHO)).convert()
		self.mapaManager = MapaManager(self.camera)
		self.cor = (62, 39, 49)
		self.botoes = {}
		self.setUpBotoes()
	
	def setUpBotoes(self):
		botoes = self.botoes
		botoes["cima"] = Botao(16, DISPLAY_TAMANHO_REAL[1]-56, lambda: self.jogador.mover(0, -1, self), True)
		botoes["cima"].imgNormal = (4, 0, 2, 2)
		botoes["cima"].imgPressionando = (4, 2, 2, 2)
		
		botoes["baixo"] = Botao(16, DISPLAY_TAMANHO_REAL[1]-24, lambda: self.jogador.mover(0, 1, self), True)
		botoes["baixo"].imgNormal = (6, 0, 2, 2)
		botoes["baixo"].imgPressionando = (6, 2, 2, 2)
		
		botoes["esquerda"] = Botao(0, DISPLAY_TAMANHO_REAL[1]-40, lambda: self.jogador.mover(-1, 0, self), True)
		botoes["esquerda"].imgNormal = (0, 0, 2, 2)
		botoes["esquerda"].imgPressionando = (0, 2, 2, 2)
		
		botoes["direita"] = Botao(32, DISPLAY_TAMANHO_REAL[1]-40, lambda: self.jogador.mover(1, 0, self), True)
		botoes["direita"].imgNormal = (2, 0, 2, 2)
		botoes["direita"].imgPressionando = (2, 2, 2, 2)
		
		botoes["inventario"] = Botao(208, 8, self.inventario.toggle)
		botoes["inventario"].imgNormal = (8, 0, 2, 2)
		botoes["inventario"].imgPressionando = (8, 2, 2, 2)
		
	def update(self, cenaManager):
		for botao in self.botoes:
			self.botoes[botao].update()
			
		self.jogador.update(self)
		self.camera.moverPara(self.jogador.xMovendo, self.jogador.yMovendo, self.mapaManager.mapa)
	
		self.lidarEventos(cenaManager)

	def show(self):
		self.display.fill(self.cor)
		if self.camera.mudouPosicao()==True:
			self.mapaManager.show(self.camera)
		
		self.mapaDisplay.blit(self.mapaManager.display, (0, 0))
		self.jogador.show(self.mapaDisplay, self.camera)
		self.display.blit(self.mapaDisplay, (48, 0))
		self.showUi()
		self.inventario.show(self.display)
	
	def showUi(self):
		for botao in self.botoes:
			self.botoes[botao].show(self.display, self.spriteManager)

	def lidarEventos(self, cenaManager):
		for evento in cenaManager.eventos:			
			if evento.type in [MOUSEBUTTONDOWN, MOUSEMOTION]:
				pos = telaParaDisplay(*evento.pos)
				for botao in self.botoes:
					self.botoes[botao].pressionandoMouse(pos)
				
			elif evento.type==MOUSEBUTTONUP:
				pos = telaParaDisplay(*evento.pos)
				for botao in self.botoes:
					self.botoes[botao].tirandoMouse(pos)
		
class ESTADOS(Enum):
	OVERWORLD = 0
	MENUPRINCIPAL = 1
	MENUCONFIGURACOES = 2
	MENUAJUDA = 3
	estados = [Overworld]#MenuPrincipal, MenuConfiguracoes]
	
def telaParaDisplay(x, y):
	return [int(x/TELA_TAMANHO[0]*DISPLAY_TAMANHO_REAL[0]),
				int(y/TELA_TAMANHO[1]*DISPLAY_TAMANHO_REAL[1])]