########################################
###         Troisième objectif       ###
###      (c) Zeste de Savoir (c)     ###
###           Licence GPL            ###
###         Auteur : TAlone          ###
########################################

# Le troisième objectif vise à animer le serpent
# (sous-objectif 1) - en ligne droite ;
# (sous-objectif 2) - dans les autres directions.

# Import de la bibliothèque du coding gouter (fonctions d'abstraction)
from bibliotheque import Jeu, Serpent

# Fonction principale d'initialisation
def initialisation(jeu):
	# Création d'un serpent à l'écran
	jeu.serpent = Serpent()

	# (SO1) Donne une direction par défaut au serpent
	jeu.direction_serpent = jeu.serpent.DIRECTIONS.STOP

	# Déclaration du cactus
	jeu.ajouter_image("Cactus", "images/cactus.png")

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
	if Jeu.EVENEMENTS.QUITTER in jeu.evenements:
		jeu.quitter()

	# (SO1) Lorsqu'une touche est appuyée
	if Jeu.EVENEMENTS.TOUCHE_APPUYEE in jeu.evenements:
		# (SO1) On stocke la touche appuyée
		touche = jeu.evenements[Jeu.EVENEMENTS.TOUCHE_APPUYEE]

		# (SO1) ...on vérifie la direction droite...
		if touche == Jeu.TOUCHES.FLECHE_DROITE:
			jeu.direction_serpent = jeu.serpent.DIRECTIONS.DROITE
		# (SO2) ...et les autres directions.
		elif touche == Jeu.TOUCHES.FLECHE_HAUT:
			jeu.direction_serpent = jeu.serpent.DIRECTIONS.HAUT
		elif touche == Jeu.TOUCHES.FLECHE_BAS:
			jeu.direction_serpent = jeu.serpent.DIRECTIONS.BAS
		elif touche == Jeu.TOUCHES.FLECHE_GAUCHE:
			jeu.direction_serpent = jeu.serpent.DIRECTIONS.GAUCHE

	# Effacement de l'écran, et remplissage avec les tiles de fond
	jeu.effacer_ecran()

	# Itération sur tous les morceaux de grille
	for carreau in jeu.grille():
		# (SO1) Si l'on est sur un côté...
		if jeu.est_un_bord(carreau):
			# (SO1) ...dessine un cactus
			jeu.dessiner("Cactus", { "position": carreau })

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

	# (SO1) Déplacement du serpent
	jeu.serpent.deplacer(jeu.direction_serpent)

# Lancement du jeu à partir des fonctions d'abstraction
Jeu(initialisation, boucle)
