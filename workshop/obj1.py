########################################
###         Premier objectif         ###
###      (c) Zeste de Savoir (c)     ###
###           Licence GPL            ###
###         Auteur : TAlone          ###
########################################

# Le premier objectif consiste à remplir la zone de jeu :
# (sous-objectif 1) - du fond de grille ;
# (sous-objectif 2) - des cactus sur les bords.

# Import de la bibliothèque pygame (gestion des graphismes)
import pygame
# Import de la bibliothèque du coding gouter (fonctions d'abstraction)
import cg

# Tout le code à écrire sera là-dedans
def main():
	# Création d'une instance de jeu
	jeu = cg.Game()

	# (SO2) Déclaration des sprites
	jeu.addAsset("Cactus", "assets/cactus.png")

	# (SO1) Ajout de l'asset spécial qui sera automatiquement mis en fond
	jeu.addAsset("background", "assets/background.png")

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

		# (SO1) Effacement de l'écran, et remplissage avec les tiles de fond
		jeu.eraseScreen()

		# (SO2) Dessin de tous les cactus
		for tile in jeu.screenIterator():
			if jeu.isSide(tile):
				jeu.draw(jeu.asset("Cactus"), tile)

		# (SO1) Ne pas oublier de terminer la phase de dessin
		jeu.end()

# Lancement de main : pas important
main()
