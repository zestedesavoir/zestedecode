########################################
###          Second objectif         ###
###      (c) Zeste de Savoir (c)     ###
###           Licence GPL            ###
###         Auteur : TAlone          ###
########################################

# Ce second objectif à pour objet d'afficher le serpent :
# (sous-objectif 1) - comme un ensemble de corps ;
# (sous-objectif 2) - avec une tête et une queue.

# Import de la bibliothèque pygame (gestion des graphismes)
import pygame
# Import de la bibliothèque du coding gouter (fonctions d'abstraction)
import cg

# Tout le code à écrire sera là-dedans
def main():
	# Création d'une instance de jeu
	jeu = cg.Game()
	# (SO1) Création d'un serpent à l'écran
	snake = cg.Snake()

	# Déclaration des sprites
	jeu.addAsset("Cactus", "assets/cactus.png")
	# (SO1) Ajout du corps
	jeu.addAsset("Corps", "assets/body.png")
	# (SO2) Ajout queue et tête
	jeu.addAsset("Queue", "assets/tail.png")
	jeu.addAsset("Tête", "assets/head.png")

	# Ajout de l'asset spécial qui sera automatiquement mis en fond
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

		# Effacement de l'écran, et remplissage avec les tiles de fond
		jeu.eraseScreen()

		# Dessin de tous les cactus
		for tile in jeu.screenIterator():
			if jeu.isSide(tile):
				jeu.draw(jeu.asset("Cactus"), tile)

		# (SO1) Dessin du serpent à l'écran
		for part in snake.partsIterator():
			# (SO1) Dessin du sprite à l'écran (/!\ hors SO2)
			# jeu.draw(jeu.asset("Corps"), part.position)

			# (SO2) Choix du sprite en fonction de la partie à dessiner et rotation
			if part.type == snake.PARTS.HEAD:
				sprite = jeu.asset("Tête")
			elif part.type == snake.PARTS.TAIL:
				sprite = jeu.asset("Queue")
			else:
				sprite = jeu.asset("Corps")

			# (SO2) Dessin du sprite à l'écran
			jeu.draw(sprite, part.position)

		# Ne pas oublier de terminer la phase de dessin
		jeu.end()

# Lancement de main : pas important
main()
