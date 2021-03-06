from pygame.math import Vector2
from scripts.config import *

class Camera:
	def __init__(self):
		self.x = 0
		self.xAntigo = 0
		self.y = 0
		self.yAntigo = 0
#		self.posAntiga = Vector2(0, 0)
#		self.pos = Vector2(0, 0)
		self.largura = int(DISPLAY_TAMANHO[0]//8)
		self.altura = int(DISPLAY_TAMANHO[1]//8)
	
	def moverPara(self, x, y, mapa):
		#posNova = math.Vector2(x-DISPLAY_TAMANHO[0]//2, y-DISPLAY_TAMANHO[1]//2)
#		self.pos.x = max(1, self.pos.x)
#		self.pos.y = max(1, self.pos.y)
		#self.pos = self.pos.lerp(posNova, 1/frames)
		self.xAntigo = self.x
		self.yAntigo = self.y
		self.x -= self.x - (x-DISPLAY_TAMANHO[0]//2)
		self.y -= self.y - (y-DISPLAY_TAMANHO[1]//2)
		
		self.x = max(0, self.x)
		self.y = max(0, self.y)
		self.x = min(mapa.width*8-DISPLAY_TAMANHO[0], self.x)
		self.y = min(mapa.height*8-DISPLAY_TAMANHO[1], self.y)
#		self.posAntiga.x = max(0, self.posAntiga.x)
#		self.posAntiga.y = max(0, self.posAntiga.y)
	
	def mudouPosicao(self):
		x = int(self.x/8)
		xAntigo = int(self.xAntigo/8)
		y = int(self.y/8)
		yAntigo = int(self.yAntigo/8)
		return xAntigo!=x or yAntigo!=y#self.xAntigo!=self.x or self.yAntigo!=self.y