# othello_ai.py
import math
import time
import random
from othello_game import OthelloGame

#  Classe de base
class AI:
    def __init__(self, player: str):
        self.player = player
        self.opponent = 'W' if player == 'B' else 'B'
        self.name = "Base AI"
        self.moves_evaluated = 0
        self.thinking_time = 0.0

    def get_valid_moves(self, game):
        return game.get_valid_moves()

    def get_move(self, game):
        raise NotImplementedError("À implémenter dans les sous-classes")
#  Fonctions d'évaluation partagées
def evaluate_simple(game: OthelloGame, player: str) -> float:
    """Évaluation basique: différence de pions, contrôle des coins et des bords."""
    opponent = 'W' if player == 'B' else 'B'
    board = game.board
    score = 0.0
    
    # Différence basique de pions
    p_count = sum(row.count(player) for row in board)
    o_count = sum(row.count(opponent) for row in board)
    score += (p_count - o_count)
    
    # Occupation des coins (+25 chacun, -25 pour l'adversaire)
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for r, c in corners:
        if board[r][c] == player:
            score += 25
        elif board[r][c] == opponent:
            score -= 25
    
    # Pions sur les bords (+5 chacun, -5 pour l'adversaire)
    edges = []
    for i in range(1, 7):
        edges.extend([(0, i), (7, i), (i, 0), (i, 7)])
    
    for r, c in edges:
        if board[r][c] == player:
            score += 5
        elif board[r][c] == opponent:
            score -= 5
    
    return score
def evaluate_advanced(game: OthelloGame, player: str) -> float:
    """Évaluation avancée avec mobilité, stabilité et conscience de fin de partie."""
    opponent = 'W' if player == 'B' else 'B'
    board = game.board
    
    # Commencer par l'évaluation de base
    score = evaluate_simple(game, player)
    
    # Mobilité (+2 pour chaque coup légal, -2 pour l'adversaire)
    p_mobility = len(game.get_valid_moves(player))
    o_mobility = len(game.get_valid_moves(opponent))
    score += 2 * (p_mobility - o_mobility)
    
    # Mobilité potentielle (cases frontières)
    p_frontier, o_frontier = 0, 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == ' ':
                # Compter les pions adjacents
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if game.is_on_board(nr, nc):
                            if board[nr][nc] == player:
                                p_frontier += 1
                            elif board[nr][nc] == opponent:
                                o_frontier += 1
    
    score += (o_frontier - p_frontier)  # Moins de pions frontières est mieux
    
    # Estimation de stabilité (les coins propagent la stabilité)
    # Pénalité pour les cases X (-15)
    x_squares = [(0, 1), (1, 0), (1, 1), (0, 6), (1, 6), (1, 7),
                (6, 0), (6, 1), (7, 1), (6, 6), (6, 7), (7, 6)]
    
    for r, c in x_squares:
        if board[r][c] == player:
            # Pénaliser la case X seulement si le coin adjacent est vide
            if (r <= 1 and c <= 1 and board[0][0] == ' ') or \
               (r <= 1 and c >= 6 and board[0][7] == ' ') or \
               (r >= 6 and c <= 1 and board[7][0] == ' ') or \
               (r >= 6 and c >= 6 and board[7][7] == ' '):
                score -= 15
        elif board[r][c] == opponent:
            # Une case X adverse est bonne pour nous (si le coin est vide)
            if (r <= 1 and c <= 1 and board[0][0] == ' ') or \
               (r <= 1 and c >= 6 and board[0][7] == ' ') or \
               (r >= 6 and c <= 1 and board[7][0] == ' ') or \
               (r >= 6 and c >= 6 and board[7][7] == ' '):
                score += 15
    
    # Bonus de parité pour le dernier coup quand ≤ 8 cases vides (+10)
    empty_count = sum(row.count(' ') for row in board)
    if empty_count <= 8:
        # S'il y a un nombre impair de cases vides et c'est notre tour,
        # on fera le dernier coup (bon)
        if empty_count % 2 == 1 and game.current_player == player:
            score += 10
        # S'il y a un nombre pair de cases vides et c'est le tour de l'adversaire,
        # on fera le dernier coup (bon)
        elif empty_count % 2 == 0 and game.current_player == opponent:
            score += 10
    
    return score
