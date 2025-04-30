🎯 Number Guessing Game

Un jeu de devinette de nombres, jouable en deux modes :

Client vs Client : Deux joueurs humains (via réseau local).

Client vs IA : Un humain défie une intelligence artificielle.

🛠 Fonctionnement général

Client vs Client :Un joueur fixe secrètement un nombre (give.py), pendant qu'un autre tente de le deviner (guess.py), tous deux connectés au serveur (server.py).

Client vs IA :L'IA devine le nombre choisi par le joueur grâce à un algorithme de recherche binaire.

📂 Structure des fichiers

Fichier

Rôle

Main Interface.py

Interface principale pour choisir le mode de jeu.

server.py

Serveur local pour le mode Client vs Client.

give.py

Interface pour le joueur qui donne le nombre à deviner.

guess.py

Interface pour le joueur qui doit deviner le nombre.

Client Vs Ai.py

Partie où l'IA devine le nombre sans demander à l'utilisateur.

Ai Guesser.py

Mécanisme de l'IA et interface pour le jeu Client vs IA.

🚀 Installation

Prérequis :

Python 3.8 ou plus récent.

Modules standards (tkinter, socket, select, threading).

Cloner le projet :

git clone <lien-du-repo>
cd number-guessing-game

Lancer le serveur : (obligatoire pour "Client vs Client")

python server.py

Démarrer l'interface principale :

python "Main Interface.py"

🎯 Modes de jeu

1. Client vs Client

Le serveur doit être lancé d'abord.

Choisir "Client vs Client" dans l'interface principale.

Deux fenêtres apparaissent :

Judge (give.py) entre le nombre secret.

Guesser (guess.py) devine ce nombre.

2. Client vs IA

Choisir "Client vs AI" dans l'interface principale.

L'IA tentera de deviner le nombre que l'utilisateur entre (sans que l'IA ne puisse voir).

🧐 Comment fonctionne l'IA ?

L'IA utilise l'algorithme de recherche binaire :

Elle propose un nombre médian.

L'utilisateur indique si la proposition est trop basse, trop haute, ou correcte.

L'IA ajuste alors ses bornes pour trouver plus rapidement la bonne réponse.

💬 Remarques

Le jeu utilise TCP/IP local (127.0.0.1:12345) pour la communication entre clients et serveur.

Aucune base de données ou connexion internet n'est nécessaire.

L'IA ne triche pas (le nombre est entré manuellement).

📝 À améliorer éventuellement

Support multi-joueurs via réseau distant (avec IP externe).

Ajouter une interface plus moderne avec tkinter.ttk ou PyQt.

Implémenter un mode "IA vs IA" pour tester les stratégies.

📄 Licence

Projet personnel - libre d'utilisation et de modification. 🚀

