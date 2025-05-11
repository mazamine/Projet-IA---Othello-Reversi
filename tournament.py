# othello_tournament.py — Gère les affrontements entre IA et affiche les résultats

import random
from othello_game import OthelloGame
from ai_strategies import EasyAI, MediumAI, HardAI

class Tournament:
    """Organise les matchs entre IA et collecte les statistiques."""
    def __init__(self):
        self.results = []

    def run_match(self, ai1, ai2, num_games: int = 50):
        """Joue `num_games` parties entre `ai1` et `ai2`, en alternant les couleurs."""
        stats = {
            ai1.name: 0,
            ai2.name: 0,
            'draws': 0,
            'disc_diff': {ai1.name: 0, ai2.name: 0},
            'total_discs': {ai1.name: 0, ai2.name: 0}
        }

        print(f"Match {ai1.name} vs {ai2.name}:")
        for i in range(num_games):
            # Afficher la barre de progression
            progress = int((i + 1) / num_games * 50)  # 50 caractères pour la barre
            bar = f"[{'#' * progress}{'.' * (50 - progress)}] {i + 1}/{num_games}\n"
            print(f"\r{bar}", end='')

            game = OthelloGame()
            # Détermine qui joue Noir (B) ou Blanc (W)
            if i % 2 == 0:
                players = {'B': ai1, 'W': ai2}
            else:
                players = {'B': ai2, 'W': ai1}
            for color, ai in players.items():
                ai.player = color
                ai.opponent = 'W' if color == 'B' else 'B'

            # Déroulement de la partie
            while not game.game_over:
                current = players[game.current_player]
                move = current.get_move(game)
                if move is None:
                    # Passage de tour
                    game.current_player = game.get_opponent()
                    if not game.get_valid_moves():
                        game.check_game_state()
                    continue
                game.place_disc(*move)

            # Bilan de la partie
            b_score, w_score = game.get_score()
            # Mise à jour victoire / nul
            if game.winner:
                stats[players[game.winner].name] += 1
            else:
                stats['draws'] += 1
            # Différence de disques
            diff = b_score - w_score
            stats['disc_diff'][players['B'].name] += diff
            stats['disc_diff'][players['W'].name] -= diff
            # Total de disques pour moyenne
            stats['total_discs'][players['B'].name] += b_score
            stats['total_discs'][players['W'].name] += w_score

        print()  # Nouvelle ligne après la barre de progression
        record = {
            'matchup': f"{ai1.name} vs {ai2.name}",
            'stats': stats,
            'num_games': num_games
        }
        self.results.append(record)
        return record

    def full_tournament(self, num_games: int = 50, output_file: str = "resultats_tournoi.txt"):
        """Lance le tournoi Easy vs Medium vs Hard et affiche un résumé clair, enregistre les résultats dans un fichier."""
        ais = [EasyAI('B'), MediumAI('B'), HardAI('B')]
        print("\n=== Tournoi Othello IA ===")
        print(f"Parties par affrontement : {num_games}\n")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=== Tournoi Othello IA ===\n")
            f.write(f"Parties par affrontement : {num_games}\n\n")

            for i in range(len(ais)):
                for j in range(i + 1, len(ais)):
                    ai1, ai2 = ais[i], ais[j]
                    print(f"--- {ai1.name} vs {ai2.name} ---")
                    f.write(f"--- {ai1.name} vs {ai2.name} ---\n")
                    rec = self.run_match(ai1, ai2, num_games)
                    s = rec['stats']
                    ng = rec['num_games']

                    # Victoires / nuls
                    w1, w2, nd = s[ai1.name], s[ai2.name], s['draws']
                    p1 = w1 / ng * 100
                    p2 = w2 / ng * 100
                    pd = nd / ng * 100

                    # Moyenne de disques finaux (sur 64)
                    avg1 = s['total_discs'][ai1.name] / ng
                    avg2 = s['total_discs'][ai2.name] / ng

                    # Différence agrégée
                    diff1 = s['disc_diff'][ai1.name]
                    diff2 = s['disc_diff'][ai2.name]

                    result_str = (f"{ai1.name}: {w1} victoires ({p1:.1f}%),  "
                                  f"{ai2.name}: {w2} victoires ({p2:.1f}%),  "
                                  f"Nuls: {nd} ({pd:.1f}%)\n"
                                  f"ΔDisques: {ai1.name} {diff1:+d} | {ai2.name} {diff2:+d}\n"
                                  f"Moyenne disques finaux: {ai1.name} {avg1:.1f}/64 | {ai2.name} {avg2:.1f}/64\n")
                    
                    print(result_str)
                    f.write(result_str + "\n")

        return self.results


if __name__ == '__main__':
    try:
        ng = int(input("Nombre de parties par affrontement [défaut 50] : ") or 50)
    except:
        ng = 50
    Tournament().full_tournament(ng)
