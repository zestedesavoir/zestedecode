# ZdS Coding Goûter – Partie Code

Ce dossier traite de la partie **Snake** (Python) des ateliers de programmation Zeste de Code.

## Licence

TL;DR : **Have fun**, tout en respectant les auteurs du projet.

Comme mentionné dans le README commun, cette partie est placée sous licence GNU GPL v3.0 (voir LICENCE.md), pour rappel, cette licence impose :

- le crédit des auteurs : les commentaires en début de fichier ne sauraient donc être retirés lors de la réutilisation de tout ou partie du code, sauf à obtenir l’accord particulier de l’association Zeste de Savoir ;
- la redistribution de la source : toute modification du présent code doit être redistribuée à tous sous la même licence, afin que le partage du savoir ne se perde pas ;
- la documentation des changements effectués : en cas de redistribution d’un code dérivé, il doit être porté mention des changements effectués, et ce afin de ne pas berner l’utilisateur.

En contrepartie, vous obtenez les droits de faire ce que vous souhaitez de ce code, en particulier :

- d’en faire un usage personnel ;
- de le modifier pour réaliser votre propre atelier ;
- de le vendre ;
- de le partager à quiconque et sans restriction autre que celles mentionnés ci-dessus ;
- d’expérimenter vos propres projets, et de tout casser.

Dans tous les cas mentionnés, l’association Zeste de Savoir ainsi que les auteurs du code ne sauraient être tenus responsable de tous dégâts éventuels provoqués par le code, qui est distribué sans aucune garantie. De plus, ce court texte ne saurait en aucun cas se substituer au texte intégral de la licence (voir LICENCE.md).

## Présentation

Ces objectifs sont des recommandations pour l’apprentissage, et ne sont en aucun cas figés : si un participant nécessite de l’aide pour autre chose, il apprendra autant par ce biais.

La présentation ici vise à guider les organisateurs afin d’aiguiller les participants perdus au cas par cas ; ce document n’est pas destiné à être lu oralement dans son intégralité.

Note avant de commencer : ce projet ne tourne plus que sous Python 3, suite aux gestions calamiteuses d’à-peu-près tout dans Python 2 ; de plus, le support de Python 2 s’arrête cette année, profitez-en pour vous mettre à jour.

### Première partie : découverte des outils

Durée recommandée : **moins d’une heure**

Avant de commencer à coder le Snake, il est nécessaire de prendre du temps pour découvrir les outils de travail ainsi que le fonctionnement de l’interpréteur Python. À ce titre, il faudra présenter aux participants le fonctionnement des outils utilisés, en particulier la gestion des erreurs, très importante pour avancer en programmation. La présentation de l’association pourra tenir au début de l’heure, et la présentation des métiers de l’informatique à la fin ; ainsi, trois heures pleines peuvent être réservées au code.

#### Présentation de l’association et de l’atelier

Se réferer aux diapositives de présentation proposées sur ce repo ; ne pas oublier d’expliquer les enjeux de la programmation et le principe de l’atelier. Les participants devront, à l’issu de ces présentations, être répartis en groupe selon qu’ils traitent le Snake (Python) ou le Flappy Bird (Scratch).

#### Calculs simples avec l’interpréteur

La première démonstration consiste à montrer quelques calculs simples pouvant être effectués avec l’interpréteur ; se référer aux diapositives pour quelques exemples d’opérations simples. Après la démonstration, proposer quelques exercices simples.

#### Déclaration de variables

Il conviendra ensuite de montrer aux participants comment déclarer des variables ainsi que quelques types courants – en particulier, les nombres, booléens et types personnalisés qui seront nécessaires par la suite.

Suite à cette initiation, les participants seront invités à créer un premier fichier pour leur jeu dans le bon répertoire, et à importer la bilbiothèque. Dans ce fichier, ils pourront tenter de créer quelques variables, puis il sera temps de passer à la conception du jeu (note : présenter les métiers de l’informatique ici peut être une bonne idée, car les participants n’auront pas encore trop la tête dans le code à ce moment).

### Seconde partie : création d’un Snake

#### Premier objectif

Le premier objectif consiste en la découverte du fonctionnement de la bibliothèque ; cet objectif reste très guidé par rapport au suivant : il se veut comme une intermédiaire entre le cours et la partie en autonomie. Il est important pour bien réussir que les participants comprennent ce que sont les fonctions `init` et `boucle` ainsi que leur fonctionnement au sein du jeu. L'idée d'une boucle peut être nouvelle, il conviendra donc de la tester en vérifiant que le participant est capable de faire afficher la taille du serpent à chaque tour.

Le premier sous-objectif consiste en la création des variables internes et l'affichage de la taille du serpent, il ne contient pas de notions nouvelles à l'exception des variables internes qui seront très rapidement comprises.

Dans le second sous-objectif, les participants sont invités à créer une zone de jeu réelle avec affichage du désert en fond. Il s'agit ici de la première étape véritable pour la partie ludique, ayant pour objectif de faire découvrir les structures de contrôle utilisés dans la suite du jeu, en particulier le `if`, à travers la gestion de la fermeture de la fenêtre de jeu lors de l'appui sur la petite croix du système. Les `else` pourront être abordés pour les participants ayant bien compris le fonctionnement du `if`.