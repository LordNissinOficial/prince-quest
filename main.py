import pygame as pg
from scripts.cenas import CenaManager
from profilehooks import profile
pg.init()
pg.font.init()

#@profile()
def main():
	a = 0
	flags = pg.DOUBLEBUF
	tela = pg.display.set_mode((1920, 1080), flags, 16)
	#tela.set_alpha(None)
	fonte = pg.font.SysFont("Calibri", 10)
	cenaManager = CenaManager()
	clock = pg.time.Clock()
	while cenaManager.rodando and a<30:
		#a += 1
		cenaManager.update()
		cenaManager.show(tela)
		tela.blit(fonte.render(str(int(clock.get_fps())), 0, (100, 100, 100)), (40, 40))
#		tela.blit(fonte.render(str((cenaManager.jogo.camera.posAntiga, cenaManager.jogo.camera.pos)), 0, (100, 100, 100)), (40, 50))
#		tela.blit(fonte.render(str(cenaManager.jogo.camera.mudouPosicao()), 0, (100, 100, 100)), (40, 60))
		pg.display.flip()
		cenaManager.jogo.deltaTime = clock.tick(50)/1000

main()
#import cProfile as Profile
#Profile.run('main()')