Cette partie est un rappel des notions abordées ci-avant, dans le cas où tu aurais besoin de revoir les bases du langage, pendant l'atelier ou chez toi.

# Quelques calculs simples

Pour rappel, le langage Python interprétera et exécutera tout calcul présent dans son code. Quelques exemples sont proposés ci-dessous :


```python
>>> 1 + 1
2
>>> 6 * 7
42
>>> 4-2
2
>>> 2-4
-2
>>> (4-2)*2
4
>>> 3.6/2
1.8
>>> 3*5.2
15.6
```

# Les variables et fonctions

**Variable** : boite dans laquelle on peut mettre une valeur.

**Fonction** : morceau de code que quelqu'un d'autre a déjà écrit pour vous, qu'on appelle avec son nom pour ne pas le ré-écrire. On peut également écrire nos propres fonctions (comme mentionné un peu plus bas).

Quelques rappels issus de l'initiation au code :

```python
# Appel de la fonction d'affichage, avec pour paramètre "Bonjour !"
print("Bonjour !")
>>> Bonjour !

x=3
print(x)
>>> 3
```

On notera ici que `x` est passée directement à la fonction. En effet, une variable est une boîte qu'on peut donner tel quel et Python comprend très bien qu'on veut donner à la fonction le *contenu* de la boîte. Pour le cas du texte "Bonjour !", il est passé entre guillemets, ce qui indique que la chaîne de caractères "Bonjour !" est donnée directement en argument.

Pour rappel, seule une nouvelle déclaration changera la valeur d'une variable :

```python
x=3
x+1
>>> 4
print(x)
>>> 3
x=x+1
>>> 4
print(x)
>>> 4
```

Enfin, on rappelle les deux types de variables :

- **locale** : disponible uniquement dans la fonction en cours ;
- **interne** : disponible partout où l'objet concerné est présent (pratique pour passer une variable de `initialisation` à `boucle`, par exemple).

Les deux types de fonctions sont de même nature :

- **principale** : disponible pour le fichier en cours ;
- **interne** : peut être utilisée par le jeu lui-même (c'est le cas de `boucle`, par exemple) ou utilisée depuis la variable jeu (`jeu.quitter()` par exemple).

Comme mentionné en introduction, on peut créer (on dit « déclarer ») des fonctions nous-même. Ça ressemble toujours à ceci :

```python
def nom_de_la_fonction(premier_argument, second_argument, ...):
	print("Contenu de la fonction")
```

Par exemple, notre fonction `boucle` ressemble à ceci :

```python
def boucle(jeu):
	# Mettre ici le code de la fonction
```

Elle attend donc un argument appelé jeu, qui lui sera passé par la bibliothèque avant d'exécuter le contenu de la fonction ; cet objet contiendra tout ce qui est nécessaire pour l'affichage de notre jeu.

# Structures conditionnelles

**Condition** : Expression qui exécute un morceau de code seulement si elle est vérifiée.

Aucun rappel particulier n'est nécessaire pour les conditions, mais nous te proposons le code final de l'initiation afin d'avoir les idées claires. En cas de question, n'hésite pas à appeler un animateur.

```python
age = 15
# Si l'âge est supérieur ou égal à 21…
if age >= 21:
	print("Majorité internationale")
# Sinon, si l'âge est supérieur à 18…
elif age >= 18:
	print("Tu es majeur")
# Sinon…
else:
	print("Tu es mineur")
```

Aussi, les tests dont nous pourrions avoir besoin par la suite sont les suivants :

- `>` supérieur à ;
- `<` inférieur à ;
- `==` strictement égal à ;
- `!=` différent de.

# Les boucles

**Boucle** : Morceau de code répété un certain nombre de fois, jusqu'à ce qu'une condition soit vraie.

Ici encore, tout devrait aller, et pour référence, voici le code écrit en introduction. Dans la documentation ci-après, les méthodes destinées à être utilisées dans une boucle sont toujours explicitement mentionnées comme tel.

```python
for carreau in jeu.grille():
	if jeu.est_un_bord(carreau):
		print(carreau)
```
