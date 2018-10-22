########################################
###         Troisième objectif       ###
###      (c) Zeste de Savoir (c)     ###
###           Licence GPL            ###
###         Auteur : TAlone          ###
########################################

# Le troisième objectif vise à animer le serpent
# (sous-objectif 1) - en ligne droite ;
# (sous-objectif 2) - dans les autres directions ;
# (sous-objectif 3) - avec les rotations qui s'imposent.

# Import de la bibliothèque pygame (gestion des graphismes)
import pygame
# Import de la bibliothèque du coding gouter (fonctions d'abstraction)
import cg

# Tout le code à écrire sera là-dedans
def main():
	# Création d'une instance de jeu
	jeu = cg.Game()
	# Création d'un serpent à l'écran
	snake = cg.Snake()

	# Déclaration des sprites
	jeu.addAsset("Cactus", "assets/cactus.png")
	# Ajout du corps
	jeu.addAsset("Corps", "assets/body.png")
	# Ajout queue et tête
	jeu.addAsset("Queue", "assets/tail.png")
	jeu.addAsset("Tête", "assets/head.png")

	# Ajout de l'asset spécial qui sera automatiquement mis en fond
	jeu.addAsset("background", "assets/background.png")

	# Variable controlant l'ouverture de la fenêtre
	ouvert = True
	# (SO1) Par défaut, le serpent ne doit pas bouger
	direction = snake.DIRECTIONS.STOP

	# Boucle principale du jeu
	while ouvert:
		# Récupération des événements de la file d'attente
		for event in pygame.event.get():
			# Si l'utilisateur veut quitter...
			if event.type == pygame.QUIT:
				# ...sortie de la boucle principale, et fermeture du jeu.
				ouvert = False
			# (SO1) Lorsqu'une touche est appuyée...
			if event.type == pygame.KEYDOWN:
				# (SO1) ...on vérifie la direction droite...
				if event.key == pygame.K_RIGHT:
					direction = snake.DIRECTIONS.RIGHT
				# (SO2) ...et les autres directions.
				elif event.key == pygame.K_UP:
					direction = snake.DIRECTIONS.TOP
				elif event.key == pygame.K_DOWN:
					direction = snake.DIRECTIONS.BOTTOM
				elif event.key == pygame.K_LEFT:
					direction = snake.DIRECTIONS.LEFT

		# Effacement de l'écran, et remplissage avec les tiles de fond
		jeu.eraseScreen()

		# Dessin de tous les cactus
		for tile in jeu.screenIterator():
			if jeu.isSide(tile):
				jeu.draw(jeu.asset("Cactus"), tile)

		# Dessin du serpent à l'écran
		for part in snake.partsIterator():
			# Choix du sprite en fonction de la partie à dessiner et rotation
			if part.type == snake.PARTS.HEAD:
				# (SO3) Rotation de la tête
				sprite = jeu.asset("Tête", part.rotation)
			elif part.type == snake.PARTS.TAIL:
				# (SO3) Idem
				sprite = jeu.asset("Queue", part.rotation)
			else:
				# (SO3) Idem
				sprite = jeu.asset("Corps", part.rotation)

			# Dessin du sprite à l'écran
			jeu.draw(sprite, part.position)

		# Ne pas oublier de terminer la phase de dessin
		jeu.end()

		# (SO1) Déplacement du serpent
		snake.move(direction)

# Lancement de main : pas important
main()
