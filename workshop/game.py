########################################
###       Corrigé complet Snake      ###
###      (c) Zeste de Savoir (c)     ###
###           Licence GPL            ###
###         Auteur : TAlone          ###
########################################

# Import de la bibliothèque pygame (gestion des graphismes)
import pygame
# Import de la bibliothèque du coding gouter (fonctions d'abstraction)
import cg

def main():
	# Création d'une instance de jeu
	jeu = cg.Game()
	# Création d'un serpent à l'écran
	snake = cg.Snake()

	# Déclaration des sprites
	jeu.addAsset("Cactus", "assets/cactus.png")
	jeu.addAsset("Pomme", "assets/apple.png")
	jeu.addAsset("Corps", "assets/body.png")
	jeu.addAsset("Queue", "assets/tail.png")
	jeu.addAsset("Tête", "assets/head.png")

	# Asset spécial qui sera automatiquement mis en fond
	jeu.addAsset("background", "assets/background.png")

	# Variable pour contrôler la boucle principale
	running = True
	# Par défaut, le serpent ne doit pas bouger
	direction = snake.DIRECTIONS.STOP

	# Stockage de la position de la pomme
	pomme = jeu.randomPosition()

	# Boucle principale du jeu
	while running:
		# Récupération des événements de la file d'attente
		for event in pygame.event.get():
			# Si l'utilisateur veut quitter...
			if event.type == pygame.QUIT:
				# ...sortie de la boucle principale, et fermeture du jeu.
				running = False
			# Lorsqu'une touche est appuyée...
			if event.type == pygame.KEYDOWN:
				# ...on vérifie les quatre flèches directionnelles pour donner au serpent sa direction.
				if event.key == pygame.K_UP:
					direction = snake.DIRECTIONS.TOP
				elif event.key == pygame.K_DOWN:
					direction = snake.DIRECTIONS.BOTTOM
				elif event.key == pygame.K_LEFT:
					direction = snake.DIRECTIONS.LEFT
				elif event.key == pygame.K_RIGHT:
					direction = snake.DIRECTIONS.RIGHT

		# Premièrement, effacement de l'écran
		jeu.eraseScreen()

		# Dessin de tous les cactus
		for tile in jeu.screenIterator():
			if jeu.isSide(tile):
				jeu.draw(jeu.asset("Cactus"), tile)

		# Dessin du serpent à l'écran
		for part in snake.partsIterator():
			# Choix du sprite en fonction de la partie à dessiner et rotation
			if part.type == snake.PARTS.HEAD:
				sprite = jeu.asset("Tête", part.rotation)
			elif part.type == snake.PARTS.TAIL:
				sprite = jeu.asset("Queue", part.rotation)
			else:
				sprite = jeu.asset("Corps", part.rotation)

			# Dessin du sprite tourné à l'écran
			jeu.draw(sprite, part.position)

		# Dessin de la pomme
		jeu.draw(jeu.asset("Pomme"), pomme)

		# Terminer la phase de dessin
		jeu.end()

		# Déplacement du serpent
		snake.move(direction)

		# Si il y a collision entre la pomme et la tête du serpent
		if jeu.collision(snake.getHeadPosition(), pomme):
			# Le serpent grandit
			snake.grow()
			# La pomme change de position
			pomme = jeu.randomPosition()

			# Tant que la pomme est hors-zone, on la change de place
			while jeu.isSide(pomme):
				pomme = jeu.randomPosition()

		# Vérifie que le serpent soit toujours à l'écran
		for tile in jeu.screenIterator():
			if jeu.isSide(tile) and jeu.collision(snake.getHeadPosition(), tile):
				# Ferme le jeu si collision avec un mur
				running = 0

		# Vérifie que le serpent ne se mord pas
		for part in snake.partsIterator():
			# Attention : la tête est incluse, il faut donc la retirer
			if jeu.collision(snake.getHeadPosition(), part.position) and part.type != snake.PARTS.HEAD:
				# Ferme le jeu si le serpent se rentre dedans
				running = 0

# Run the main function only if this module is executed as the main script
if __name__ == "__main__":
	main()
