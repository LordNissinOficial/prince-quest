from pygame import (image, Surface, Rect)
from scripts.config import *
from tmx import TileMap

class MapaManager:
	def __init__(self, camera):
		self.camera = camera
		self.display = Surface(DISPLAY_TAMANHO).convert()
		self.mapa = None
		self.colisoes = None
		self.grid = None
		self.tileset = None
		self.tilesDic = None
		self.funcoes = None
		self.tiles = None
		self.novoMapa("mapa-mundi")
		self.show(camera)
	
#	def __getstate__(self):
#		state = self.__dict__.copy()
#		#state["tilesetImg"] = image.tostring(state['tilesetImg'], "RGB")
#	#	print(state['tiles'], end="\n"*4)
#		print(self.tiles)
#		for key, tile in list(state["tiles"].items()):
#			#print(key, state['tiles'][key])
#			state['tiles'][key] = image.tostring(tile, "RGB")
#			
#		#print(state['tiles'])
#		return state
#	
#	def __setstate__(self, state):
#		state["tilesetImg"] = image.fromstring(state['tilesetImg'], [128, 128], "RGB")
#		state["tilesetImg"].set_colorkey((0, 0, 0))
#		for key, tile in state["tiles"].items():
#			#print(key, state["tiles"][key])
#			state["tiles"][key] = image.fromstring(tile, [16, 16], "RGB")
#		#print(state["tiles"])
#		self.__dict__.update(state)	
	
	
	def novoMapa(self, filename):
		del self.mapa
		del self.tileset
		del self.funcoes
		del self.grid
		del self.colisoes
		del self.tiles
		print("name", filename)
		self.mapa = TileMap.load(f'recursos/mapas/{filename}.tmx')
		self.funcoes = self.mapa.layers[-1].objects
		print("funcoes", self.funcoes)
		self.tileset = self.mapa.tilesets[0]
		print("tileset", self.tileset.name, "size", (self.tileset.tilewidth, self.tileset.tileheight))
		self.tilesPraDicionario(self.tileset.tiles)
		tilesetImg = image.load(f"recursos/sprites/tilesets/{self.tileset.image.source.split('/')[-1]}").convert()
		self.grid = []
		self.colisoes = []
		self.tiles = self.tilesetPraLista(tilesetImg, self.tileset.tilewidth, self.tileset.tileheight)
		del tilesetImg
		self.carregarMapa()
		self.show(self.camera)
	
	def emWarp(self, entidadeRect):
		for funcao in self.funcoes:
			if funcao.type=="warp":
				rect = Rect((funcao.x, funcao.y, funcao.width, funcao.height))
				if entidadeRect.colliderect(rect):
					return funcao
		return False
				
	def entrarWarp(self, Rect):
		for funcao in self.funcoes:
			if funcao.type=="warp" and self.emWarp(Rect):
				self.novoMapa(self.conseguirMapaWarp(funcao))
	
	def conseguirMapaWarp(self, warp):
		for propriedade in warp.properties:
			if propriedade.name=="mapa":
				return propriedade.value[0:propriedade.value.find(".")]
	
	def tilesPraDicionario(self, tiles):
		del self.tilesDic
		self.tilesDic = {}
		for tile in tiles:
			self.tilesDic[tile.id+1] = {}
			for propriedade in tile.properties:
				valor = propriedade.value
				valor = valor!="true"
				self.tilesDic[tile.id+1][propriedade.name] = valor
	
	def carregarMapa(self):
		y = 0
		for layer in self.mapa.layers:
			if layer.name!="funcoes":
				self.layerPraGrid(layer)
			
	def tilesetPraLista(self, tileset, tileLargura, tileAltura):
		lista = {}
		for y in range(tileset.get_height()//tileAltura):
			for x in range(tileset.get_width()//tileLargura):
				surface = Surface((tileLargura, tileAltura))
				rect = Rect((x*tileLargura, y*tileAltura, tileLargura, tileAltura))
				surface.blit(tileset, (0, 0), rect)
				if not self.transparente(surface):
					lista[y*int(tileset.get_width()/tileLargura)+x+1] = surface.convert()
		return lista
		
##retorna true se a surface for toda transparente
	def transparente(self, surface):
		return surface.get_bounding_rect(1).width<1
			
	def layerPraGrid(self, layer):
		tiles = layer.tiles
		grid = []
		l = []
		y, x = 0, 0
		
		for tile in tiles:
			l.append(tile.gid)
			x += 1
			if x==self.mapa.width:
				x = 0
				y += 1
				grid.append(l)
				l = []
		if layer.name!="colisoes":
			self.grid.append(grid)
		else:
			self.colisoes = grid
			
	def conseguirRect(self, pos):
		x = pos[0]*self.tileset.tilewidth
		y = pos[1]*self.tileset.tileheight
		return Rect((x, y, self.tileset.tilewidth, self.tileset.tileheight))	

	def show(self, camera):
		minY = max(int(camera.pos.y/8), 0)
		maxY = min(int(camera.pos.y/8+camera.altura+1), self.mapa.height)
		minX = max(int(camera.pos.x/8), 0)
		maxX = min(int(camera.pos.x/8+camera.largura+1), self.mapa.width)		

		self.showLayer(0, camera, minX, minY, maxX, maxY)
		
	def showLayer(self, layer, camera, minX, minY, maxX, maxY):
		
		for y in range(minY, maxY):
			for x in range(minX, maxX):
				self.display.blit(self.tiles[self.grid[layer][y][x]], (x*self.tileset.tilewidth-int(camera.pos.x), y*self.tileset.tileheight-int(camera.pos.y)))
				#self.showGid(layer, camera, x, y)
				#10**5
		
#	def showGid(self, layer, camera, x, y):		
#		self.display.blit(self.tiles[self.grid[layer][y][x]], (x*self.tileset.tilewidth-int(camera.pos.x), y*self.tileset.tileheight-int(camera.pos.y)))
