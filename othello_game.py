# othello_game.py

class OthelloGame:
    """Implémentation du jeu Othello/Reversi avec un plateau de 8×8."""
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Initialise une nouvelle partie avec les 4 pions centraux standards."""
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        # Configuration initiale
        self.board[3][3], self.board[4][4] = 'W', 'W'
        self.board[3][4], self.board[4][3] = 'B', 'B'
        self.current_player = 'B'  # B = Noir, W = Blanc
        self.game_over = False
        self.winner = None
        self.last_move = None
    
    def get_opponent(self, player=None):
        """Renvoie l'adversaire du joueur donné."""
        if player is None:
            player = self.current_player
        return 'W' if player == 'B' else 'B'
    
    def is_on_board(self, row, col):
        """Vérifie si les coordonnées sont dans les limites du plateau."""
        return 0 <= row < 8 and 0 <= col < 8
    
    def is_valid_move(self, row, col, player=None):
        """Renvoie True si placer à (row,col) encadre des pions adverses."""
        if player is None:
            player = self.current_player
        # Doit être vide et sur le plateau
        if not self.is_on_board(row, col) or self.board[row][col] != ' ':
            return False
        
        opponent = self.get_opponent(player)
        # Vérifier les 8 directions
        for dr, dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            r, c = row + dr, col + dc
            # Le premier adjacent doit être un adversaire
            if not (self.is_on_board(r, c) and self.board[r][c] == opponent):
                continue
            # Continuer au-delà de l'adversaire
            r += dr; c += dc
            while self.is_on_board(r, c) and self.board[r][c] == opponent:
                r += dr; c += dc
            # Si on termine sur un pion du joueur, c'est valide
            if self.is_on_board(r, c) and self.board[r][c] == player:
                return True
        return False
    
    def get_flipped_discs(self, row, col, player=None):
        """Renvoie la liste des positions adverses retournées par ce coup."""
        if player is None:
            player = self.current_player
        if not self.is_valid_move(row, col, player):
            return []
        
        opponent = self.get_opponent(player)
        flipped = []
        # Vérifier les 8 directions
        for dr, dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            r, c = row + dr, col + dc
            to_flip = []
            # Collecter les pions adverses
            while self.is_on_board(r, c) and self.board[r][c] == opponent:
                to_flip.append((r, c))
                r += dr; c += dc
            # Si on termine sur un pion du joueur, ceux de to_flip sont retournés
            if self.is_on_board(r, c) and self.board[r][c] == player:
                flipped.extend(to_flip)
        return flipped
    
    def place_disc(self, row, col):
        """Place un pion à (row,col), retourne les pions encadrés, met à jour le tour/état."""
        if not self.is_valid_move(row, col) or self.game_over:
            return False
        
        flips = self.get_flipped_discs(row, col)
        # Placer et retourner
        self.board[row][col] = self.current_player
        for r, c in flips:
            self.board[r][c] = self.current_player
        
        self.last_move = (row, col)
        # Vérifier la fin de partie
        self.check_game_state()
        if not self.game_over:
            # Changer de tour
            self.current_player = self.get_opponent()
            # Passer si pas de coups
            if not self.get_valid_moves():
                self.current_player = self.get_opponent()
                if not self.get_valid_moves():
                    self.check_game_state()
        return True
    
    def get_valid_moves(self, player=None):
        """Renvoie la liste des coups légaux (row,col) pour le joueur donné."""
        if player is None:
            player = self.current_player
        if self.game_over:
            return []
        moves = []
        for r in range(8):
            for c in range(8):
                if self.is_valid_move(r, c, player):
                    moves.append((r, c))
        return moves
    
    def check_game_state(self):
        """Définit game_over et winner quand il n'y a plus de coups ou plateau plein."""
        black_moves = self.get_valid_moves('B')
        white_moves = self.get_valid_moves('W')
        bcount = sum(row.count('B') for row in self.board)
        wcount = sum(row.count('W') for row in self.board)
        if bcount + wcount == 64 or (not black_moves and not white_moves):
            self.game_over = True
            if bcount > wcount:
                self.winner = 'B'
            elif wcount > bcount:
                self.winner = 'W'
            else:
                self.winner = None
    
    def get_score(self):
        """Renvoie (score_noir, score_blanc)."""
        return (sum(row.count('B') for row in self.board),
                sum(row.count('W') for row in self.board))
    
    def clone(self):
        """Copie profonde de l'état du jeu."""
        copy = OthelloGame()
        copy.board = [row[:] for row in self.board]
        copy.current_player = self.current_player
        copy.game_over = self.game_over
        copy.winner = self.winner
        copy.last_move = self.last_move
        return copy
    
    def print_board(self):
        """Affiche le plateau avec une grille UTF-8 et l'état actuel."""
        print("    " + "   ".join(str(c) for c in range(8)))
        print("  ┌" + "───┬"*7 + "───┐")
        for r in range(8):
            print(f"{r} │", end="")
            for c in range(8):
                print(f" {self.board[r][c]} │", end="")
            print()
            if r < 7:
                print("  ├" + "───┼"*7 + "───┤")
            else:
                print("  └" + "───┴"*7 + "───┘")
        b, w = self.get_score()
        print(f"\nScore: Noir (B): {b}  Blanc (W): {w}")
        print(f"Prochain tour: {'Noir (B)' if self.current_player=='B' else 'Blanc (W)'}")
        if self.last_move:
            print(f"Dernier coup: ligne {self.last_move[0]}, colonne {self.last_move[1]}\n")
