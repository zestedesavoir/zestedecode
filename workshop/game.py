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
	jeu.addAsset("Pomme", "apple.png")
	jeu.addAsset("Corps", "body.png")
	jeu.addAsset("Queue", "tail.png")
	jeu.addAsset("Tête", "head.png")

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

		# Premièrement, effaçons l'écran
		jeu.eraseScreen()

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

		if jeu.collision(snake.getHeadPosition(), pomme):
			snake.grow()
			pomme = jeu.randomPosition()

		# Vérifie que le serpent soit toujours à l'écran
		#if snakeX[0] >= (WIDTH - 32) or snakeX[0] <= 0:
		#	stepX = 0
		#if snakeY[0] >= (HEIGHT - 32) or snakeY[0] <= 0:
		#	stepY = 0



# Run the main function only if this module is executed as the main script
if __name__ == "__main__":
	main()
