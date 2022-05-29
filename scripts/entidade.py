import pygame as pg


class Entidade():
	def __init__(self, x, y, largura, altura):
		self.largura = largura//8
		self.altura = altura//8
		self.x = x*8
		self.y = y*8
		self.xMovendo = x*8
		self.yMovendo = y*8
		self.movendo = [not False, [1, 0]]
		self.dentroDeWarp = None #id do warp que usou para nao entrar num warp enquanto sai dele.

	def mover(self, x, y, jogo, continuarMovendo=False):
		if not self.podeMover(x, y, jogo):	return
		if self.movendo[0] and not continuarMovendo: return
		self.xMovendo = self.x
		self.yMovendo = self.y
		self.movendo = [True, [x, y]]
		self.x += x*8
		self.y += y*8
	
	def podeMover(self, x, y, jogo):
		novoX = self.x//8+x
		novoY = self.y//8+y

		if 0<=novoX<len(jogo.mapaManager.grid[0][0])-self.largura+1 and 0<=novoY<len(jogo.mapaManager.grid[0])-self.altura+1:			
			for x in range(self.largura):
				for y in range(self.altura):					 
					 if jogo.mapaManager.colisoes[int(novoY+y)][int(novoX+x)]!=257:
					 	return False
			return True
		return False
	
	def updateMovimento(self, jogo):
		if self.movendo[0]:
			movendo = True
			self.xMovendo += self.movendo[1][0]*32*jogo.deltaTime
			self.yMovendo += self.movendo[1][1]*32*jogo.deltaTime
			if self.arrumarPosMovendo():
				self.movendo = [False, [0, 0]]
				self.xMovendo = self.x
				self.yMovendo = self.y
				
				if self.emWarp(jogo):
					self.movendo = [False, [0, 0]]
					jogo.mapaManager.entrarWarp(pg.Rect((self.pos.x, self.pos.y, 16, 16)))
				return 
				
			if self.xMovendo==self.x and self.yMovendo==self.y:
				continuarMovendo = False
				for index, botao in enumerate([self.botaoEsquerda, self.botaoDireita, self.botaoCima, self.botaoBaixo]):
					if [[-1, 0], [1, 0], [0, -1], [0, 1]][index]==self.movendo[1] and botao.pressionado:
						continuarMovendo = True
						break
				
				if self.emWarp(jogo):
						self.movendo = [False, [0, 0]]
						jogo.mapaManager.entrarWarp(pg.Rect((self.x, self.y, 16, 16)))
						#self.x, self.y = (3*16, 8*16)
						#self.xMovendo, self.yMovendo = (3*16, 8*16)
						#jogo.camera.pos = pg.math.Vector2(3*16, 8*16)
						
				if not continuarMovendo:					
					movendo = False
					self.movendo = [False, [0, 0]]
					self.xMovendo = self.x
					self.yMovendo = self.y
				else:
					self.mover(self.movendo[1][0], self.movendo[1][1], jogo, True)

	
	def arrumarPosMovendo(self):
		if self.movendo[1][0]==1 and self.xMovendo>self.x: return True
		if self.movendo[1][0]==-1 and self.xMovendo<self.x: return True
		if self.movendo[1][1]==1 and self.yMovendo>self.y: return True
		if self.movendo[1][1]==-1 and self.yMovendo<self.y: return True

	def emWarp(self, jogo):
		warp = jogo.mapaManager.emWarp(pg.Rect(self.x, self.y, self.largura*8, self.altura*8))
		if warp:
			warpId = [propertie.value for propertie in warp.properties if propertie.name=="warp_id"][0]
			if warpId==self.dentroDeWarp: return False
			self.dentroDeWarp = warpId
			return True
		else:
			self.dentroDeWarp = None
			return False