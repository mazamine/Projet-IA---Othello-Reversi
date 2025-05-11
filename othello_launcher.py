# main.py — Menu principal pour jouer ou lancer un tournoi Othello

import sys
from othello_game import human_vs_human, human_vs_ai
from ai_strategies import EasyAI, MediumAI, HardAI
from tournament import Tournament


def main_menu():
    """Affiche le menu principal et gère le choix de l'utilisateur."""
    options = [
        "1) Humain vs Humain",
        "2) Contre Easy AI",
        "3) Contre Medium AI",
        "4) Contre Hard AI",
        "5) Tournoi d'IA",
        "6) Quitter"
    ]

    while True:
        print("\n=== Othello AI ===")
        for opt in options:
            print(opt)
        choix = input("\nVotre choix [1-6] : ").strip()

        if choix == '1':
            human_vs_human()
        elif choix == '2':
            human_vs_ai(EasyAI('W'))  # Vous jouez en Noir
        elif choix == '3':
            human_vs_ai(MediumAI('W'))
        elif choix == '4':
            human_vs_ai(HardAI('W'))
        elif choix == '5':
            nb = input("Nombre de parties par affrontement (défaut 50) : ").strip()
            nb = int(nb) if nb.isdigit() and int(nb) > 0 else 50
            fichier_resultats = input("Nom du fichier pour enregistrer les résultats (défaut: 'resultats_tournoi.txt') : ").strip()
            fichier_resultats = fichier_resultats if fichier_resultats else "resultats_tournoi.txt"
            Tournament().full_tournament(nb, fichier_resultats)
        elif choix == '6':
            print("Au revoir !")
            sys.exit()
        else:
            print("Choix invalide, veuillez réessayer.")


if __name__ == '__main__':
    main_menu()