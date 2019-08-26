# Présentation générale

## Déclaration de l'objet Serpent

Après avoir importé la bibliothèque Zeste de Code, tu auras accès aux fonctions concernant le serpent. Une nouvelle instance de serpent devra ensuite être crée, préférentiellement à l'intérieur du jeu :

```python
def init(jeu):
	jeu.serpent = Serpent()
```

## Constantes du serpent

Dans l'objet Serpent précédemment créé, en plus des méthodes mentionnées ci-dessous, tu trouveras trois constantes (variables qui ne changent pas) importantes.

### Gestion de la direction

La première, `jeu.serpent.DIRECTIONS` permet de donner au serpent une direction ; elle est particulièrement utilisée avec la fonction `deplacer`, qui la prend en argument. Cet objet se décline en cinq clefs :

```python
# Le serpent va vers la droite
jeu.serpent.DIRECTIONS.DROITE
# Le serpent se déplace à gauche
jeu.serpent.DIRECTIONS.GAUCHE
# Le serpent monte
jeu.serpent.DIRECTIONS.HAUT
# Le serpent part en bas
jeu.serpent.DIRECTIONS.BAS
# Le serpent s'arrête (pas tout à fait une direction)
jeu.serpent.DIRECTIONS.STOP
```

### Gestion des rotations

Pour les plus avancés d'entre vous, il sera nécessaire de détecter quand le serpent tourne et dans quel sens. C'est à cet effet qu'a été créé la constante `ROTATIONS` :

```python
# Le serpent tourne dans le sens des aiguilles d'une montre
jeu.serpent.ROTATIONS.HORAIRE
# Le serpent tourne dans le sens inverse
jeu.serpent.ROTATIONS.ANTI_HORAIRE
```

### Parties du serpent

Le serpent se décompose automatiquement en diverses partie :

- une tête, pour indiquer l'avant ;
- une queue, pour indiquer l'arrière ;
- le reste est composé de morceaux de corps.

Afin de détecter ces différentes parties, une constante `jeu.serpent.PARTIES` existe, et peut prendre les valeurs suivantes :

```python
# Renseigne la tête du serpent (donc l'avant)
jeu.serpent.PARTIES.TETE
# Renseigne une partie de corps du serpent
jeu.serpent.PARTIES.CORPS
# Renseigne la queue du serpent (donc l'arrière)
jeu.serpent.PARTIES.QUEUE
```

Notons que lors de l'itération, les parties sont ordonnées dans le sens inverse (et si tu ne comprends rien à cette phrase, reviens plus tard).

Lorsque le serpent grandit, la bibliothèque ajoute automatiquement un morceau de corps juste après la tête, ce qui a pour effet de l'allonger.

# Déplacement et taille

Dans cette partie sont détaillées les fonctions concernant la taille du serpent ainsi que la gestion de ses déplacements.

## Taille du serpent et agrandissement

En premier lieu, voyons une fonction très utile, qui permet d'obtenir la taille du serpent : `serpent.taille()`. Cette fonction ne nécessite aucun paramètre (sauf celui implicite passé par l'appel via une méthode) ; elle retourne simplement la taille brute du serpent. Par exemple, au début du jeu, elle renverra 3.

Pour faire grandir le serpent, nous en avons parlé plus haut, il est possible d'appeler la fonction `serpent.grandir()`. Elle ne prend aucun paramètre et ne retourne rien, mais modifie en interne la taille du serpent en ajoutant en morceau juste après la tête.

## Fonction de déplacement

Afin de déplacer le serpent, il faut appeler la méthode `serpent.deplacer(direction)` avec direction une des constantes de direction vue ci-dessus. Par exemple, pour déplacer le serpent d'une case vers le haut :

```python
serpent.deplacer(jeu.serpent.DIRECTIONS.HAUT)
```

# Position du serpent

Un itérateur existe et permet d'obtenir tous les morceaux de serpent dans l'ordre allant de la queue à la tête, il s'agit de `serpent.morceaux(taille)` ; le seul argument est la taille du serpent, ou plus simplement le nombre de morceaux à prendre. Pour afficher les positions successives du serpent :

```python
for morceau in jeu.serpent.morceaux(taille):
	print(morceau.position)
```

Comme tu peux le voir, morceau contient une information `position`, mais aussi une information `direction_rotation`, qui contient une des constantes de rotation vue ci-dessus, et enfin `type`, qui contient une constante de partie du serpent (tête, queue ou corps).

Pour obtenir la position de la tête du serpent, une fonction peut te simplifier la vie, c'est la fonction `serpent.position_tete`, qui retourne simplement la position (x, y) de la tête du serpent.
