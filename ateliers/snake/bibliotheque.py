########################################
###        Bibliothèque Snake        ###
###      (c) Zeste de Savoir (c)     ###
###           Licence GPL            ###
###    Auteurs : TAlone, Situphen    ###
########################################

# Import des bibliothèques pygame et dotmap (faire attention à les installer: pip install pygame dotmap)
import pygame
from dotmap import DotMap
# Import de la fonction tirant des nombres aléatoires
from random import randint
# Import de la fonction d'arrondi au supérieur
from math import ceil

# Définition de constantes de jeu par défaut
LARGEUR = 640
HAUTEUR = 416
GRILLE = 32

# Liste des évenements possibles dans le jeu
Evenements = DotMap({
	"QUITTER": pygame.QUIT,
	"TOUCHE_APPUYEE": pygame.KEYDOWN
})

# Liste des touches autorisées
Touches = DotMap({
	"FLECHE_DROITE": pygame.K_RIGHT,
	"FLECHE_GAUCHE": pygame.K_LEFT,
	"FLECHE_HAUT": pygame.K_UP,
	"FLECHE_BAS": pygame.K_DOWN
})

class Serpent:
	# Liste de directions pour une utilisation simplifiée
	DIRECTIONS = DotMap({
		"DROITE": 0,
		"GAUCHE": 2,
		"HAUT": 1,
		"BAS": 3,
		"STOP": 4
	})

	# Liste des parties du serpent pour une plus grande aisance
	PARTIES = DotMap({
		"TETE": 0,
		"CORPS": 1,
		"QUEUE": 2
	})

	# initX, initY : positions initiales de la tête
	def __init__(self, initX=160, initY=64):
		# Positions (x, y) du serpent sur la fenêtre de jeu
		self.sX = [initX, initX - GRILLE, initX - 2 * GRILLE]
		self.sY = [initY, initY, initY]
		# Rotations des morceaux de serpent
		self.sR = [0, 0, 0]

	def __avancer_serpent(self):
		# Avancement du corps du serpent : chaque morceau prend la position du précédent
		for i in range(len(self.sX) - 1, 0, -1):
			self.sX[i] = self.sX[i - 1]
			self.sY[i] = self.sY[i - 1]
			self.sR[i] = self.sR[i - 1]

	def deplacer(self, direction, pas=GRILLE):
		# D'abord, bouger tout le corps
		if direction != self.DIRECTIONS.STOP: self.__avancer_serpent()

		# Puis mettre à jour la tête selon la direction souhaitée
		if direction == self.DIRECTIONS.DROITE:
			self.sX[0] += pas
		elif direction == self.DIRECTIONS.GAUCHE:
			self.sX[0] -= pas
		elif direction == self.DIRECTIONS.BAS:
			self.sY[0] += pas
		elif direction == self.DIRECTIONS.HAUT:
			self.sY[0] -= pas

		# Les rotations sont plus simples grâce aux constantes
		self.sR[0] = 90 * direction

	def morceaux(self, longueur):
		# Vérifions que les participants ne fassent pas n'importe quoi
		if(longueur > len(self.sX)):
			longueur = self.taille

		# Pour chaque partie du corps...
		for i in range(longueur, 0, -1):
			# ...on regarde d'abord le type...
			type = self.PARTIES.CORPS
			if i == 1: type = self.PARTIES.TETE
			elif i == len(self.sX): type = self.PARTIES.QUEUE

			# ...avant de donner les informations nécessaires.
			yield DotMap({
				"position": (self.sX[i - 1], self.sY[i - 1]),
				"rotation": self.sR[i - 1],
				"type": type
			})
	
	# NOTE: la taille ne doit pas pouvoir être modifiée directement par l'utilisateur
	@property
	def taille(self):
		return len(self.sX)

	def grandir(self):
		# On regarde d'abord la direction de la dernière partie du serpent
		direction = self.sR[len(self.sR) - 1] / 90

		# On ajoute une composante de rotation similaire
		self.sR.append(direction * 90)

		# En fonction de la direction, il faut ajouter la composante à différents endroits
		if direction == self.DIRECTIONS.DROITE:
			self.sX.append(self.sX[len(self.sX) - 1] - GRILLE)
			self.sY.append(self.sY[len(self.sY) - 1])
		elif direction == self.DIRECTIONS.GAUCHE:
			self.sX.append(self.sX[len(self.sX) - 1] + GRILLE)
			self.sY.append(self.sY[len(self.sY) - 1])
		elif direction == self.DIRECTIONS.BAS:
			self.sX.append(self.sX[len(self.sX) - 1])
			self.sY.append(self.sY[len(self.sY) - 1] - GRILLE)
		elif direction == self.DIRECTIONS.HAUT:
			self.sX.append(self.sX[len(self.sX) - 1])
			self.sY.append(self.sY[len(self.sY) - 1] + GRILLE)

	# NOTE: la position de la tete ne doit pas pouvoir être modifiée directement par l'utilisateur
	@property
	def position_tete(self):
		# Donne la position de la tête du serpent
		return (self.sX[0], self.sY[0])

