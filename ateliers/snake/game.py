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

# Fonction principale d'initialisation
def init(jeu):
	# Création d'un serpent à l'écran
	jeu.snake = cg.Snake()

	# Déclaration des sprites
	jeu.addAsset("Cactus", "assets/cactus.png")
	# Ajout du corps
	jeu.addAsset("Corps", "assets/body.png")
	# Ajout de la queue
	jeu.addAsset("Queue", "assets/tail.png")
	# Ajout de la tête
	jeu.addAsset("Tête", "assets/head.png")
	# Ajout de la pomme
	jeu.addAsset("Pomme", "assets/apple.png")

	# Ajout de l'asset spécial qui sera automatiquement mis en fond
	jeu.addAsset("background", "assets/background.png")

	# Par défaut, le serpent ne doit pas bouger
	jeu.snakeDir = jeu.snake.DIRECTIONS.STOP

	# Choix d'une position initiale pour la pomme
	jeu.pommePos = jeu.randomApplePosition()

def boucle(jeu):
	################################
	###  Gestion des évenements  ###
	################################

	# Lorsque l'on veut quitter le jeu
	if pygame.QUIT in jeu.events:
		jeu.end()

	# Lorsqu'une touche est appuyée
	if pygame.KEYDOWN in jeu.events:
		# On stocke la touche appuyée
		touche = jeu.events[pygame.KEYDOWN]

		# ...on vérifie la direction droite...
		if touche == pygame.K_RIGHT:
			jeu.snakeDir = jeu.snake.DIRECTIONS.RIGHT
		# ...et les autres directions.
		elif touche == pygame.K_UP:
			jeu.snakeDir = jeu.snake.DIRECTIONS.TOP
		elif touche == pygame.K_DOWN:
			jeu.snakeDir = jeu.snake.DIRECTIONS.BOTTOM
		elif touche == pygame.K_LEFT:
			jeu.snakeDir = jeu.snake.DIRECTIONS.LEFT

	################################
	###     Phase de dessin      ###
	################################

	# Effacement de l'écran, et remplissage avec les tiles de fond
	jeu.eraseScreen()

	# Itération sur tous les morceaux de grille
	for carreau in jeu.screenIterator():
		# Si l'on est sur un côté...
		if jeu.isSide(carreau):
			# ...dessine un cactus
			jeu.draw("Cactus", carreau)

	# Dessin du serpent à l'écran
	for partie in jeu.snake.partsIterator():
		# Choix du sprite en fonction de la partie à dessiner et dessin à l'écran
		if partie.type == jeu.snake.PARTS.HEAD:
			jeu.draw("Tête", partie.position, partie.rotation)
		elif partie.type == jeu.snake.PARTS.TAIL:
			jeu.draw("Queue", partie.position, partie.rotation)
		else:
			jeu.draw("Corps", partie.position, partie.rotation)

	# Dessin de la pomme
	jeu.draw("Pomme", jeu.pommePos)

	# Ne pas oublier de terminer la phase de dessin
	jeu.endDraw()

	################################
	### Déplacement et collision ###
	################################

	# Déplacement du serpent
	jeu.snake.move(jeu.snakeDir)

	# Si il y a collision entre la pomme et la tête du serpent
	if jeu.collision(jeu.snake.getHeadPosition(), jeu.pommePos):
		# Le serpent grandit
		jeu.snake.grow()
		# La pomme change de position
		jeu.pommePos = jeu.randomApplePosition()

	# Vérifie que le serpent soit toujours à l'écran
	for carreau in jeu.screenIterator():
		if jeu.isSide(carreau) and jeu.collision(jeu.snake.getHeadPosition(), carreau):
			# Ferme le jeu si collision avec un mur
			jeu.end()

	# Vérifie que le serpent ne se mord pas
	for partie in jeu.snake.partsIterator():
		# Attention : la tête est incluse, il faut donc la retirer
		if jeu.collision(jeu.snake.getHeadPosition(), partie.position) and partie.type != jeu.snake.PARTS.HEAD:
			# Ferme le jeu si le serpent se rentre dedans
			jeu.end()

# Lancement du jeu seulement si le fichier n'est pas importé comme module
if __name__ == "__main__":
	cg.Game(init, boucle)
