# ZdS Coding Goûter – Partie Code

## Licence

TL;DR : **Have fun**, tout en respectant les auteurs du projet.

Comme mentionné dans le README commun, cette partie est placée sous licence GNU GPL v3.0 (voir LICENCE.md), pour rappel, cette licence impose :

- le crédit des auteurs : les commentaires en début de fichier ne sauraient donc être retirés lors de la réutilisation de tout ou partie du code, sauf à obtenir l'accord particulier de l'association Zeste de Savoir ;
- la redistribution de la source : toute modification du présent code doit être redistribuée à tous sous la même licence, afin que le partage du savoir ne se perde pas ;
- la documentation des changements effectués : en cas de redistribution d'un code dérivé, il doit être porté mention des changements effectués, et ce afin de ne pas berner l'utilisateur.

En contrepartie, vous obtenez les droits de faire ce que vous souhaitez de ce code, en particulier :

- d'en faire un usage personnel ;
- de le modifier pour réaliser votre propre atelier ;
- de le vendre ;
- de le partager à quiconque et sans restriction autre que celles mentionnés ci-dessus ;
- d'expérimenter vos propres projets, et de tout casser.

Dans tous les cas mentionnés, l'association Zeste de Savoir ainsi que les auteurs du code ne sauraient être tenus responsable de tous dégâts éventuels provoqués par le code, qui est distribué sans aucune garantie. De plus, ce court texte ne saurait en aucun cas se substituer au texte intégral de la licence (voir LICENCE.md).

## Présentation

Ces objectifs sont des recommandations pour l'apprentissage, et ne sont en aucun cas figés : si un participant nécessite de l'aide pour autre chose, il apprendra autant par ce biais.

La présentation ici vise à guider les organisateurs afin d'aiguiller les participants perdus au cas par cas ; ce document n'est pas destiné à être lu oralement dans son intégralité.

Note avant de commencer : ce projet ne tourne plus que sous Python 3, suite aux gestions calamiteuses d'à-peu-près tout dans Python 2 ; de plus, le support de Python 2 s'arrête cette année, profitez-en pour vous  mettre à jour.

### Code initial : affichage d'une fenêtre

Le code initialement proposé est à réaliser avec les participants, il s'agit simplement d'afficher la fenêtre de jeu vide et d'écouter l'évènement de fermeture afin d'éviter d'être bloqué.

C'est un code extrêmement simple qui doit servir de base pour présenter les rudiments de la programmation (boucles, conditions, variables).

### Objectif 1 : Remplissage de la fenêtre

Cet objectif est très varié (boucles, conditions, variables), et peu prendre beaucoup de temps aux participants, car il nécessite la prise en main de la bibliothèque ; il est nécessaire de les orienter **sans donner la solution** sauf s'ils sont réellement perdus.

Sous-objectif 1 : L'objectif consiste à proposer une solution pour remplir entièrement l'espace de jeu avec les tiles de fond fournies (`background.png`). La fonction `jeu.screenIterator()` est complexe et devra sans doute être expliquée.

Sous-objectif 2 : Ensuite, il conviendra de délimiter la zone pour montrer à l'utilisateur où sont les limites du terrain, et plus tard pour la gestion des collisions.

### Objectif 2 : Affichage du serpent

Cet objectif vise à réviser les bases de la programmation, déjà survolées dans l'objectif 1, mais de façon plus brève, comme un rappel des fondamentaux.

Sous-objectif 1 : Ici, il faudra trouver un moyen d'ajouter à l'écran le serpent, de sa déclaration à son affichage pratique comme des morceaux de corps. La fonction de bibliothèque associée (`snake.partsIterator()`) n'est pas évidente mais les participants pourront se rendre compte qu'elle ressemble à `jeu.screenIterator()`, expliquée plus tôt.

Sous-objectif 2 : Il faudra ensuite afficher une tête à l'avant et une queue à l'arrière ; c'est un objectif rapide, car il ne fait appel qu'à des conditions et un peu de logique.

### Objectif 3 : Animation du serpent

Cet objectif est fortement marqué par la nécessité de lire la documentation (*RTFM*), fondement de la programmation, les participants sont donc censés se débrouiller seuls excepté pour la boucle de gestion des événements, qui pourra leur être expliquée.

Sous-objectif 1 : Le premier objectif vraiment amusant du jeu consiste à animer le serpent en ligne droite lorsque l'utilisateur appuie sur la touche correspondante (au choix, cf. doc). Il conviendra d'expliquer la gestion des événements afin de ne pas laisser les participants se perdre.

Sous-objectif 2 : Très simple, cet objectif complète le premier en ajoutant les trois autres directions, il est une application directe de la documentation.

Sous-objectif 3 : Un objectif pour le moins complexe qui doit répondre à la problématique : les tiles ne tournent pas ; hormis la phase de recherche de la fonction de rotation (la même que pour le dessin), les conditions à mettre en place sont non-triviales et peu documentées, une aide pourra être nécessaire à ce niveau.

### Objectif 4 : Gestion de la pomme

Outre les notions précédentes, cet objectif traite de l'aléatoire et des collisions, et dispose d'une boucle while avancée. Il n'est pas particulièrement complexe mais nécessite plus de réflexion et de logique que les précédents.

Sous-objectif 1 : La pomme apparaît indépendamment du serpent, n'importe où sur la zone de jeu, grâce à la fonction intégrée d'aléatoire documentée. C'est un sous-objectif simple, pour bien aborder le problème.

Sous-objectif 2 : Par la suite, le serpent doit pouvoir manger la pomme, il faudra pour cela détecter la collision entre la tête du serpent et la pomme, par la fonction prévue à cet effet. L'utilisation de `snake.partsIterator()` ayant déjà été abordée, les participants sont invités à se référer au code déjà écrit.

Sous-objectif 3 : Cet objectif de transition vise à initier les participants à la gestion des collisions, avec la fonctions d'abstraction `jeu.isSide()` déjà utilisée et vérifiant si la pomme se situe sur un cactus afin de la déplacer le cas échéant.

### Objectif 5 : Ajout de collisions

Cet objectif voit le jeu se terminer, et est le dernier principal (avant les objectifs bonus) ; il étudie particulièrement les fonctions de collision, très importantes en programmation vidéoludique. Il se conclut par un sous-objectif bonus non-documenté ici visant à étudier les déclarations de fonctions.

Sous-objectif 1 : Lorsque le serpent heurte un cactus, il doit mourir ; en l’occurrence, la zone de jeu doit se fermer. Une solution devra être proposée par les participants, en réutilisant ce qui a été vu précédemment et la nouvelle fonction de collision.

Sous-objectif 2 : Le serpent ne doit pas se mordre la queue ; il incombe au participant de ne quitter le jeu le cas échéant, mais il faudra faire attention au cas où il se mord la tête.
