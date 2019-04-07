########################################
###          Objectifs bonus         ###
###      (c) Zeste de Savoir (c)     ###
###           Licence GPL            ###
###         Auteur : TAlone          ###
########################################

# Quelques bonus pour les participants en avance :
# (bonus 1 - aisé) - empêche le serpent d'aller en arrière ;
# (bonus 2 - aisé) - ajout d'un compteur de points ;
# (bonus 3 - moyen) - ajout d'un écran pour rejouer ;
# (bonus 4 - difficile) - ajout de coins au serpent.

# Import de la bibliothèque du coding gouter (fonctions d'abstraction)
from bibliotheque import *

# Fonction principale d'initialisation
def initialisation(jeu):
	# Création d'un serpent à l'écran
	jeu.serpent = Serpent()

	# Création d'une pomme
	jeu.pomme = jeu.position_aleatoire_pomme()

	# (B3) Création d'une variable de perte
	jeu.serpent.vivant = True
	# (B3) Ajout du texte pour relancer la partie
	jeu.ajouter_texte("Nouvelle Partie", "Pour rejouer, appuyez sur ESPACE")

	# Donne une direction par défaut au serpent
	jeu.direction_serpent = jeu.serpent.DIRECTIONS.STOP

	# Déclaration du cactus
	jeu.ajouter_image("Cactus", "images/cactus.png")
	# Déclaration de la pomme
	jeu.ajouter_image("Pomme", "images/pomme.png")

	# Ajout du corps
	jeu.ajouter_image("Corps", "images/corps.png")
	# Ajout de la queue
	jeu.ajouter_image("Queue", "images/queue.png")
	# Ajout de la tête
	jeu.ajouter_image("Tête", "images/tete.png")
	# (B4) Ajout de l'image de rotation
	jeu.ajouter_image("Coin", "images/coin.png")

	# Ajout de l'asset spécial qui sera automatiquement mis en fond
	jeu.ajouter_image("fond", "images/fond.png")

# Fonction executée regulièrement
def boucle(jeu):
	# Fermeture du jeu lors de l'appui de la croix
	if Evenements.QUITTER in jeu.evenements:
		jeu.quitter()

	# Lorsqu'une touche est appuyée
	if Evenements.TOUCHE_APPUYEE in jeu.evenements:
		# On stocke la touche appuyée
		touche = jeu.evenements[Evenements.TOUCHE_APPUYEE]

		# ...on vérifie la direction droite...
		# (B1) On vérifie aussi que le serpent n'aille pas déjà à gauche
		if touche == Touches.FLECHE_DROITE and jeu.direction_serpent != jeu.serpent.DIRECTIONS.GAUCHE:
			jeu.direction_serpent = jeu.serpent.DIRECTIONS.DROITE
		# ...et les autres directions.
		# (B1) De même pour les autres directions
		elif touche == Touches.FLECHE_HAUT and jeu.direction_serpent != jeu.serpent.DIRECTIONS.BAS:
			jeu.direction_serpent = jeu.serpent.DIRECTIONS.HAUT
		elif touche == Touches.FLECHE_BAS and jeu.direction_serpent != jeu.serpent.DIRECTIONS.HAUT:
			jeu.direction_serpent = jeu.serpent.DIRECTIONS.BAS
		elif touche == Touches.FLECHE_GAUCHE and jeu.direction_serpent != jeu.serpent.DIRECTIONS.DROITE:
			jeu.direction_serpent = jeu.serpent.DIRECTIONS.GAUCHE
		# (B3) Si l'on appuie sur espace quand le serpent est mort
		elif touche == Touches.ESPACE and not jeu.serpent.vivant:
			# (B3) Création d'un nouveau serpent (écrase le précédent)
			jeu.serpent = Serpent()
			# (B3) Le serpent est vivant et à l'arrêt
			jeu.serpent.vivant = True
			jeu.direction_serpent = jeu.serpent.DIRECTIONS.STOP

	# Si il y a collision entre la pomme et la tête du serpent
	if jeu.collision(jeu.serpent.position_tete, jeu.pomme.position):
		# Le serpent grandit
		jeu.serpent.grandir()
		# La pomme change de position
		jeu.pomme = jeu.position_aleatoire_pomme()

	# Effacement de l'écran, et remplissage avec les tiles de fond
	jeu.effacer_ecran()

	# Déclaration d'une variable contenant la taille du serpent
	taille = jeu.serpent.taille

	# (B2) Ajoute le texte de score et le dessine
	jeu.ajouter_texte("Score", "Score : " + str(taille - 3))

	# (B3) Change la position du score si l'écran "Rejouer" est affiché
	if jeu.serpent.vivant:
		jeu.dessiner("Score", { "position": (36, 36) })
	else:
		jeu.dessiner("Score", { "position": (260, 150) })
		# (B3) Ajoute le message pour rejouer
		jeu.dessiner("Nouvelle Partie", { "position": (50, 200) })

	# Itération sur tous les morceaux de grille
	for carreau in jeu.grille():
		# Si l'on est sur un côté...
		if jeu.est_un_bord(carreau):
			# ...dessine un cactus
			jeu.dessiner("Cactus", { "position": carreau })

			# Si le coin est en contact avec la tête du serpent
			if jeu.collision(carreau, jeu.serpent.position_tete):
				# Ferme le jeu si il y a contact entre la tête et un bord
				#jeu.quitter()
				# (B3) Le serpent meurt s'il rentre dans un mur
				jeu.serpent.vivant = False

	# (B3) Dessin du serpent uniquement s'il est en vie
	if jeu.serpent.vivant:
		# Dessin d'un certain nombre de morceaux à l'écran
		for morceau in jeu.serpent.morceaux(taille):
			# Choix du sprite en fonction de la partie à dessiner et dessin à l'écran
			if morceau.type == jeu.serpent.PARTIES.TETE:
				jeu.dessiner("Tête", morceau)
			elif morceau.type == jeu.serpent.PARTIES.QUEUE:
				jeu.dessiner("Queue", morceau)
			else:
				# (B4) Vérification de la rotation dans le sens des aiguilles
				if morceau.direction_rotation == jeu.serpent.ROTATIONS.HORAIRE:
					# (B4) On doit alors orienter de -90° la tuile
					morceau.rotation -= 90

					# (B4) Ne pas oublier de dessiner
					jeu.dessiner("Coin", morceau)
				elif morceau.direction_rotation == jeu.serpent.ROTATIONS.ANTI_HORAIRE:
					# (B4) Pour une rotation en sens inverse des aiguilles, il faut tourner de 180°
					morceau.rotation += 180

					# (B4) Ne pas oublier de dessiner
					jeu.dessiner("Coin", morceau)
				# Dans les autres cas, on considère qu'il n'y a pas de rotation
				else:
					# Dessin du corps
					jeu.dessiner("Corps", morceau)

			# Vérification que le serpent ne se mord pas
			# Attention : la tête est incluse, il faut donc la retirer
			if jeu.collision(jeu.serpent.position_tete, morceau.position) and morceau.type != jeu.serpent.PARTIES.TETE:
				# Ferme le jeu si le serpent se rentre dedans
				#jeu.quitter()
				# (B3) Le serpent meurt s'il se rentre dedans
				jeu.serpent.vivant = False

	# (B3) La pomme n'apparait que si le serpent est en vie
	if jeu.serpent.vivant:
		# Dessin de la pomme
		jeu.dessiner("Pomme", jeu.pomme)

	# Déplacement du serpent
	jeu.serpent.deplacer(jeu.direction_serpent)

# Lancement du jeu à partir des fonctions d'abstraction
Jeu(initialisation, boucle)
