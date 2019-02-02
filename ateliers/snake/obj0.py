########################################
###          Code de départ          ###
###      (c) Zeste de Savoir (c)     ###
###           Licence GPL            ###
###         Auteur : TAlone          ###
########################################

# L'objectif de base est simple : afficher une fenêtre à l'écran,
# il s'agit du seul objectif qui sera commun, et dont on leur donnera le code.
# La fenêtre doit pouvoir être fermée, sans quoi il faut aller à la console et Ctrl+C.

# Import de la bibliothèque pygame (gestion des graphismes)
import pygame
# Import de la bibliothèque du coding gouter (fonctions d'abstraction)
import cg

# Tout le code à écrire sera là-dedans
def main():
	# Création d'une instance de jeu
	jeu = cg.Game()

	# Variable controlant l'ouverture de la fenêtre
	ouvert = True

	# Boucle principale du jeu
	while ouvert:
		# Récupération des événements de la file d'attente
		for event in pygame.event.get():
			# Si l'utilisateur veut quitter...
			if event.type == pygame.QUIT:
				# ...sortie de la boucle principale, et fermeture du jeu.
				ouvert = False

# Lancement de main : pas important
main()
