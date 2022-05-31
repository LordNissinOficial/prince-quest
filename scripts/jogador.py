from pygame.image import load
from scripts.entidade import Entidade
from scripts.uiComponentes import Botao
from scripts.config import *


class Jogador(Entidade):#pg.sprite.Sprite):
	def __init__(self, x, y, jogo):
		self.img = load("recursos/sprites/jogador.png").convert()
		self.img.set_colorkey((0, 0, 0))
		Entidade.__init__(self, x, y, self.img.get_width(), self.img.get_height())
		
		self.botaoCima = Botao(16, DISPLAY_TAMANHO_REAL[1]-56)
		self.botaoCima.imgNormal = jogo.spriteManager.load("spritesheets/ui", (4, 0, 2, 2))
		self.botaoCima.imgPressionando = jogo.spriteManager.load("spritesheets/ui", (4, 2, 2, 2))
		
		self.botaoBaixo = Botao(16, DISPLAY_TAMANHO_REAL[1]-24)
		self.botaoBaixo.imgNormal = jogo.spriteManager.load("spritesheets/ui", (6, 0, 2, 2))
		self.botaoBaixo.imgPressionando = jogo.spriteManager.load("spritesheets/ui", (6, 2, 2, 2))
		
		self.botaoEsquerda = Botao(0, DISPLAY_TAMANHO_REAL[1]-40)
		self.botaoEsquerda.imgNormal = jogo.spriteManager.load("spritesheets/ui", (0, 0, 2, 2))
		self.botaoEsquerda.imgPressionando = jogo.spriteManager.load("spritesheets/ui", (0, 2, 2, 2))
		
		self.botaoDireita = Botao(32, DISPLAY_TAMANHO_REAL[1]-40)
		self.botaoDireita.imgNormal = jogo.spriteManager.load("spritesheets/ui", (2, 0, 2, 2))
		self.botaoDireita.imgPressionando = jogo.spriteManager.load("spritesheets/ui", (2, 2, 2, 2))
	
	def update(self, jogo):			
		if self.botaoCima.pressionado:
			self.mover(0, -1, jogo)
		elif self.botaoBaixo.pressionado:
			self.mover(0, 1, jogo)
		elif self.botaoDireita.pressionado:
			self.mover(1, 0, jogo)
		elif self.botaoEsquerda.pressionado:
			self.mover(-1, 0, jogo)
		
		self.updateMovimento(jogo)

	def show(self, display, camera):
		x = self.xMovendo-camera.pos.x
		y = self.yMovendo-camera.pos.y
		display.blit(self.img, (x, y))		