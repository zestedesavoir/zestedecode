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

Se réferer aux diapositives de présentation proposées sur ce dépôt ; ne pas oublier d’expliquer les enjeux de la programmation et le principe de l’atelier. Les participants devront, à l’issu de ces présentations, être répartis en groupe selon qu’ils traitent le Snake (Python) ou le Flappy Bird (Scratch).

#### Calculs simples avec l’interpréteur

La première démonstration consiste à montrer quelques calculs simples pouvant être effectués avec l’interpréteur ; se référer aux diapositives pour quelques exemples d’opérations simples. Après la démonstration, proposer quelques exercices simples.

#### Déclaration de variables

Il conviendra ensuite de montrer aux participants comment déclarer des variables ainsi que quelques types courants – en particulier, les nombres, booléens et types personnalisés qui seront nécessaires par la suite.

Suite à cette initiation, les participants seront invités à créer un premier fichier pour leur jeu dans le bon répertoire, et à importer la bibliothèque. Dans ce fichier, ils pourront tenter de créer quelques variables, puis il sera temps de passer à la conception du jeu (note : présenter les métiers de l’informatique ici peut être une bonne idée, car les participants n’auront pas encore trop la tête dans le code à ce moment).

### Seconde partie : création d’un Snake

#### Premier objectif

Le premier objectif consiste en la découverte du fonctionnement de la bibliothèque ; cet objectif reste très guidé par rapport au suivant : il se veut comme un intermédiaire entre le cours et la partie en autonomie. Il est important pour bien réussir que les participants comprennent ce que sont les fonctions `init` et `boucle` ainsi que leur fonctionnement au sein du jeu. L’idée d’une boucle peut être nouvelle, il conviendra donc de la tester en vérifiant que le participant est capable de faire afficher la taille du serpent à chaque tour.

Le premier sous-objectif consiste en la création des variables internes et l’affichage de la taille du serpent, il ne contient pas de notions nouvelles à l’exception des variables internes qui seront très rapidement comprises.

Dans le second sous-objectif, les participants sont invités à créer une zone de jeu réelle avec affichage du désert en fond. Il s’agit ici de la première étape véritable pour la partie ludique, ayant pour objectif de faire découvrir les structures de contrôle utilisées dans la suite du jeu, en particulier le `if`, à travers la gestion de la fermeture de la fenêtre de jeu lors de l’appui sur la petite croix du système. Les `else` pourront être abordés pour les participants ayant bien compris le fonctionnement du `if`.

#### Second objectif

Cet objectif présente le fonctionnement des boucles, et initie les participants à la gestion de tableaux. Il est très peu guidé, et présente comme objectif de faire lire la documentation aux participants. La réalisation des trois sous-objectifs peut être longue et demander beaucoup de patience aux organisateurs, afin de poser les bases. Les rudiments de la programmation vu précédemment (structures conditionnelles et variables) seront aussi réutilisés afin de les consolider.

Le premier sous-objectif consiste à afficher les bordures de la zone en forme de cactus ; en cela, il est très simple et vise surtout à comprendre l’intérêt des boucles. Il est conseillé de montrer aux participants comment remplir la zone de jeu de cactus avant se limiter à en afficher seulement sur les bords. La phase de recherche de fonctions est très importante à ce stade car deux fonctions utiles : `grille` et `est_un_bord` seront nécessaires pour finaliser cet objectif.

Le second sous-objectif voit simplement un autre type de boucle qui itère sur un nombre donné de parties du serpent : `serpent.morceaux`. Une compréhension au moins grossière du fonctionnement des tableaux est nécessaire afin de passer les arguments, mais cet objectif devrait être simple et court.

Le dernier sous-objectif révise les structures conditionnelles en affichant les différentes parties du serpent : queue, tête et corps. Une partie encore une fois simple visant à compléter le second sous-objectif. Les participants veilleront à ne pas oublier de déclarer les sprites avec la fonction `ajouter_image` avant de les utiliser ; en cas d’oubli, ils seront invités à tenter de comprendre les erreurs Python.

