from pygame.font import (init, SysFont)
from pygame.time import Clock
from pygame.display import (set_mode, flip)
from pygame.locals import (DOUBLEBUF, FULLSCREEN)
#import pygame as pg
from scripts.cenas import CenaManager
from profilehooks import profile

#pg.init()
init()

#@profile()
def main():
	frame = 0
	flags = DOUBLEBUF|FULLSCREEN
	tela = set_mode((1920, 1080), flags, 16)
	fonte = SysFont("Calibri", 10)
	cenaManager = CenaManager()
	clock = Clock()
	while cenaManager.rodando:# and frame<240:
		#frame += 1
		cenaManager.update()
		cenaManager.show(tela)
		tela.blit(fonte.render(str(int(clock.get_fps())), 0, (100, 100, 100)), (40, 40))
		flip()
		cenaManager.jogo.deltaTime = clock.tick(50)/1000

main()