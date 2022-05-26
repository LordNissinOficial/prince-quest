import pygame as pg
from scripts.cenas import CenaManager

pg.init()
pg.font.init()

flags = pg.DOUBLEBUF
tela = pg.display.set_mode((1920, 1080), flags, 16)
fonte = pg.font.SysFont("Calibri", 10)
cenaManager = CenaManager()
clock = pg.time.Clock()
#print(cenaManager.jogo.mapaManager.funcoes)
while cenaManager.rodando:
	cenaManager.update()
	cenaManager.show(tela)
	tela.blit(fonte.render(str(int(clock.get_fps())), 0, (100, 100, 100)), (40, 40))
	pg.display.flip()
	clock.tick(40)