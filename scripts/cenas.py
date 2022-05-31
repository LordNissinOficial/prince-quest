from pygame import event# as event
from pygame import Surface
from pygame.transform import scale
from pygame.locals import (QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP)
#from pygame import ()
#import pygame as pg
import pickle, copy
from enum import Enum
from scripts.uiComponentes import Botao
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
		self.spriteManager.load("spritesheets/ui")
		self.deltaTime = 0
		self.camera = Camera()
		self.jogador = Jogador(5, 5, self)
		self.display = Surface((256, 144)).convert()
		self.mapaDisplay = Surface((DISPLAY_TAMANHO)).convert()
		self.mapaManager = MapaManager(self.camera)
		self.cor = (62, 39, 49)		

	def update(self, cenaManager):		
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
	
	def showUi(self):
		self.jogador.botaoCima.show(self.display)
		self.jogador.botaoBaixo.show(self.display)
		self.jogador.botaoDireita.show(self.display)
		self.jogador.botaoEsquerda.show(self.display)

	def lidarEventos(self, cenaManager):
		for evento in cenaManager.eventos:			
			if evento.type in [MOUSEBUTTONDOWN, MOUSEMOTION]:
				pos = telaParaDisplay(*evento.pos)
				self.jogador.botaoCima.pressionandoMouse(pos)
				self.jogador.botaoBaixo.pressionandoMouse(pos)
				self.jogador.botaoDireita.pressionandoMouse(pos)
				self.jogador.botaoEsquerda.pressionandoMouse(pos)
				
			elif evento.type==MOUSEBUTTONUP:
				pos = telaParaDisplay(*evento.pos)
				self.jogador.botaoCima.tirandoMouse(pos)
				self.jogador.botaoBaixo.tirandoMouse(pos)
				self.jogador.botaoDireita.tirandoMouse(pos)
				self.jogador.botaoEsquerda.tirandoMouse(pos)
		
class ESTADOS(Enum):
	OVERWORLD = 0
	MENUPRINCIPAL = 1
	MENUCONFIGURACOES = 2
	MENUAJUDA = 3
	estados = [Overworld]#MenuPrincipal, MenuConfiguracoes]
	
def telaParaDisplay(x, y):
	return [int(x/TELA_TAMANHO[0]*DISPLAY_TAMANHO_REAL[0]),
				int(y/TELA_TAMANHO[1]*DISPLAY_TAMANHO_REAL[1])]