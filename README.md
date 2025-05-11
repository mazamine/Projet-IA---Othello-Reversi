# README — Application Othello IA

## 1. Introduction

Cette application vous permet de jouer à Othello/Reversi avec 3 niveaux d'IA (Facile, Moyen, Difficile) et d'organiser des tournois entre elles.

## 2. Prérequis

* Python 3.x
* Modules standards : `math`, `time`, `random` (aucune dépendance supplémentaire requise)

## 3. Installation

1. Assurez-vous que les fichiers suivants sont présents :
   * `core_game.py`
   * `ai_strategies.py`
   * `ai_tournament.py`
   * `othello_launcher.py`
2. Vérifiez que leurs extensions sont `.py` et que le mode de langage dans VS Code est défini sur Python.

## 4. Utilisation

* Pour commencer à jouer ou organiser un tournoi, ouvrez le terminal et tapez :

  ```bash
  python othello_launcher.py
  ```
* Vous verrez un menu avec les options suivantes :

  1. Humain vs Humain
  2. Contre l'IA Facile
  3. Contre l'IA Moyenne
  4. Contre l'IA Difficile
  5. Tournoi d'IA
  6. Quitter

## 5. Désactiver l'affichage de la profondeur

Si vous souhaitez **désactiver** l'affichage de la profondeur maximale atteinte par les IA :

* Ouvrez `ai_strategies.py`.
* Recherchez les deux lignes où la profondeur est affichée :

  ```python
  print(f"[Medium AI] Maximum depth reached: {self.depth_reached}")  # vers la ligne 239
  print(f"[Hard AI] Maximum depth reached: {self.depth_reached}")    # vers la ligne 333
  ```
* Ajoutez un `#` devant chaque `print(...)` pour les désactiver.

## 6. Configuration de l'IA

Dans `ai_strategies.py` :

* `self.max_depth` : Vous pouvez modifier cette valeur comme vous le souhaitez pour les deux classes (Moyenne, Difficile).

  * Remarque : Augmenter cette valeur rend l'IA plus forte mais plus lente à répondre.
* `self.time_limit` : Vous pouvez augmenter ou diminuer la limite de temps pour éviter les dépassements de délai.

## 7. Structure des fichiers

```
/morris_game.py         # Logique du jeu, mouvements, score, affichage du plateau
/ai_strategies.py     # Classes EasyAI, MediumAI, HardAI
/tournament.py     # Classe Tournament pour les tournois en round-robin
/othello_launcher.py  # Menu principal + exécution
```
