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

# Import de la bibliothèque du coding gouter (fonctions d'abstraction)
from bibliotheque import *

# Fonction principale d'initialisation
def initialisation(jeu):
	# Création d'un serpent à l'écran
	jeu.serpent = Serpent()

	# (SO1) Déclaration du cactus
	jeu.ajouter_image("Cactus", "images/cactus.png")

	# (SO2) Ajout du corps
	jeu.ajouter_image("Corps", "images/corps.png")
	# (SO3) Ajout de la queue
	jeu.ajouter_image("Queue", "images/queue.png")
	# (SO3) Ajout de la tête
	jeu.ajouter_image("Tête", "images/tete.png")

	# Ajout de l'asset spécial qui sera automatiquement mis en fond
	jeu.ajouter_image("fond", "images/fond.png")

# Fonction executée regulièrement
def boucle(jeu):
	# Déclaration d'une variable contenant la taille du serpent
	taille = jeu.serpent.taille

	# Fermeture du jeu lors de l'appui de la croix
	if Evenements.QUITTER in jeu.evenements:
		jeu.quitter()

	# Effacement de l'écran, et remplissage avec les tiles de fond
	jeu.effacer_ecran()

	# (SO1) Itération sur tous les morceaux de grille
	for carreau in jeu.grille():
		# (SO1) Si l'on est sur un côté...
		if jeu.est_un_bord(carreau):
			# (SO1) ...dessine un cactus
			jeu.dessiner("Cactus", { "position": carreau })

	# (SO2) Dessin d'un certain nombre de morceaux à l'écran
	for morceau in jeu.serpent.morceaux(taille):
		# (SO3) Choix du sprite en fonction de la partie à dessiner et dessin à l'écran
		if morceau.type == jeu.serpent.PARTIES.TETE:
			jeu.dessiner("Tête", morceau)
		elif morceau.type == jeu.serpent.PARTIES.QUEUE:
			jeu.dessiner("Queue", morceau)
		else:
			# (SO2) Dessin du corps
			jeu.dessiner("Corps", morceau)

# Lancement du jeu à partir des fonctions d'abstraction
Jeu(initialisation, boucle)
