from pygame.math import Vector2
from scripts.config import *

class Camera:
	def __init__(self):
		self.posAntiga = Vector2(0, 0)
		self.pos = Vector2(0, 0)
		self.largura = int(DISPLAY_TAMANHO[0]//8)
		self.altura = int(DISPLAY_TAMANHO[1]//8)
	
	def moverPara(self, x, y, mapa):
		#posNova = math.Vector2(x-DISPLAY_TAMANHO[0]//2, y-DISPLAY_TAMANHO[1]//2)
#		self.pos.x = max(1, self.pos.x)
#		self.pos.y = max(1, self.pos.y)
		#self.pos = self.pos.lerp(posNova, 1/frames)
		self.posAntiga.x = self.pos.x
		self.posAntiga.y = self.pos.y
		self.pos.x -= self.pos.x - (x-DISPLAY_TAMANHO[0]//2)
		self.pos.y -= self.pos.y - (y-DISPLAY_TAMANHO[1]//2)
		
		self.pos.x = max(0, self.pos.x)
		self.pos.y = max(0, self.pos.y)
		self.pos.x = min(mapa.width*8-DISPLAY_TAMANHO[0], self.pos.x)
		self.pos.y = min(mapa.height*8-DISPLAY_TAMANHO[1], self.pos.y)
#		self.posAntiga.x = max(0, self.posAntiga.x)
#		self.posAntiga.y = max(0, self.posAntiga.y)
	
	def mudouPosicao(self):
		return self.posAntiga.x!=self.pos.x or self.posAntiga.y!=self.pos.y