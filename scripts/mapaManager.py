from pygame import (math, image, Surface, Rect)
from tmx import TileMap

#pg.init()

class MapaManager:
	def __init__(self):
		self.mapa = None
		self.colisoes = None
		self.grid = None
		self.tileset = None
		self.tilesetImg = None
		self.tilesDic = None
		self.funcoes = None
		self.tiles = None
		self.novoMapa("mapa1")
	
	
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
		del self.tilesetImg
		del self.grid
		del self.colisoes
		del self.tiles
		#self.grid = []
		print("name", filename)
		self.mapa = TileMap.load(f'recursos/mapas/{filename}.tmx')
		self.funcoes = self.mapa.layers[-1].objects
		#print("funcoes", self.funcoes)
		self.tileset = self.mapa.tilesets[0]
		print("tileset", self.tileset.name)
		self.tilesPraDicionario(self.tileset.tiles)
		#self.tilesetImg = image.load("recursos/sprites/tilesets/tileset_1.png").convert()
		tilesetImg = image.load(f"recursos/sprites/tilesets/{self.tileset.image.source.split('/')[-1]}").convert()
		tilesetImg.set_colorkey((0, 0, 0))
		self.grid = []
		self.colisoes = []
		#self.layers = self.mapa.layers
		self.tiles = self.tilesetPraLista(tilesetImg, self.tileset.tilewidth, self.tileset.tileheight)
		del tilesetImg
		self.carregarMapa()
	
	def emWarp(self, entidadeRect):
		#print(self.funcoes)
		for funcao in self.funcoes:
			if funcao.type=="warp":
				rect = Rect((funcao.x, funcao.y, funcao.width, funcao.height))
				if entidadeRect.colliderect(rect):
					return [True, funcao]
					
	def entrarWarp(self, Rect):
		for funcao in self.funcoes:
			if funcao.type=="warp" and self.emWarp(Rect):
				#print(self.conseguirMapaWarp(funcao))
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
				#if propriedade.name=="embaixo de entidade":
				valor = valor!="true"
				#print(tile.id+1)
				self.tilesDic[tile.id+1][propriedade.name] = valor
	
	def carregarMapa(self):
		y = 0
		for layer in self.mapa.layers:
			if layer.name!="funções":
				self.layerPraGrid(layer)
			
	def tilesetPraLista(self, tileset, tileLargura, tileAltura):
		lista = {}
		for y in range(int(tileset.get_height()/tileAltura)):
			for x in range(int(tileset.get_width()/tileLargura)):
				surface = Surface((tileLargura, tileAltura)).convert()
				rect = Rect((x*tileLargura, y*tileAltura, tileLargura, tileAltura))
				surface.blit(tileset, (0, 0), rect)
				surface.set_colorkey((0, 0, 0))
				if not self.transparente(surface):
					#print("gid", y*int(tileset.get_width()/tileLargura)+x+1)
					#print((x, y), y*int(tileset.get_width()/tileLargura)+x+1)
					lista[y*int(tileset.get_width()/tileLargura)+x+1] = surface
		return lista
##retorna true se a surface for toda transparente
	def transparente(self, surface):
		return surface.get_bounding_rect(1).width<1
			
	def layerPraGrid(self, layer):
		tiles = layer.tiles
	#	
#		if layer.name:
		grid = []
		l = []

		y, x = 0, 0
		for tile in tiles:
			#if tile.gid!=0:
			#print(tile.gid)
			l.append(tile.gid)
#			l.append(1)
		#	l.append(Tile(tile.gid))#, self.conseguirRect([x, y])))#, self.tilesDic[tile.gid-1]))

			x += 1
			if x==self.mapa.width:
				x = 0
				y += 1
				grid.append(l)
				#print(*l)
				#print(x, y, self.grid[y][x])
				l = []
		#print<(self.grid)
		if layer.name not in ["colisoes", "funções"]:
#			if not
			self.grid.append(grid)
		else:
			self.colisoes = grid
			
	def conseguirRect(self, pos):
		x = pos[0]*self.tileset.tilewidth
		y = pos[1]*self.tileset.tileheight
		return Rect((x, y, self.tileset.tilewidth, self.tileset.tileheight))	

	def show(self, camera, display, jogador):
		minY = max(int(camera.pos.y/16), 0)
		minX = max(int(camera.pos.x/16), 0)
		#print(self.mapa.width)
		maxY = min(int(camera.pos.y/16)+camera.altura+1, self.mapa.height)
		maxX = min(int(camera.pos.x/16)+camera.largura+1, self.mapa.width)
		#print(minX, maxX)
