########################################
###        Bibliothèque Snake        ###
###      (c) Zeste de Savoir (c)     ###
###           Licence GPL            ###
###         Auteur : TAlone          ###
########################################

# Import des bibliothéques pygame et dotmap (faire attention à les installer: pip install pygame dotmap)
import pygame
from dotmap import DotMap
# Import de la fonction tirant des nombres aléatoires
from random import randint
# Import de la fonction d'arrondi au supérieur
from math import ceil

# Définition de constantes de jeu par défaut
WIDTH = 640
HEIGHT = 416
GRID = 32

class Snake:
	# Liste de directions pour une utilisation simplifiée
	DIRECTIONS = DotMap({
		"RIGHT": 0,
		"LEFT": 2,
		"TOP": 1,
		"BOTTOM": 3,
		"STOP": 4
	})

	# Liste des parties du serpent pour une plus grande aisance
	PARTS = DotMap({
		"HEAD": 0,
		"BODY": 1,
		"TAIL": 2
	})

	# initX, initY : positions initiales de la tête
	def __init__(self, initX=160, initY=64):
		# Positions (x, y) du serpent sur la fenêtre de jeu
		self.sX = [initX, initX - GRID, initX - 2 * GRID]
		self.sY = [initY, initY, initY]
		# Rotations des morceaux de serpent
		self.sR = [0, 0, 0]

	def nextFrame(self):
		# Avancement du corps du serpent : chaque morceau prend la position du précédent
		for i in range(len(self.sX) - 1, 0, -1):
			self.sX[i] = self.sX[i - 1]
			self.sY[i] = self.sY[i - 1]
			self.sR[i] = self.sR[i - 1]

	def move(self, direction, step=GRID):
		# D'abord, bouger tout le corps
		if direction != self.DIRECTIONS.STOP: self.nextFrame()

		# Puis mettre à jour la tête selon la direction souhaitée
		if direction == self.DIRECTIONS.RIGHT:
			self.sX[0] += step
		elif direction == self.DIRECTIONS.LEFT:
			self.sX[0] -= step
		elif direction == self.DIRECTIONS.BOTTOM:
			self.sY[0] += step
		elif direction == self.DIRECTIONS.TOP:
			self.sY[0] -= step

		# Les rotations sont plus simples grâce aux constantes
		self.sR[0] = 90 * direction

	def partsIterator(self):
		# Pour chaque partie du corps...
		for i in range(len(self.sX), 0, -1):
			# ...on regarde d'abord le type...
			type = self.PARTS.BODY
			if i == 1: type = self.PARTS.HEAD
			elif i == len(self.sX): type = self.PARTS.TAIL

			# ...avant de donner les informations nécessaires.
			yield DotMap({
				"position": (self.sX[i - 1], self.sY[i - 1]),
				"rotation": self.sR[i - 1],
				"type": type
			})

	def grow(self):
        # On regarde d'abord la direction de la dernière partie du serpent
		direction = self.sR[len(self.sR) - 1] / 90

        # On ajoute une composante de rotation similaire
		self.sR.append(direction * 90)

        # En fonction de la direction, il faut ajouter la composante à différents endroits
		if direction == self.DIRECTIONS.RIGHT:
			self.sX.append(self.sX[len(self.sX) - 1] - GRID)
			self.sY.append(self.sY[len(self.sY) - 1])
		elif direction == self.DIRECTIONS.LEFT:
			self.sX.append(self.sX[len(self.sX) - 1] + GRID)
			self.sY.append(self.sY[len(self.sY) - 1])
		elif direction == self.DIRECTIONS.BOTTOM:
			self.sX.append(self.sX[len(self.sX) - 1])
			self.sY.append(self.sY[len(self.sY) - 1] - GRID)
		elif direction == self.DIRECTIONS.TOP:
			self.sX.append(self.sX[len(self.sX) - 1])
			self.sY.append(self.sY[len(self.sY) - 1] + GRID)

	def getHeadPosition(self):
		# Donne la position de la tête du serpent
		return (self.sX[0], self.sY[0])

class Game:
	def __init__(self, init=None, loop=None, width=WIDTH, height=HEIGHT):
		# Initialisation de PyGame
		pygame.init()

		# Déclarations des paramètres facultatifs (fonctions du jeu)
		if init is None:
			def init(game):
				return

		if loop is None:
			def loop(game):
				return

		# Ajout des variables internes
		self.assets = { }
		self.screen = pygame.display.set_mode((width, height))
		self.clock = pygame.time.Clock()
		self.wWidth = width
		self.wHeight = height
		self.opened = True
		self.__init = init
		self.__loop = loop

		# Un peu d'esthétique
		# pygame.display.set_icon(apple)
		pygame.display.set_caption("Snake")

		# Lancement de l'initialisation
		self.__init(self)
		# Lancement de la boulce infinie principale
		self.loop()

	def loop(self):
		# Lancement de la boucle tant que le jeu est ouvert
		while self.opened:
			# Prétraitement des événements
			self.events = {}

			# Pour chaque évenement PyGame, on prémache le boulot
			for e in pygame.event.get():
				if e.type == pygame.KEYDOWN:
					self.events[e.type] = e.key
				else:
					self.events[e.type] = 0
			
			# Lancement de la boucle utilisateur
			self.__loop(self)

	def asset(self, name, rotation=0):
        # Effectue une rotation (éventuelle) de la tile avant de la retourner
		sprite = pygame.transform.rotate(self.assets[name], rotation)
		return sprite

    # Chargement d'un asset dans PyGame
	def addAsset(self, name, path):
		self.assets[name] = pygame.image.load(path)

	def eraseScreen(self):
		# Remplis l'écran de blanc
		self.screen.fill((255, 255, 255))

		# Si un fond est défini, remplis l'écran avec ce fond
		if self.assets["background"]:
			for x in range(0, ceil(self.wWidth / GRID)):
				for y in range(0, ceil(self.wHeight / GRID)):
					self.screen.blit(self.assets["background"], (x * GRID, y * GRID))

	def draw(self, sprite, position):
		# Dessin simple d'un sprite à l'écran
		self.screen.blit(sprite, position)

	def endDraw(self):
		# Rafraichissement de l'écran
		pygame.display.flip()
		# Délai avant la prochaine frame (6 FPS)
		self.clock.tick(6)

	def end(self):
		self.opened = False

	def randomPosition(self):
		# Donne une position sur la zone de jeu
		return (randint(0, ceil(self.wWidth / GRID)) * GRID, randint(0, ceil(self.wHeight / GRID)) * GRID)

	def collision(self, p1, p2):
		# cf. https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection
		return (p1[0] < p2[0] + GRID) and (p1[0] + GRID > p2[0]) and (p1[1] < p2[1] + GRID) and (p1[1] + GRID > p2[1])

	def screenIterator(self):
		# Renvoie un itérateur de chaque x et y disponible sur la grille
		for x in range(0, ceil(self.wWidth / GRID)):
			for y in range(0, ceil(self.wHeight / GRID)):
				yield (x * GRID, y * GRID)

	def isSide(self, position):
		# Fonction de détection de côté de la zone de jeu
		return position[0] == 0 or position[1] == 0 or position[0] >= self.wWidth - GRID or position[1] >= self.wHeight - GRID