#  IA Facile (profondeur 1, heuristique simple)
class EasyAI(AI):
    def __init__(self, player):
        super().__init__(player)
        self.name = "Easy AI"
        self.max_depth = 1

    def minimax(self, game, depth, α, β, maxi):
        self.moves_evaluated += 1
        if game.game_over or depth == self.max_depth:
            return evaluate_simple(game, self.player)

        best = -math.inf if maxi else math.inf
        for mv in game.get_valid_moves():
            g2 = game.clone()
            g2.place_disc(*mv)
            val = self.minimax(g2, depth + 1, α, β, not maxi)
            if maxi:
                best = max(best, val)
                α = max(α, best)
            else:
                best = min(best, val)
                β = min(β, best)
            if α >= β:
                break
        return best

    def get_move(self, game):
        self.moves_evaluated = 0
        t0 = time.time()
        valid = game.get_valid_moves()
        if not valid:
            self.thinking_time = time.time() - t0
            return None

        # Vérifier une victoire immédiate
        for mv in valid:
            t = game.clone()
            t.place_disc(*mv)
            if t.game_over and t.winner == self.player:
                self.thinking_time = time.time() - t0
                return mv

        best_mv, best_score = None, -math.inf
        for mv in valid:
            g2 = game.clone()
            g2.place_disc(*mv)
            score = self.minimax(g2, 1, -math.inf, math.inf, False)
            if score > best_score:
                best_score, best_mv = score, mv

        self.thinking_time = time.time() - t0
        return best_mv
#  IA Moyenne (profondeur 4, heuristique simple +limite temps(10s)+ ordre des coups)
class MediumAI(AI):
    def __init__(self, player):
        super().__init__(player)
        self.name = "Medium AI"
        self.max_depth = 4
        self.time_limit = 10.0
        self.depth_reached = 0

    def prioritize_moves(self, game, moves):
        corners = {(0, 0), (0, 7), (7, 0), (7, 7)}
        edges = {(0, i) for i in range(1, 7)} | {(7, i) for i in range(1, 7)} | {(i, 0) for i in range(1, 7)} | {(i, 7) for i in range(1, 7)}
        return sorted(moves, key=lambda mv: (0 if mv in corners else 1 if mv in edges else 2))

    def minimax(self, game, depth, α, β, maxi, start_time):
        if time.time() - start_time > self.time_limit:
            return None

        self.moves_evaluated += 1
        self.depth_reached = max(self.depth_reached, depth)

        if game.game_over or depth == self.max_depth:
            return evaluate_simple(game, self.player)

        moves = game.get_valid_moves()
        if not moves:
            g2 = game.clone()
            g2.current_player = 'W' if g2.current_player == 'B' else 'B'
            return self.minimax(g2, depth, α, β, not maxi, start_time)

        ordered = self.prioritize_moves(game, moves)
        best = -math.inf if maxi else math.inf

        for mv in ordered:
            g2 = game.clone()
            g2.place_disc(*mv)
            val = self.minimax(g2, depth + 1, α, β, not maxi, start_time)
            if val is None: return None  # timeout
            if maxi:
                best = max(best, val)
                α = max(α, best)
            else:
                best = min(best, val)
                β = min(β, best)
            if α >= β: break
        return best

    def get_move(self, game):
        self.moves_evaluated = 0
        self.depth_reached = 0
        t0 = time.time()
        valid = game.get_valid_moves()
        if not valid:
            self.thinking_time = time.time() - t0
            print(f"[Medium AI] Profondeur max atteinte: {self.depth_reached}")
            return None

        best_mv, best_score = None, -math.inf
        for mv in self.prioritize_moves(game, valid):
            g2 = game.clone()
            g2.place_disc(*mv)
            score = self.minimax(g2, 1, -math.inf, math.inf, False, t0)
            if score is None: break  # timeout
            if score > best_score:
                best_score, best_mv = score, mv

        self.thinking_time = time.time() - t0
        print(f"[Medium AI] Profondeur max atteinte: {self.depth_reached}")
        return best_mv
