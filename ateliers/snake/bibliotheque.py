########################################
###        Bibliothèque Snake        ###
###      (c) Zeste de Savoir (c)     ###
###           Licence GPL            ###
###    Auteurs : TAlone, Situphen    ###
########################################

# Import des bibliothèques pygame et dotmap (faire attention à les installer: pip install pygame dotmap)
import pygame
import pygame.freetype
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
	"FLECHE_BAS": pygame.K_DOWN,
	"ESPACE": pygame.K_SPACE
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

	# Liste des directions de rotations possibles
	ROTATIONS = DotMap({
		"HORAIRE": 90,
		"ANTI_HORAIRE": 270
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
		self.__sX = [initX, initX - GRILLE, initX - 2 * GRILLE]
		self.__sY = [initY, initY, initY]
		# Rotations des morceaux de serpent
		self.__sR = [0, 0, 0]

	def __avancer_serpent(self):
		# Avancement du corps du serpent : chaque morceau prend la position du précédent
		for i in range(len(self.__sX) - 1, 0, -1):
			self.__sX[i] = self.__sX[i - 1]
			self.__sY[i] = self.__sY[i - 1]
			self.__sR[i] = self.__sR[i - 1]
		
		# Forcer la queue à être orientée comme le corps juste avant
		self.__sR[len(self.__sX) - 1] = self.__sR[len(self.__sX) - 2]

	def deplacer(self, direction, pas=GRILLE):
		# D'abord, bouger tout le corps
		if direction != self.DIRECTIONS.STOP: self.__avancer_serpent()

		# Puis mettre à jour la tête selon la direction souhaitée
		if direction == self.DIRECTIONS.DROITE:
			self.__sX[0] += pas
		elif direction == self.DIRECTIONS.GAUCHE:
			self.__sX[0] -= pas
		elif direction == self.DIRECTIONS.BAS:
			self.__sY[0] += pas
		elif direction == self.DIRECTIONS.HAUT:
			self.__sY[0] -= pas

		# Les rotations sont plus simples grâce aux constantes
		self.__sR[0] = 90 * direction

	def morceaux(self, longueur):
		# Vérifions que les participants ne fassent pas n'importe quoi
		if(longueur > len(self.__sX)):
			longueur = self.taille

		# Pour chaque partie du corps...
		for i in range(longueur, 0, -1):
			# ...on regarde d'abord le type...
			type = self.PARTIES.CORPS
			if i == 1: type = self.PARTIES.TETE
			elif i == len(self.__sX): type = self.PARTIES.QUEUE

			# ...puis on déduit le sens de la rotation...
			direction_rotation = self.__sR[i - 1] - self.__sR[i - 2]

			# Dans certains cas, la rotation ne tombe pas juste
			# il faut donc l'ajuster
			if direction_rotation < 0:
				direction_rotation += 360

			# ...avant de donner les informations nécessaires.
			yield DotMap({
				"position": (self.__sX[i - 1], self.__sY[i - 1]),
				"rotation": self.__sR[i - 1],
				"direction_rotation": direction_rotation,
				"type": type
			})
	
	# NOTE: la taille ne doit pas pouvoir être modifiée directement par l'utilisateur
	@property
	def taille(self):
		return len(self.__sX)

	def grandir(self):
		# On regarde d'abord la direction de la dernière partie du serpent
		direction = self.__sR[len(self.__sR) - 1] / 90

		# On ajoute une composante de rotation similaire
		self.__sR.append(direction * 90)

		# En fonction de la direction, il faut ajouter la composante à différents endroits
		if direction == self.DIRECTIONS.DROITE:
			self.__sX.append(self.__sX[len(self.__sX) - 1] - GRILLE)
			self.__sY.append(self.__sY[len(self.__sY) - 1])
		elif direction == self.DIRECTIONS.GAUCHE:
			self.__sX.append(self.__sX[len(self.__sX) - 1] + GRILLE)
			self.__sY.append(self.__sY[len(self.__sY) - 1])
		elif direction == self.DIRECTIONS.BAS:
			self.__sX.append(self.__sX[len(self.__sX) - 1])
			self.__sY.append(self.__sY[len(self.__sY) - 1] - GRILLE)
		elif direction == self.DIRECTIONS.HAUT:
			self.__sX.append(self.__sX[len(self.__sX) - 1])
			self.__sY.append(self.__sY[len(self.__sY) - 1] + GRILLE)

	# NOTE: la position de la tete ne doit pas pouvoir être modifiée directement par l'utilisateur
	@property
	def position_tete(self):
		# Donne la position de la tête du serpent
		return (self.__sX[0], self.__sY[0])

class Jeu:
	def __init__(self, initialisation=None, boucle=None, largeur=LARGEUR, hauteur=HAUTEUR):
		# Initialisation de PyGame
		pygame.init()

		# Initialisation du texte
		pygame.freetype.init()

		# Déclarations des paramètres facultatifs (fonctions du jeu)
		if initialisation is None:
			def initialisation(jeu):
				return

		if boucle is None:
			def boucle(jeu):
				return

		# Ajout des dimensions (modifiables)
		self.largeur = largeur
		self.hauteur = hauteur

		# Ajout des variables internes
		self.__images = { }
		self.__ecran = pygame.display.set_mode((largeur, hauteur))
		self.__horloge = pygame.time.Clock()
		self.__ouvert = True
		self.__initialisation = initialisation
		self.__boucle = boucle

		# Initialisation des polices
		# NOTE: cette fonction peut être de nouveau appelée ultérieurement pour changer les paramètres
		self.init_text()

		# Un peu d'esthétique
		pygame.display.set_caption("Snake")

		# Lancement de l'initialisation
		self.__initialisation(self)
		# Lancement de la boucle infinie principale
		self.boucle()

	def init_text(self, font="sans-serif", size=32):
		self.__police = pygame.freetype.SysFont(font, size)

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

			if self.__ouvert:
				# Terminer le dessin du jeu
				self.__rafraichir_ecran()

	# Chargement d'un asset dans PyGame
	def ajouter_image(self, name, path):
		self.__images[name] = pygame.image.load(path)

	def ajouter_texte(self, name, text):
		self.__images[name] = self.__police.render(text, (0, 0, 0))[0]

	def effacer_ecran(self):
		# Remplit l'écran de jaune
		self.__ecran.fill((255, 255, 0))

		# Si un fond est défini, remplis l'écran avec ce fond
		if self.__images["fond"]:
			for x in range(0, ceil(self.largeur / GRILLE)):
				for y in range(0, ceil(self.hauteur / GRILLE)):
					self.__ecran.blit(self.__images["fond"], (x * GRILLE, y * GRILLE))

	def dessiner(self, image, parametres):
		# Effectue une rotation (éventuelle) de la tile
		sprite = pygame.transform.rotate(self.__images[image], parametres.get("rotation", 0))
		# Dessin simple de la sprite à l'écran
		self.__ecran.blit(sprite, parametres.get("position", 0))

	def __rafraichir_ecran(self):
		# Rafraichissement de l'écran
		pygame.display.flip()
		# Délai avant la prochaine frame (6 FPS)
		self.__horloge.tick(6)

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
