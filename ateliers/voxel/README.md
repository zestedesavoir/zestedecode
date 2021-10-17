# Atelier Zeste de Code – Voxel

Ce dossier contient les sources de l'atelier Voxel de Zeste de Code. Cet atelier a lieu entièrement en ligne ; il est donc constitué d'une application web et de son serveur, afin que les participants n'aient rien à installer. Leur code est exécuté directement dans leur navigateur.

L'objectif est de développer les contrôles d'un personnage d'un jeu en voxel similaire à Minecraft.

Attention : cet atelier est encore en développement, et est très, très incomplet !

## Installation

Vous devez avoir Node 12 ou supérieur. Si ce n'est pas le cas, installez-le avec `nvm install 12`.

Ensuite, depuis ce dossier, assurez-vous d'être dans la bonne version de NodeJS (dans le doute, `nvm use` vous passera dans la bonne version), puis exécutez :

```bash
make install
```

## Lancement

L'application utilise Vue-CLI pour l'environnement de développement. Pour la lancer, exécutez :

```bash
make run
```

Le chemin vers le serveur sera affiché dans la console.