#  IA Difficile (approfondissement itératif jusquà 6 , limite de temps (10s), table de transposition)
class HardAI(AI):
    def __init__(self, player):
        super().__init__(player)
        self.name = "Hard AI"
        self.time_limit = 10.0
        self.max_depth = 5
        self.depth_reached = 0

    def board_hash(self, game):
        return "".join("".join(r) for r in game.board) + "_" + game.current_player

    def prioritize_moves(self, game, moves, depth):
        corners = {(0, 0), (0, 7), (7, 0), (7, 7)}
        x_squares = {(1, 1): (0, 0), (1, 6): (0, 7), (6, 1): (7, 0), (6, 6): (7, 7)}
        scores = []
        for r, c in moves:
            s = 1000 if (r, c) in corners else 500 if r in [0, 7] or c in [0, 7] else 0
            if (r, c) in x_squares and game.board[x_squares[(r, c)][0]][x_squares[(r, c)][1]] == ' ':
                s -= 700
            if hasattr(self, "killer_moves") and self.killer_moves.get(depth) == (r, c):
                s += 800
            if hasattr(self, "history_table"):
                s += self.history_table.get((r, c, game.current_player), 0)
            scores.append((s, (r, c)))
        return [mv for _, mv in sorted(scores, reverse=True)]

    def minimax(self, game, d, a, b, maxing, t0):
        if time.time() - t0 > self.time_limit:
            return None
        key = self.board_hash(game)
        if hasattr(self, "transposition_table"):
            tt = self.transposition_table.get(key)
            if tt and tt["depth"] >= d:
                v = tt["value"]
                if tt["type"] == "exact": return v
                if tt["type"] == "lower" and v > a: a = v
                if tt["type"] == "upper" and v < b: b = v
                if a >= b: return v
        if game.game_over:
            return 10000 if game.winner == self.player else -10000 if game.winner else 0
        if d == 0: return evaluate_advanced(game, self.player)
        moves = game.get_valid_moves()
        if not moves:
            g2 = game.clone()
            g2.current_player = 'W' if g2.current_player == 'B' else 'B'
            return self.minimax(g2, d, a, b, not maxing, t0)
        best = -math.inf if maxing else math.inf
        for mv in self.prioritize_moves(game, moves, d):
            g2 = game.clone(); g2.place_disc(*mv)
            val = self.minimax(g2, d-1, a, b, not maxing, t0)
            if val is None: return None
            if maxing:
                if val > best: best = val
                a = max(a, best)
            else:
                if val < best: best = val
                b = min(b, best)
            if a >= b:
                if hasattr(self, "killer_moves"):
                    self.killer_moves[d] = mv
                if hasattr(self, "history_table"):
                    k = (mv[0], mv[1], game.current_player)
                    self.history_table[k] = self.history_table.get(k, 0) + 2 ** d
                break
        if hasattr(self, "transposition_table"):
            t = "exact" if a < best < b else "lower" if best >= b else "upper"
            self.transposition_table[key] = {"value": best, "depth": d, "type": t}
        return best

    def get_move(self, game):
        import time
        t0 = time.time()
        self.depth_reached = 0
        valid = game.get_valid_moves()
        if not valid: print(f"[Hard AI] Profondeur max atteinte: {self.depth_reached}"); return None
        if len(valid) == 1: print(f"[Hard AI] Profondeur max atteinte: {self.depth_reached}"); return valid[0]

        self.transposition_table = {}; self.killer_moves = {}; self.history_table = {}
        best_mv, best_score = None, -math.inf

        for d in range(1, self.max_depth + 1):
            if time.time() - t0 > self.time_limit * 0.8: break
            a, b = (best_score - 50, best_score + 50) if d > 1 else (-math.inf, math.inf)
            move, score = None, -math.inf
            for mv in self.prioritize_moves(game, valid, d):
                g2 = game.clone(); g2.place_disc(*mv)
                val = self.minimax(g2, d - 1, a, b, False, t0)
                if val is None: break
                if val > score: move, score = mv, val
            if move: best_mv, best_score = move, score; self.depth_reached = d
            if best_score > 9000: break
        print(f"[Hard AI] Profondeur max atteinte: {self.depth_reached}") # affiche la profondeur max atteinte pour chaque coup
        return best_mv