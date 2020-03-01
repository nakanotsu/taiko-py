import os, sys, pygame
import itertools, random

# Set Window
displaysize = displayWidth, displayHeight = 1920, 1080
winsize = windowWidth, windowHeight = 1280, 768
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (displayWidth/2-windowWidth/2, displayHeight/2-windowHeight/2)

singuletProbability = 0.3
doubletProbability = 0.8

def generateBeatmap(size):
	color = True
	beatmap = []
	for i in range(size):
		probability = random.random()
		if probability <= singuletProbability: 
			if color is True:
				beatmap.append(1)
			else:
				beatmap.append(0)
		if probability > singuletProbability and probability <= doubletProbability:
			if color is True:
				beatmap.extend((1,1))
			else:
				beatmap.extend((0,0))
		if probability > doubletProbability:
			if color is True:
				beatmap.extend((1,1,1))
			else:
				beatmap.extend((0,0,0))
		color = not color
	return beatmap

beatmapSize = 90
beatmap = generateBeatmap(beatmapSize)
beatmapOnScreenLimit = 60
kat = 0
don = 1

hitAreaRadius = 60
hitObjectRadius = 45
hitObjectLeftMargin = hitAreaRadius*2
playAreaBackgroundHeight = 200
playAreaBackgroundMarginTop = 250
playAreaBackgroundMarginLeft = 0
playAreaBackgroundVCenter = playAreaBackgroundMarginTop + int(playAreaBackgroundHeight/2)

sliderVelocity = int(hitAreaRadius*0.7)

currentKeyState = ['Right Hand', 'Left Hand']
currentKeyStateActive = 0

isPopped = False
iAnimation = 0

black = 0, 0, 0
white = 255, 255, 255
grey = 50, 50, 50
red = 255, 0, 0
blue = 0, 0, 255

screen = pygame.display.set_mode(winsize)

def drawHitObject(color, x_pos, y_pos):
	if color is 1: color = red
	elif color is 0: color = blue
	circleBorderBlack = pygame.draw.circle(screen, black, (x_pos, y_pos), hitObjectRadius+10)
	circleBorderWhite = pygame.draw.circle(screen, white, (x_pos, y_pos), hitObjectRadius+5)
	circleHit = pygame.draw.circle(screen, color, (x_pos, y_pos), hitObjectRadius)

def currentKeyRender(active=0):
	keysBackground = pygame.draw.rect(screen, grey, (0, playAreaBackgroundMarginTop-50, hitAreaRadius*4, 50))
	keysHeight = keysBackground.bottom-keysBackground.top
	if active is 1:	
		keyRimLeft = pygame.draw.rect(screen, white, (0, keysBackground.top, hitAreaRadius, keysHeight),0)
	else:
		keyRimLeft = pygame.draw.rect(screen, white, (0, keysBackground.top, hitAreaRadius, keysHeight),1)
	if active is 2:
		keyDrumLeft = pygame.draw.rect(screen, white, (hitAreaRadius, keysBackground.top, hitAreaRadius, keysHeight),0)
	else:
		keyDrumLeft = pygame.draw.rect(screen, white, (hitAreaRadius, keysBackground.top, hitAreaRadius, keysHeight),1)
	if active is 3:
		keyDrumRight = pygame.draw.rect(screen, white, (hitAreaRadius*2, keysBackground.top, hitAreaRadius, keysHeight),0)
	else:
		keyDrumRight = pygame.draw.rect(screen, white, (hitAreaRadius*2, keysBackground.top, hitAreaRadius, keysHeight),1)
	if active is 4:
		keyRimRight = pygame.draw.rect(screen, white, (hitAreaRadius*3, keysBackground.top, hitAreaRadius, keysHeight),0)
	else: 
		keyDrumRight = pygame.draw.rect(screen, white, (hitAreaRadius*3, keysBackground.top, hitAreaRadius, keysHeight),1)

def playAreaRender():
	playAreaBackground = pygame.draw.rect(screen, grey, (playAreaBackgroundMarginLeft, playAreaBackgroundMarginTop, windowWidth, playAreaBackgroundHeight))
	hitArea = pygame.draw.circle(screen, white, (hitAreaRadius*2, playAreaBackgroundVCenter), hitAreaRadius, 2)

def beatmapRender():
	left_margin = hitObjectLeftMargin
	for hitObject in beatmap[:beatmapOnScreenLimit]:
		drawHitObject(hitObject, left_margin, playAreaBackgroundVCenter)
		left_margin += sliderVelocity

def popAnimation():
	left_margin = hitObjectLeftMargin
	#drawHitObject(beatmap[0], hitObjectLeftMargin, playAreaBackgroundVCenter-iAnimation)
	for hitObject in beatmap[1:beatmapOnScreenLimit]:
		drawHitObject(hitObject, sliderVelocity+left_margin-iAnimation, playAreaBackgroundVCenter)
		left_margin += sliderVelocity

pygame.init()

while True:	
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN:
			pressed = pygame.key.get_pressed()
			if beatmap and isPopped is False:
				if  pressed[pygame.K_z] and currentKeyState[0] is "Left Hand" and beatmap[0] is kat: isPopped = True
				if  pressed[pygame.K_x] and currentKeyState[0] is "Left Hand" and beatmap[0] is don: isPopped = True
				if  pressed[pygame.K_b] and currentKeyState[0] is "Right Hand" and beatmap[0] is don: isPopped = True
				if  pressed[pygame.K_n] and currentKeyState[0] is "Right Hand" and beatmap[0] is kat: isPopped = True
			if  pressed[pygame.K_F1]: beatmap = generateBeatmap(beatmapSize)

	screen.fill(black)
	playAreaRender()
	if beatmap:
		if currentKeyState[0] is "Right Hand":
			if beatmap[0] is kat: currentKeyStateActive = 4
			if beatmap[0] is don: currentKeyStateActive = 3
		else:
			if beatmap[0] is don: currentKeyStateActive = 2
			if beatmap[0] is kat: currentKeyStateActive = 1
		currentKeyRender(currentKeyStateActive)
	else:
		currentKeyRender()
	if isPopped:
		popAnimation()
		if iAnimation < 30:
			iAnimation += 2
		else:
			iAnimation = 0
			beatmap.pop(0)
			isPopped = False
			currentKeyState = currentKeyState[::-1] 
	else:
		beatmapRender()

	pygame.display.flip()