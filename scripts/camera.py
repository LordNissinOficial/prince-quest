from pygame import math
from scripts.config import *

class Camera:
	def __init__(self):
		self.pos = math.Vector2(0, 0)
		self.largura = int(DISPLAY_TAMANHO[0]//8)
		self.altura = int(DISPLAY_TAMANHO[1]//8)
	
	def moverPara(self, x, y):
		#posNova = math.Vector2(x-DISPLAY_TAMANHO[0]//2, y-DISPLAY_TAMANHO[1]//2)
#		self.pos.x = max(1, self.pos.x)
#		self.pos.y = max(1, self.pos.y)
		#self.pos = self.pos.lerp(posNova, 1/frames)

		self.pos.x -= self.pos.x - (x-DISPLAY_TAMANHO[0]//2)
		self.pos.y -= self.pos.y - (y-DISPLAY_TAMANHO[1]//2)
		
		self.pos.x = max(0, self.pos.x)
		self.pos.y = max(0, self.pos.y)