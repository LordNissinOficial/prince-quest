from pygame.image import load

class SpriteManager():
	def __init__(self):
		self.path = "recursos/sprites/"
		self.spriteAtual = None
		self.sprites = {}
	
	def load(self, filename, rect=None):
		if filename not in self.sprites:
			try:
				self.sprites[filename] = load(self.path+filename+".png").convert()
				self.sprites[filename].set_colorkey((0, 0, 0))
			except:
				raise Exception(f"nao foi possivel carregar arquivo {self.path+filename+'.png'}")
		
		if rect:
			return self.sprites[filename].subsurface((rect[0]*8, rect[1]*8, rect[2]*8, rect[3]*8))
		return self.sprites[filename]