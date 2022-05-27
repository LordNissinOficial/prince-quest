import pygame as pg
import pickle, copy
from enum import Enum
from scripts.uiComponentes import Botao
from scripts.spritesheet import SpriteSheet
from scripts.mapaManager import MapaManager
from scripts.camera import Camera
from scripts.jogador import Jogador
from scripts.config import *

pg.init()

class CenaManager():
	"""classe principal que cuida do jogo atual"""
	def __init__(self):
		self.estado = ESTADOS.MENUPRINCIPAL
		self.uiSpriteSheet = SpriteSheet("ui")
		#self.fade = Fade1()
		self.deltatime = 0
		self.jogoAntigo = None
		self.jogo = None
		self.rodando = 1
		self.eventos = []
		self.setJogo(ESTADOS.OVERWORLD)
		pg.event.set_blocked(None)
		pg.event.set_allowed([pg.QUIT, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.MOUSEMOTION])
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
		self.eventos = pg.event.get()
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
#			tela.blit(pg.transform.scale(displayCopia, tela.get_size()), (0, 0))
#			return
		self.jogo.show()
		pg.transform.scale(self.jogo.display, tela.get_size(), tela)

class Overworld():
	def __init__(self, cenaManager):
		self.display = pg.Surface((256, 144)).convert()
		self.mapaDisplay = pg.Surface((DISPLAY_TAMANHO)).convert()
		self.uiSpriteSheet = SpriteSheet("ui")
		#self.uiSpriteSheet = SpriteSheet("ui_antiga")
		self.mapaManager = MapaManager()
		
		self.cor = (38, 43, 68)
		self.camera = Camera()
		self.jogador = Jogador(5, 5, self)

	def update(self, cenaManager):		
		self.jogador.update(self)
		self.camera.moverPara(self.jogador.posMovendo.x, self.jogador.posMovendo.y)
	
		self.lidarEventos(cenaManager)
		#self.jogadores[0].pos.x += 2
		#self.camera.pos.x += 1
		#self.camera.moverPara(self.jogadores[0].pos.x, self.jogadores[0].pos.y)
		#print("camera", self.camera.pos.x)
#		raise Exception("a")


	def show(self):
		self.display.fill(self.cor)
		self.mapaDisplay.fill(self.cor)
		self.mapaManager.show(self.camera, self.mapaDisplay, self.jogador)		
		self.display.blit(self.mapaDisplay, (48, 0))
		self.showUi()
		#pg.draw.rect(self.display, (100, 140, 100), (24, 144-55, 16, 16))
#		pg.draw.rect(self.mapaDisplay, (100, 140, 100), (24, 144-55, 16, 16))
	
	def showUi(self):
		self.jogador.botaoCima.show(self.display)
		self.jogador.botaoBaixo.show(self.display)
		self.jogador.botaoDireita.show(self.display)
		self.jogador.botaoEsquerda.show(self.display)

	def lidarEventos(self, cenaManager):
		for evento in cenaManager.eventos:			
			if evento.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEMOTION]:

				pos = telaParaDisplay(*evento.pos)
#				pos[0] = int(pos[0]/TELA_TAMANHO[0]*DISPLAY_TAMANHO[0])
#				pos[1] = int(pos[1]/TELA_TAMANHO[1]*DISPLAY_TAMANHO[1])
				self.jogador.botaoCima.pressionandoMouse(pos)
				self.jogador.botaoBaixo.pressionandoMouse(pos)
				self.jogador.botaoDireita.pressionandoMouse(pos)
				self.jogador.botaoEsquerda.pressionandoMouse(pos)
				
			elif evento.type==pg.MOUSEBUTTONUP:
				#self.uiSpriteSheet.m("ui")
				pos = telaParaDisplay(*evento.pos)
				#pos[0] = int(pos[0]/TELA_TAMANHO[0]*DISPLAY_TAMANHO[0])
#				pos[1] = int(pos[1]/TELA_TAMANHO[1]*DISPLAY_TAMANHO[1])
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