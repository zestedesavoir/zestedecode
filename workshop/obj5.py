########################################
###         Cinquième objectif       ###
###      (c) Zeste de Savoir (c)     ###
###           Licence GPL            ###
###         Auteur : TAlone          ###
########################################

# Le cinquième objectif gère les collisions :
# (sous-objectif 1) - contre les bords de la zone ;
# (sous-objectif 2) - du serpent avec lui-même ;
# (sous-objectif 3) - des pommes avec le corps du serpent (bonus: fonctions).

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
	# Ajout de la pomme
	jeu.addAsset("Pomme", "assets/apple.png")

	# Ajout de l'asset spécial qui sera automatiquement mis en fond
	jeu.addAsset("background", "assets/background.png")

	# Variable controlant l'ouverture de la fenêtre
	ouvert = True
	# Par défaut, le serpent ne doit pas bouger
	direction = snake.DIRECTIONS.STOP

	# Stockage de la position de la pomme
	pomme = jeu.randomPosition()

	# Tant que la pomme est hors-zone, on la change de place
	while jeu.isSide(pomme):
		pomme = jeu.randomPosition()

	# (SO3) Fonction pour faire apparaitre la pomme
	#def spawnPomme():
	#	# Stockage de la position de la pomme
	#	pomme = jeu.randomPosition()
	#
	#	# Tant que la pomme est hors-zone, on la change de place
	#	while jeu.isSide(pomme):
	#		pomme = jeu.randomPosition()
	#
	#		# (SO3) Ne pas mettre la pomme sur le serpent
	#		for part in snake.partsIterator():
	#			if jeu.collision(pomme, part.position):
	#				# (SO3) Tant que la pomme est sur le joueur, on la change de place
	#				pomme = jeu.randomPosition()
	#
	#	# (SO3) Retourne la position trouvée
	#	return pomme

	# (SO3) Ajout de la pomme
	#pomme = spawnPomme()

	# Boucle principale du jeu
	while ouvert:
		# Récupération des événements de la file d'attente
		for event in pygame.event.get():
			# Si l'utilisateur veut quitter...
			if event.type == pygame.QUIT:
				# ...sortie de la boucle principale, et fermeture du jeu.
				ouvert = False
			# Lorsqu'une touche est appuyée...
			if event.type == pygame.KEYDOWN:
				# ...on vérifie la direction droite...
				if event.key == pygame.K_RIGHT:
					direction = snake.DIRECTIONS.RIGHT
				# ...et les autres directions.
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
				# Rotation de la tête
				sprite = jeu.asset("Tête", part.rotation)
			elif part.type == snake.PARTS.TAIL:
				sprite = jeu.asset("Queue", part.rotation)
			else:
				sprite = jeu.asset("Corps", part.rotation)

			# Dessin du sprite à l'écran
			jeu.draw(sprite, part.position)

		# Dessin de la pomme
		jeu.draw(jeu.asset("Pomme"), pomme)

		# Ne pas oublier de terminer la phase de dessin
		jeu.end()

		# Déplacement du serpent
		snake.move(direction)

		# Si il y a collision entre la pomme et la tête du serpent
		if jeu.collision(snake.getHeadPosition(), pomme):
			# Le serpent grandit
			snake.grow()
			# La pomme change de position
			# (SO3) Ajout de la pomme
			#pomme = spawnPomme()
			pomme = jeu.randomPosition()

			# Tant que la pomme est hors-zone, on la change de place
			while jeu.isSide(pomme):
				pomme = jeu.randomPosition()

		# (SO1) Vérifie que le serpent soit toujours à l'écran
		for tile in jeu.screenIterator():
			if jeu.isSide(tile) and jeu.collision(snake.getHeadPosition(), tile):
				# (SO1) Ferme le jeu si collision avec un mur
				ouvert = False

		# (SO2) Vérifie que le serpent ne se mord pas
		for part in snake.partsIterator():
			# (SO2) Attention : la tête est incluse, il faut donc la retirer
			if jeu.collision(snake.getHeadPosition(), part.position) and part.type != snake.PARTS.HEAD:
				# (SO2) Ferme le jeu si le serpent se rentre dedans
				ouvert = False

# Lancement de main : pas important
main()
