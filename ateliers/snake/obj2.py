########################################
###          Second objectif         ###
###      (c) Zeste de Savoir (c)     ###
###           Licence GPL            ###
###         Auteur : TAlone          ###
########################################

# Ce second objectif à pour objet d'afficher les bordures et le serpent :
# (sous-objectif 1) - affichage des cactus ;
# (sous-objectif 2) - affichage du serpent comme un ensemble de corps ;
# (sous-objectif 3) - affichage du serpent avec une tête et une queue.

# Import de la bibliothèque pygame (gestion des graphismes)
import pygame
# Import de la bibliothèque du coding gouter (fonctions d'abstraction)
import cg

# Fonction principale d'initialisation
def init(jeu):
	# Création d'un serpent à l'écran
	jeu.snake = cg.Snake()

	# (SO1) Déclaration du cactus
	jeu.addAsset("Cactus", "assets/cactus.png")

	# (SO2) Ajout du corps
	jeu.addAsset("Corps", "assets/body.png")
	# (SO3) Ajout de la queue
	jeu.addAsset("Queue", "assets/tail.png")
	# (SO3) Ajout de la tête
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

	# Effacement de l'écran, et remplissage avec les tiles de fond
	jeu.eraseScreen()

	# (SO1) Itération sur tous les morceaux de grille
	for carreau in jeu.screenIterator():
		# (SO1) Si l'on est sur un côté...
		if jeu.isSide(carreau):
			# (SO1) ...dessine un cactus
			jeu.draw("Cactus", { "position": carreau })

	# (SO2) Dessin d'un certain nombre de morceaux à l'écran
	for partie in jeu.snake.partsIterator(taille):
		# (SO3) Choix du sprite en fonction de la partie à dessiner et dessin à l'écran
		if partie.type == jeu.snake.PARTS.HEAD:
			jeu.draw("Tête", partie)
		elif partie.type == jeu.snake.PARTS.TAIL:
			jeu.draw("Queue", partie)
		else:
			# (SO2) Dessin du corps
			jeu.draw("Corps", partie)

# Lancement du jeu à partir des fonctions d'abstraction
cg.Game(init, boucle)
