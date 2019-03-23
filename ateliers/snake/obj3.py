########################################
###         Troisième objectif       ###
###      (c) Zeste de Savoir (c)     ###
###           Licence GPL            ###
###         Auteur : TAlone          ###
########################################

# Le troisième objectif vise à animer le serpent
# (sous-objectif 1) - en ligne droite ;
# (sous-objectif 2) - dans les autres directions.

# Import de la bibliothèque pygame (gestion des graphismes)
import pygame
# Import de la bibliothèque du coding gouter (fonctions d'abstraction)
import cg

# Fonction principale d'initialisation
def init(jeu):
	# Création d'un serpent à l'écran
	jeu.snake = cg.Snake()

	# (SO1) Donne une direction par défaut au serpent
	jeu.snakeDir = jeu.snake.DIRECTIONS.STOP

	# Déclaration du cactus
	jeu.addAsset("Cactus", "assets/cactus.png")

	# Ajout du corps
	jeu.addAsset("Corps", "assets/body.png")
	# Ajout de la queue
	jeu.addAsset("Queue", "assets/tail.png")
	# Ajout de la tête
	jeu.addAsset("Tête", "assets/head.png")

	# Ajout de l'asset spécial qui sera automatiquement mis en fond
	jeu.addAsset("background", "assets/background.png")

# Fonction executée regulièrement
def boucle(jeu):
	# Déclaration d'une variable contenant la taile du serpent
	taille = jeu.snake.size()

	# Fermeture du jeu lors de l'appui de la croix
	if pygame.QUIT in jeu.events:
		jeu.end()

	# (SO1) Lorsqu'une touche est appuyée
	if pygame.KEYDOWN in jeu.events:
		# (SO1) On stocke la touche appuyée
		touche = jeu.events[pygame.KEYDOWN]

		# (SO1) ...on vérifie la direction droite...
		if touche == pygame.K_RIGHT:
			jeu.snakeDir = jeu.snake.DIRECTIONS.RIGHT
		# (SO2) ...et les autres directions.
		elif touche == pygame.K_UP:
			jeu.snakeDir = jeu.snake.DIRECTIONS.TOP
		elif touche == pygame.K_DOWN:
			jeu.snakeDir = jeu.snake.DIRECTIONS.BOTTOM
		elif touche == pygame.K_LEFT:
			jeu.snakeDir = jeu.snake.DIRECTIONS.LEFT

	# Effacement de l'écran, et remplissage avec les tiles de fond
	jeu.eraseScreen()

	# Itération sur tous les morceaux de grille
	for carreau in jeu.screenIterator():
		# (SO1) Si l'on est sur un côté...
		if jeu.isSide(carreau):
			# (SO1) ...dessine un cactus
			jeu.draw("Cactus", { "position": carreau })

	# Dessin d'un certain nombre de morceaux à l'écran
	for partie in jeu.snake.partsIterator(taille):
		# Choix du sprite en fonction de la partie à dessiner et dessin à l'écran
		if partie.type == jeu.snake.PARTS.HEAD:
			jeu.draw("Tête", partie)
		elif partie.type == jeu.snake.PARTS.TAIL:
			jeu.draw("Queue", partie)
		else:
			# Dessin du corps
			jeu.draw("Corps", partie)

	# (SO1) Déplacement du serpent
	jeu.snake.move(jeu.snakeDir)

# Lancement du jeu à partir des fonctions d'abstraction
cg.Game(init, boucle)