#### Troisième objectif

Le troisième objectif complexifie beaucoup le code contrairement aux précédents ; il ajoute en effet une grosse partie de gestion des événements afin de vérifier l’appui des différentes touches de mouvement (les flèches directionnelles). La recherche dans la documentation sera très importante, mais aucune notion nouvelle n’est abordée à partir d’ici. Les participants qui s’arrêteront à cet objectif auront les bases nécessaires en programmation, et ce afin de créer des petits programmes simples.

Ici, le premier sous-objectif consiste à poser les bases de la direction du serpent, en particulier la déclaration d’une variable de direction ainsi que le déplacement effectif du serpent à chaque tour de boucle. Parmi les problèmes rencontrés, il est certain que figureront l’oubli de la portée globale de la variable de direction ainsi que l’oubli de l’appel à la fonction `serpent.deplacer`, qui causera le serpent à… ne pas bouger du tout, malgré un code fonctionnel.

Le second sous-objectif est une extension simple du premier qui consiste à gérer les quatre directions en se renseignant dans la documentation ainsi qu’à stocker la direction souhaitée dans la variable du jeu pour pouvoir l’utiliser par la suite.

L’objectif suivant étant prévu pour les plus avancés, il est moins documenté pour les organisateurs, sous forme plus synthétique. Après la fin des objectifs, des pistes seront proposées aux participants qui seront libres de les implémenter ou non.

#### Quatrième objectif

Cet objectif complet revient sur tout ce qui a été vu avant, et permet au participant d’acquérir une vue globale sur son code. En plus de celà, l’objectif finalise en quelque sorte le jeu en y ajoutant toutes les collisions nécessaires, ainsi que la pomme (enfin !). Comme indiqué ci-avant, voici une description synthétique de ce qui est proposé :

Le premier sous-objectif consiste simplement en l’ajout de la pomme et son dessin en fin de boucle. En outre, les participants auront besoin de la fonction `position_aleatoire_pomme`, qu’ils seront fortement invités à trouver dans la documentation.

Le second sous-objectif a pour objet la mise en place des collisions entre le serpent et la pomme. La fonction `collision` sera découverte. Pour les plus curieux, les objets pourront être abordés par la nécessité d’utiliser `pomme.position`.

Les troisième et quatrième sous-objectifs sont aussi des objectifs de collisions, simple si les participants ont compris le premier module de collisions.

#### Bonus

Une fois le quatrième objectif terminé, les participants pourront, selon leur choix, soit développer une fonctionnalité qu’ils souhaiteraient voir dans le jeu, soit tenter de concevoir un des bonus proposés. L’objectif des bonus n’est pas de les terminer tous, mais plutôt de revenir sur son code afin d’en acquérir une vision plus globale, ainsi que de revoir les acquis du jour. Il peut être bon pour les participants de réaliser ces bonus quelques jours après l’atelier, afin d’assimiler correctement et même d’approfondir les notions étudiées.

Le premier bonus, plutôt simple, résoud un problème présent dans les objectifs précédents : le serpent peut se mordre en allant en arrière. Or, dans la plupart des jeux Snake, il n’est pas possible d’aller vers l’arrière ; les participants seront donc invités à résoudre ce problème pour se faire la main.

Le second objectif bonus ajoute un compteur de points (qui est simplement la taille du serpent moins la taille initiale). L’idée est ici de se familiariser avec les fonctions de texte, particulièrement la fonction `ajouter_texte`, qui fonctionne de la même façon que `ajouter_image`.

Le troisième bonus, un peu plus complexe, vise à utiliser ces fonctions de texte afin d’afficher au joueur son score en fin de partie et lui permettre de rejouer.

Enfin, les participants les plus doués pourront proposer une solution pour gérer les rotations du serpent proprement en utilisant l’image `coin.png` mise à leur disposition. Cet objectif est complexe car il demande une bonne compréhension du fonctionnement des objets, ainsi qu’une idée (au moins vague), de la façon dont est géré le dessin du serpent en interne.