def human_vs_human():
    """Jouer une partie humain contre humain dans le terminal."""
    game = OthelloGame()
    while not game.game_over:
        game.print_board()
        print(" HUMAIN vs HUMAIN ")
        valid = game.get_valid_moves()
        if not valid:
            print(f"{'Noir' if game.current_player=='B' else 'Blanc'} n'a pas de coup. Passe.")
            game.current_player = game.get_opponent()
            continue
        # Vous pouvez commenter la ligne suivante si vous ne voulez pas voir les coups valides
        print("Coups valides:", ", ".join(f"({r},{c})" for r,c in valid))
        while True:
            inp = input(f"→ Coup de {game.current_player} [ligne colonne]: ").split()
            if len(inp)==2 and all(i.isdigit() for i in inp):
                r, c = map(int, inp)
                if game.place_disc(r, c):
                    break
            print(" ! Invalide! Entrez deux chiffres 0–7, ex. `2 4`.")
    # état final
    game.print_board()
    if game.winner:
        print(f" Joueur {'Noir' if game.winner=='B' else 'Blanc'} GAGNE! ")
    else:
        print(" MATCH NUL! ")
def human_vs_ai(ai):
    """Jouer une partie humain contre IA dans le terminal."""
    from time import time
    game = OthelloGame()
    human, comp = 'B','W'
    print(f" Défi {ai.name}! Vous jouez Noir (B). \n")
    while not game.game_over:
        game.print_board()
        if game.current_player == human:
            valid = game.get_valid_moves()
            if not valid:
                print("Vous n'avez pas de coup. Passe.")
                game.current_player = game.get_opponent()
                continue
            print("Vos coups:", ", ".join(f"({r},{c})" for r,c in valid))
            while True:
                inp = input("→ Votre coup [ligne colonne]: ").split()
                if len(inp)==2 and all(i.isdigit() for i in inp):
                    r, c = map(int, inp)
                    if game.place_disc(r, c):
                        break
                print(" ! Invalide! Entrez deux chiffres 0–7.")
        else:
            valid = game.get_valid_moves()
            if not valid:
                print(f"{ai.name} n'a pas de coup. Passe.")
                game.current_player = game.get_opponent()
                continue
            print(f"\n {ai.name} réfléchit...")
            start = time()
            move = ai.get_move(game)
            ai.thinking_time = time() - start
            print(f" Temps de réflexion {ai.thinking_time:.2f}s")
            if not move:
                print(" ! Pas de coup!")
                break
            r, c = move
            game.place_disc(r, c)
            print(f" {ai.name} → ({r},{c})\n")
    # résultat final
    game.print_board()
    b, w = game.get_score()
    print(f"Score final: Noir {b} - {w} Blanc")
    if game.winner == human:
        print(" Vous GAGNEZ! ")
    elif game.winner == comp:
        print(f" {ai.name} GAGNE! ")
    else:
        print(" Match NUL! ")