class Jeu:
	def __init__(self, initialisation=None, boucle=None, largeur=LARGEUR, hauteur=HAUTEUR):
		# Initialisation de PyGame
		pygame.init()

		# Déclarations des paramètres facultatifs (fonctions du jeu)
		if initialisation is None:
			def initialisation(jeu):
				return

		if boucle is None:
			def boucle(jeu):
				return

		# Ajout des variables internes
		self.images = { }
		self.ecran = pygame.display.set_mode((largeur, hauteur))
		self.horloge = pygame.time.Clock()
		self.largeur = largeur
		self.hauteur = hauteur
		self.__ouvert = True
		self.__initialisation = initialisation
		self.__boucle = boucle

		# Un peu d'esthétique
		# pygame.display.set_icon(apple)
		pygame.display.set_caption("Snake")

		# Lancement de l'initialisation
		self.__initialisation(self)
		# Lancement de la boucle infinie principale
		self.boucle()

	def boucle(self):
		# Lancement de la boucle tant que le jeu est ouvert
		while self.__ouvert:
			# Prétraitement des événements
			self.evenements = {}

			# Pour chaque évenement PyGame, on prémache le boulot
			for e in pygame.event.get():
				if e.type == pygame.KEYDOWN:
					self.evenements[e.type] = e.key
				else:
					self.evenements[e.type] = 0
			
			# Lancement de la boucle utilisateur
			self.__boucle(self)

			# Terminer le dessin du jeu
			self.__rafraichir_ecran()

	# Chargement d'un asset dans PyGame
	def ajouter_image(self, name, path):
		self.images[name] = pygame.image.load(path)

	def effacer_ecran(self):
		# Remplit l'écran de jaune
		self.ecran.fill((255, 255, 0))

		# Si un fond est défini, remplis l'écran avec ce fond
		if self.images["fond"]:
			for x in range(0, ceil(self.largeur / GRILLE)):
				for y in range(0, ceil(self.hauteur / GRILLE)):
					self.ecran.blit(self.images["fond"], (x * GRILLE, y * GRILLE))

	def dessiner(self, image, parametres):
		# Effectue une rotation (éventuelle) de la tile
		sprite = pygame.transform.rotate(self.images[image], parametres.get("rotation", 0))
		# Dessin simple de la sprite à l'écran
		self.ecran.blit(sprite, parametres.get("position", 0))

	def __rafraichir_ecran(self):
		# Rafraichissement de l'écran
		pygame.display.flip()
		# Délai avant la prochaine frame (6 FPS)
		self.horloge.tick(6)

	def quitter(self):
		self.__ouvert = False

	def __position_aleatoire(self):
		# Donne une position sur la zone de jeu
		return (randint(0, ceil(self.largeur / GRILLE)) * GRILLE, randint(0, ceil(self.hauteur / GRILLE)) * GRILLE)

	def position_aleatoire_pomme(self):
		# Stockage de la position de la pomme
		pomme = self.__position_aleatoire()

		# Tant que la pomme est hors-zone, on la change de place
		while self.est_un_bord(pomme):
			pomme = self.__position_aleatoire()

			# Ne pas mettre la pomme sur le serpent
			for morceau in self.serpent.morceaux(self.serpent.taille):
				if self.collision(pomme, morceau.position):
					# Tant que la pomme est sur le joueur, on la change de place
					pomme = self.__position_aleatoire()

		# Retourne la position trouvée
		return DotMap({
			"position": pomme,
			"rotation": 0
		})

	def collision(self, p1, p2):
		# cf. https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection
		return (p1[0] < p2[0] + GRILLE) and (p1[0] + GRILLE > p2[0]) and (p1[1] < p2[1] + GRILLE) and (p1[1] + GRILLE > p2[1])

	def grille(self):
		# Renvoie un itérateur de chaque x et y disponible sur la grille
		for x in range(0, ceil(self.largeur / GRILLE)):
			for y in range(0, ceil(self.hauteur / GRILLE)):
				yield (x * GRILLE, y * GRILLE)

	def est_un_bord(self, position):
		# Fonction de détection de côté de la zone de jeu
		return position[0] == 0 or position[1] == 0 or position[0] >= self.largeur - GRILLE or position[1] >= self.hauteur - GRILLE
