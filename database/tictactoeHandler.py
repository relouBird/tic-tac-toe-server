import math
from typing import List, Tuple

# Fonction pour afficher le plateau
def display_board(board):
    for i in range(3):
        print(board[3*i : 3*i+3])

# Vérifier si un joueur a gagné
def check_winner(board, player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), 
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True, "Player {} is the winner".format(player)
    return False, ""

# Vérifier s'il y a un match nul
def check_draw(board):
    return "" not in board

# Minimax: cherche à maximiser le score de l'IA et minimiser celui du joueur
def minimax(board, depth, is_maximizing):
    if check_winner(board, "O")[0]:
        return 1  # L'IA gagne
    elif check_winner(board, "X")[0]:
        return -1  # Le joueur gagne
    elif check_draw(board):
        return 0  # Match nul

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = ""
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = ""
                best_score = min(score, best_score)
        return best_score

# Fonction pour trouver le meilleur mouvement pour l'IA
def best_move(board):
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

# Exemple de plateau vide
board = ["", "", "",
         "", "", "",
         "", "", ""]
def renderBoard(tableData: List[Tuple[str,int]]):
    # Exemple de plateau vide
    boardRender = ["", "", "",
            "", "", "",
            "", "", ""]
    for data in tableData:
        if data[0] != "AI":
            boardRender[data[1]-1] = "X"
        else:
            boardRender[data[1]-1] = "O"
    return boardRender

# Fonction pour vérifier si toutes les cases sont pleines (vérification complète du tableau)
def verificationFor():
    return all([l != "" for l in board])

if __name__ == "__main__":
    # Boucle de jeu
    while True:
        display_board(board)
        
        # Tour du joueur
        player_move = input("Choisissez une case (0-8) : ")
        
        # Validation de l'entrée du joueur
        if not player_move.isdigit() or int(player_move) not in range(9) or board[int(player_move)] != "":
            print("Entrée invalide, réessayez.")
            continue
        
        board[int(player_move)] = "X"
        
        # Vérifier si le joueur a gagné
        if check_winner(board, "X")[0]:
            display_board(board)
            print(check_winner(board, "X")[1])
            break

        # Vérifier le match nul
        if check_draw(board):
            display_board(board)
            print("Match nul")
            break

        # Tour de l'IA
        ia_move = best_move(board)
        board[ia_move] = "O"

        # Vérifier si l'IA a gagné
        if check_winner(board, "O")[0]:
            display_board(board)
            print(check_winner(board, "O")[1])
            break

        # Vérifier le match nul après le coup de l'IA
        if check_draw(board):
            display_board(board)
            print("Match nul")
            break