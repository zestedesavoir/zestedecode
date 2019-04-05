########################################
###         Quatrième objectif       ###
###      (c) Zeste de Savoir (c)     ###
###           Licence GPL            ###
###         Auteur : TAlone          ###
########################################

# Il est dans ce quatrième objectif question des collisions :
# (sous-objectif 1) - objectif intermédiaire visant à ajouter la pomme ;
# (sous-objectif 2) - entre le serpent et la pomme ;
# (sous-objectif 3) - entre le serpent et le bord ;
# (sous-objectif 4) - entre le serpent et lui-même.

# Import de la bibliothèque du coding gouter (fonctions d'abstraction)
from bibliotheque import *

# Fonction principale d'initialisation
def initialisation(jeu):
	# Création d'un serpent à l'écran
	jeu.serpent = Serpent()

	# (SO1) Création d'une pomme
	jeu.pomme = jeu.position_aleatoire_pomme()

	# Donne une direction par défaut au serpent
	jeu.direction_serpent = jeu.serpent.DIRECTIONS.STOP

	# Déclaration du cactus
	jeu.ajouter_image("Cactus", "images/cactus.png")
	# (SO1) Déclaration de la pomme
	jeu.ajouter_image("Pomme", "images/pomme.png")

	# Ajout du corps
	jeu.ajouter_image("Corps", "images/corps.png")
	# Ajout de la queue
	jeu.ajouter_image("Queue", "images/queue.png")
	# Ajout de la tête
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

	# Lorsqu'une touche est appuyée
	if Evenements.TOUCHE_APPUYEE in jeu.evenements:
		# On stocke la touche appuyée
		touche = jeu.evenements[Evenements.TOUCHE_APPUYEE]

		# ...on vérifie la direction droite...
		if touche == Touches.FLECHE_DROITE:
			jeu.direction_serpent = jeu.serpent.DIRECTIONS.DROITE
		# ...et les autres directions.
		elif touche == Touches.FLECHE_HAUT:
			jeu.direction_serpent = jeu.serpent.DIRECTIONS.HAUT
		elif touche == Touches.FLECHE_BAS:
			jeu.direction_serpent = jeu.serpent.DIRECTIONS.BAS
		elif touche == Touches.FLECHE_GAUCHE:
			jeu.direction_serpent = jeu.serpent.DIRECTIONS.GAUCHE

	# (SO2) Si il y a collision entre la pomme et la tête du serpent
	if jeu.collision(jeu.serpent.position_tete, jeu.pomme.position):
		# (SO2) Le serpent grandit
		jeu.serpent.grandir()
		# (SO2) La pomme change de position
		jeu.pomme = jeu.position_aleatoire_pomme()

	# Effacement de l'écran, et remplissage avec les tiles de fond
	jeu.effacer_ecran()

	# Itération sur tous les morceaux de grille
	for carreau in jeu.grille():
		# Si l'on est sur un côté...
		if jeu.est_un_bord(carreau):
			# ...dessine un cactus
			jeu.dessiner("Cactus", { "position": carreau })

			# (SO3) Si le coin est en contact avec la tête du serpent
			if jeu.collision(carreau, jeu.serpent.position_tete):
				# (SO3) Ferme le jeu si il y a contact entre la tête et un bord
				jeu.quitter()

	# Dessin d'un certain nombre de morceaux à l'écran
	for morceau in jeu.serpent.morceaux(taille):
		# Choix du sprite en fonction de la partie à dessiner et dessin à l'écran
		if morceau.type == jeu.serpent.PARTIES.TETE:
			jeu.dessiner("Tête", morceau)
		elif morceau.type == jeu.serpent.PARTIES.QUEUE:
			jeu.dessiner("Queue", morceau)
		else:
			# Dessin du corps
			jeu.dessiner("Corps", morceau)

		# (SO4) Vérification que le serpent ne se mord pas
		# Attention : la tête est incluse, il faut donc la retirer
		if jeu.collision(jeu.serpent.position_tete, morceau.position) and morceau.type != jeu.serpent.PARTIES.TETE:
			# (SO4) Ferme le jeu si le serpent se rentre dedans
			jeu.quitter()

	# (SO1) Dessin de la pomme
	jeu.dessiner("Pomme", jeu.pomme)

	# Déplacement du serpent
	jeu.serpent.deplacer(jeu.direction_serpent)

# Lancement du jeu à partir des fonctions d'abstraction
Jeu(initialisation, boucle)
