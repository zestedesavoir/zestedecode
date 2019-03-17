########################################
###         Premier objectif         ###
###      (c) Zeste de Savoir (c)     ###
###           Licence GPL            ###
###         Auteur : TAlone          ###
########################################

# Le premier objectif consiste en la découverte du fonctionnement de la bibliothèque :
# (sous-objectif 1) - création des variables internes et affichage de la taille du serpent ;
# (sous-objectif 2) - création de la fenêtre de jeu et gestion de la fermeture d'icelle.

# Import de la bibliothèque pygame (gestion des graphismes)
import pygame
# Import de la bibliothèque du coding gouter (fonctions d'abstraction)
import cg

# (OP) Fonction principale d'initialisation
def init(jeu):
	# (SO1) Création d'un serpent à l'écran
	jeu.snake = cg.Snake()

	# (SO2) Ajout de l'asset spécial qui sera automatiquement mis en fond
	jeu.addAsset("background", "assets/background.png")

# (OP) Fonction executée regulièrement
def boucle(jeu):
	# (SO1) Déclaration d'une variable contenant la taile du serpent
	taille = jeu.snake.size()

	# (SO2) Fermeture du jeu lors de l'appui de la croix
	if pygame.QUIT in jeu.events:
		jeu.end()

	# (SO2) Effacement de l'écran, et remplissage avec les tiles de fond
	jeu.eraseScreen()

	# (SO1) Affichage de la variable de taille
	print(taille)

	# (SO2) Ne pas oublier de terminer la phase de dessin
	jeu.endDraw()

# (OP) Lancement du jeu à partir des fonctions d'abstraction
cg.Game(init, boucle)
