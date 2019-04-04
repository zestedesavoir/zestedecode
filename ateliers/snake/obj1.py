########################################
###         Premier objectif         ###
###      (c) Zeste de Savoir (c)     ###
###           Licence GPL            ###
###         Auteur : TAlone          ###
########################################

# Le premier objectif consiste en la découverte du fonctionnement de la bibliothèque :
# (sous-objectif 1) - création des variables internes et affichage de la taille du serpent ;
# (sous-objectif 2) - création de la fenêtre de jeu et gestion de la fermeture d'icelle.

# Import de la bibliothèque du coding gouter (fonctions d'abstraction)
from bibliotheque import *

# (OP) Fonction principale d'initialisation
def initialisation(jeu):
	# (SO1) Création d'un serpent à l'écran
	jeu.serpent = Serpent()

	# (SO2) Ajout de l'asset spécial qui sera automatiquement mis en fond
	jeu.ajouter_image("fond", "images/fond.png")

# (OP) Fonction executée regulièrement
def boucle(jeu):
	# (SO1) Déclaration d'une variable contenant la taille du serpent
	taille = jeu.serpent.taille

	# (SO2) Fermeture du jeu lors de l'appui de la croix
	if Evenements.QUITTER in jeu.evenements:
		jeu.quitter()

	# (SO2) Effacement de l'écran, et remplissage avec les tiles de fond
	jeu.effacer_ecran()

	# (SO1) Affichage de la variable de taille
	print(taille)

# (OP) Lancement du jeu à partir des fonctions d'abstraction
Jeu(initialisation, boucle)