#		print(minY, maxY)
		self.showLayer(0, camera, display, jogador, minX, minY, maxX, maxY)
		self.showLayer(1, camera, display, jogador, minX, minY, maxX, maxY)
		
	def showLayer(self, layer, camera, display, jogadores, minX, minY, maxX, maxY):	
		#if f"{self.tileset.image.source.split('/')[-1]}"=="casa1.png":
#					print(x, y)
		y = minY
		while y<maxY:
		#for y in range(minY, maxY):#len(self.grid)):
			
			x = minX
			while x<maxX:			
				
				#draw.rect(display, (100, 200, 100), (x*16, y*16, 16, 16))
			#	print(self)
				
				self.showGid(layer, display, camera, x, y, jogadores)
				#if self.mapa.name==""
#				self.grid[y][x].show(display, camera, self.tiles)
				x += 1
				#print(x)
			y += 1
		
	def showGid(self, layer, display, camera, x, y, jogador):##mostrar os jogadores por arqui na frente da layer 1 e atras da layer 2
		#(minX, maxX), (minY, maxY))
		if layer==1:
			#for jogador in jogadores.values():
			jogadorX = round(jogador.pos.x/16)
			jogadorY = round(jogador.pos.y/16)
			embaixo = True
			if self.grid[layer][y][x] in self.tilesDic.keys():
				embaixo = self.tilesDic[self.grid[layer][y][x]]["embaixo de entidade"]
			if x in [jogadorX, jogadorX+1] and y in [jogadorY, jogadorY+1] and embaixo:
				jogador.show(display, camera)
			
		if self.grid[layer][y][x]!=0:

			
			display.blit(self.tiles[self.grid[layer][y][x]], (x*16-int(camera.pos.x), y*16-int(camera.pos.y)))

			jogadorX = round(jogador.pos.x/16)
			jogadorY = round(jogador.pos.y/16)
			embaixo = True
			if self.grid[layer][y][x] in self.tilesDic.keys():
				
				embaixo = self.tilesDic[self.grid[layer][y][x]]["embaixo de entidade"]
			if x in [jogadorX, jogadorX+1] and y in [jogadorY, jogadorY+1] and not embaixo and layer==1:#self.tilesDic[self.grid[layer][y][x]]["embaixo de entidade"]:
				#print(54)
				jogador.show(display, camera)
		
#		if self.grid[1][y][x]!=0:
#			for jogador in jogadores.values():
#			jogadorX = jogador.pos.x//16
#			jogadorY = jogador.pos.y//16
#			if x==jogadorX and y==jogadorY:
#				jogador.show(display, camera)
#			display.blit(self.tiles[self.grid[1][y][x]], (x*16-int(camera.pos.x), y*16-int(camera.pos.y)))
		
		#relativeCamera = math.Vector2(camera.pos.x%16, camera.pos.y%16)
#		
#		try:
#			#print(self.grid[y][x])
#			display.blit(self.tiles[self.grid[y][x]], (x*16-relativeCamera.x, y*16-relativeCamera.y))#-camera.pos.x, y*16-camera.pos.y))
#		except:
#			
#			raise Exception("")
			
#class Tile:
#	def __init__(self, gid):#, rect, propriedades=None):
#		self.propriedades = propriedades
#		self.gid = gid
		#self.RectVerdadeiro = rect
	
	
	
	#def show(self, tela, camera, tiles):
#		rect = self.conseguirRect(camera)

#		if rect.x+rect.width<0 or rect.x>tela.get_width() or rect.y+rect.height<0 or rect.y>tela.get_height():
#			return
#		tela.blit(tiles[self.gid-1], rect)

#	def conseguirRect(self, camera):
#		return Rect((self.RectVerdadeiro.x-camera.pos.x, self.RectVerdadeiro.y-camera.pos.y, self.RectVerdadeiro.width, self.RectVerdadeiro.height))

#	def colide(self, rect):
#		return self.RectVerdadeiro.colliderect(rect)	