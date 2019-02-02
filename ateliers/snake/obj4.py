########################################
###         Quatrième objectif       ###
###      (c) Zeste de Savoir (c)     ###
###           Licence GPL            ###
###         Auteur : TAlone          ###
########################################

# Cet objectif voit la pomme apparaitre :
# (sous-objectif 1) - indépendamment du serpent ;
# (sous-objectif 2) - et le serpent peut la manger ;
# (sous-objectif 3) - uniquement dans la zone de jeu (transition).

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
	# (SO1) Ajout de la pomme
	jeu.addAsset("Pomme", "assets/apple.png")

	# Ajout de l'asset spécial qui sera automatiquement mis en fond
	jeu.addAsset("background", "assets/background.png")

	# Variable controlant l'ouverture de la fenêtre
	ouvert = True
	# Par défaut, le serpent ne doit pas bouger
	direction = snake.DIRECTIONS.STOP

	# (SO1) Stockage de la position de la pomme
	pomme = jeu.randomPosition()

	# (SO3) Tant que la pomme est hors-zone, on la change de place
	while jeu.isSide(pomme):
		pomme = jeu.randomPosition()

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

		# (SO1) Dessin de la pomme
		jeu.draw(jeu.asset("Pomme"), pomme)

		# Ne pas oublier de terminer la phase de dessin
		jeu.end()

		# Déplacement du serpent
		snake.move(direction)

		# (SO2) Si il y a collision entre la pomme et la tête du serpent
		if jeu.collision(snake.getHeadPosition(), pomme):
			# (SO2) Le serpent grandit
			snake.grow()
			# (SO2) La pomme change de position
			pomme = jeu.randomPosition()

			# (SO3) Tant que la pomme est hors-zone, on la change de place
			while jeu.isSide(pomme):
				pomme = jeu.randomPosition()

# Lancement de main : pas important
main()
