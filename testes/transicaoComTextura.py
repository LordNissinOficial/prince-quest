
import pygame as pg
import random
pg.init()

cutOff = 255
cutOffChange = 1

tela = pg.display.set_mode((1920, 1080))

display = pg.Surface((480, 320)).convert()
clock = pg.time.Clock()
img = pg.transform.scale(pg.image.load("Textures/angular_pattern.png"), display.get_size()).convert()

def getShader(surface, cutOff):
	imgCopy = img.copy()

	cor = min(255, max(0, cutOff))

	pg.transform.threshold(imgCopy, img, (255, 255, 255), threshold=(cor, cor, cor))
	imgCopy.set_colorkey((0, 0, 0))
	mask = pg.mask.from_surface(imgCopy, 0)
	#imgCopy = imgCopy.convert(8)
	#imgCopy.set_palette([[0, 0, 0, 255], [255, 255, 255, 255]])
	#imgCopy.set_colorkey((0, 0, 0))
	surf = mask.to_surface()
	surf.set_colorkey((255, 255, 255))
	return surf#imgCopy
	#print(cutOff)
	#imgCopy = pg.PixelArray(img)#pg.surfarray.array3d(img)#pg.Surface((480, 320)).convert()
	#print(imgCopy[0][0])
	#imgCopy = pg.surfarray.array3d(img.copy())
	#s = random.choice([0.1, 1])
	
	for y in range(len(imgCopy)):
		#print(imgCopy[y])
		break
		for x in range(len(imgCopy[0])):
			if img.unmap_rgb(imgCopy[y][x])[0]/255<=cutOff:
				imgCopy[y][x] = img.map_rgb((0, 0, 0))
			#print(imgCopy[y][x])
			if img.unmap_rgb(imgCopy[y][x])[0]/255<=cutOff:
				imgCopy[y][x] = [0, 0, 0]#img.map_rgb((0, 0, 0))
			#pixel = [0, 0, 0]
	for i in range(0, 256):
		if i>255:# i/255>cutOff:
			break
		imgCopy.replace((i/255, i/255, i/255), (0.0, 0.0, 0.0))#, weights=(s, s, s))
	for y in range(len(array)):
		for x in range(len(array[0])):
			color = array[y][x][0]/255
			if color<cutOff:
				array[y][x] = [200, 50, 50]
	print(1)
	
	#display.blit(array.make_surface(), (0, 0), special_flags=pg.BLEND_RGB_MAX)
	array.close()
	#pg.surfarray.blit_array(display, imgCopy)
	#return pg.surfarray.make_surface(imgCopy)
	#imgCopy = pg.surfarray.make_surface(imgCopy)
	imgCopy.set_palette([[i, i, i] for i in range(0, 256)])
	imgCopy = imgCopy.make_surface()
	imgCopy.set_colorkey((0, 0, 0))
	return imgCopy
	#return imgCopy#display#array.make_surface()#pg.surfarray.make_surface(array)#imgCopy	
		#	print(color)
			#break


while True:
	display.fill((60, 60, 100))
	#getShader(display, cutOff)
	display.blit(getShader(display, cutOff), (0, 0))
	tela.blit(pg.transform.scale(display, tela.get_size()), (0, 0))
	cutOff += cutOffChange
	if cutOff<-5:
		cutOff = 0
		cutOffChange *= -1
	if cutOff>260:
		cutOff = 1
		cutOffChange *= -1
	#cutOff = cutOff if cutOff<=1 else 0
	#print(cutOff)
	pg.display.update()
	print(clock.get_fps())
	clock.tick(30)