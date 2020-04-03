# Présentation générale

## Déclaration de l'objet Jeu

Après avoir importé la bibliothèque Zeste de Code, tu auras accès aux fonctions principales du jeu ; pour rappel, un objet Jeu est créé comme suit :

```py
mon_jeu = Jeu(initialisation, boucle)
```

Où `initialisation` et `boucle` sont deux fonctions qui doivent avoir été définies précédemment (voir la partie d'initiation au code) ; ces fonctions prendront en paramètre l'instance du jeu afin de pouvoir la modifier.

## Gestion des événements

### Variables passées à la boucle

Lorsque le jeu est récupéré à l'intérieur de la boucle, il dispose de variables accessibles de façon directe (hors fonctions / méthodes) :

- `mon_jeu.largeur`, qui contient la largeur de la fenêtre ;
- `mon_jeu.hauteur`, qui contient la hauteur de la fenêtre ;
- `mon_jeu.evenements`, qui contient la liste des événements déclenchés depuis le dernier tour de boucle.

La variable `evenments` nous intéressera particulièrement, et nous pourrons vérifier si un certain événement est déclenché en utilisant une condition :

```py
if Evenements.QUITTER in mon_jeu.evenements:
	print("Je veux quitter")
```

### Variables de la bibliothèque

Dans la suite de ce guide, nous te présenterons les fonctions ayant attrait à la zone de jeu et au serpent. Toutefois, certains objets transcendent et ne peuvent aller dans aucune des deux catégories ; ces objets sont importés par défaut et ne requièrent donc pas l'appel par une méthode.

Le premier objet concerne la gestion des événements, et est naturellement nommé `Evenements` ; nous l'avons vu ci-dessus sans bien comprendre à quoi il correspondait ; cet objet contient deux variantes qui nous intéressent :

```py
# Déclenché lorsque le joueur demande à fermer le jeu
Evenements.QUITTER
# Déclenché lorsqu'une touche est appuyée
Evenements.TOUCHE_APPUYEE
```

### Récupération de la touche appuyée

Une fois l'événement de `TOUCHE_APPUYEE` intercepté, il serait bon de savoir sur quelle touche le joueur a appuyé afin de déplacer le serpent dans la bonne direction ; pour cela, il suffit de tester `mon_jeu.evenements[Evenement.TOUCHE_APPUYEE]`, magique non ? La valeur peut alors être égale à (notons la seconde variable interne de la bibliothèque : `Touches`) :

```py
Touches.FLECHE_DROITE
Touches.FLECHE_GAUCHE
Touches.FLECHE_HAUT
Touches.FLECHE_BAS
Touches.ESPACE
```

Pas plus de détails ici afin de vous faire chercher par vous-même ; n'oublie pas en tout cas qu'en informatique, il faut tester, tu ne peux rien casser. En cas de problème persistant, un animateur sera heureux de te guider.

# Ajout d'images et de texte

## Déclaration des variables internes

Une fois l'objet de jeu créé, et récupéré dans une des fonctions `initialisation` ou `boucle`, il est possible de déclarer à tout moment une image par la méthode `ajouter_image`, appelée avec le nom à donner à l'image ainsi que le chemin relatif de l'image. Par la suite, on pourra afficher notre image où on veut dans la fenêtre en l'appelant par son nom (voir un peu plus loin comment faire).

[[information]]
| Le chemin relatif d'un fichier est l'endroit où il se trouve par rapport au fichier actuel. Par exemple, l'image `image.png` située dans le dossier `images` du dossier du fichier actuel est de chemin relatif `images/image.png`.

Puisqu'un exemple vaut mieux qu'un long discours :

```py
# Déclaration de l'image du cactus
mon_jeu.ajouter_image("Cactus", "images/cactus.png")
```

La méthode permettant d'ajouter du texte fonctionne de la même façon, mais prend comme second paramètre le texte à afficher ; elle est nommée `ajouter_texte`.

## Récupération et dessin

Afin de dessiner une image ou un texte précédemment déclaré, il faut faire appel à la fonction `dessin` ; cette fonction prend en paramètre :

1. le nom déclaré de l'image ou du texte ;
2. un objet de paramètres, pouvant prendre deux clefs : `position` et `rotation`, **toute valeur différente sera ignorée**.

Par exemple, pour dessiner un cactus (déclaré précédemment), en haut à gauche de l'écran, il suffit d’appeler la fonction :

```py
mon_jeu.dessiner("Cactus", { "position": (0, 0) })
```

Une autre fonction de dessin utile est la fonction `effacer_ecran`, qui permet d'effacer entièrement le contenu de la zone de jeu ; elle ne prend aucun paramètre en entrée :

```py
mon_jeu.effacer_ecran()
```

# Gestion des positions et collisions

## Itérateur principal

Dès le second objectif, vous aurez besoin de réaliser une boucle sur l'ensemble de la grille du jeu ; pour cela, un itérateur `grille` existe, et donne la position (x, y) d'un morceau de grille à chaque itération ; pour bien comprendre, voici un petit exemple d'utilisation :

```py
for carreau in mon_jeu.grille():
	print(carreau)
```

Ce code affichera la liste de tous les carreaux possibles dans la console.

## Fonctions utiles

Afin de vérifier une collision entre deux objets, il existe une fonction `collision` qui renvoie `True` lorsqu'il y a collision et `False` sinon. Cette fonction prend deux paramètres, la position du premier objet, et la position du second ; cette fonction est principalement destinée à être utilisée dans des conditions, par exemple :

```py
if mon_jeu.collision(pomme, morceau.position):
	print("Collision Serpent-Pomme")
```

Vérifiera s'il y a collision entre la pomme et la variable nommée `morceau.position`.

Afin d'afficher les cactus sur un bord, tu pourrais avoir besoin de savoir si une position correspond ou non à un bord, pour cela, une fonction `est_un_bord` existe, et prend comme unique paramètre la position à tester ; elle retourne un booléen. Pas d'exemple ici, on vous laisse essayer d'utiliser cette fonction par vous-même afin de bien comprendre son principe.

## Divers

Enfin, si tu es très avancé, tu pourras essayer d'afficher une pomme à l'écran et faire en sorte que le serpent puisse la manger. Pour générer la position de la pomme, deux solutions sont possibles :

- la solution simple, utiliser `position_aleatoire_pomme`, fonction intégrée retournant simplement une position (x, y) aléatoire bien choisie ;
- la solution plus complexe, qui consiste à créer cette fonction par toi-même ; nous donnerons évidemment des indices aux participants arrivant jusqu'ici.

L'idée est de commencer par utiliser la fonction intégrée puis éventuellement de la (re)coder soi-même par la suite.

# Fonctions diverses et bonus

Cette partie regroupe les fonctions qui ne trouvent leur place nulle part ailleurs ; l'une d'entre elle est très utile, les autres sont des bonus destinés aux participants les plus avancés.

## Quitter le jeu

La fonction très utile mentionnée ci-dessus est la fonction `quitter`, qui fermera simplement le jeu ; il sera nécessaire de l'utiliser lors de l'appui sur la croix de fermeture par le joueur, ou à la mort du serpent... éventuellement ;) .

## Fonctions bonus

Quelques détails du jeu vous ont été cachés dans les parties précédentes, mais les objectifs bonus nous obligent à révéler certains de nos secrets les mieux gardés.

Tout d'abord, la fonction d'initialisation prend en réalité non pas deux mais bien quatre paramètres ; il est en effet possible de changer la taille de la fenêtre de jeu en passant en paramètres la largeur puis la hauteur, par exemple :

```py
mon_jeu = Jeu(initialisation, boucle, 1024, 576)
```

créera une fenêtre plus grande que celle par défaut.

[[attention]]
| Il faudra veiller à ce que les deux paramètres de largeur et de hauteur soient des multiples de 32, sinon... à toi de tester.

La deuxième fonction utile pour les bonus permet d'afficher du texte en plus grand que celui par défaut ; il s'agit de la fonction `init_text`. Cette méthode est pour être exact déjà appelée lors de l'initialisation du jeu (mais masquée, bien entendu). Elle permet de régler la police et la taille du texte ; un exemple pour comprendre :

```py
init_text("sans-serif", 32)
```

Cet appel rendra le texte en police sans-serif, et en taille 32, ce sont d’ailleurs les paramètres par défaut.
