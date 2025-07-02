import tkinter as tk
from tkinter import messagebox

import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")

        self.board = [[" "]*3 for _ in range(3)]
        self.buttons = [[None]*3 for _ in range(3)]
        self.current_player = "X"
        self.single_player = False
        self.difficulty = "easy"
        self.scores = {"X": 0, "O": 0, "Tie": 0}

        self.create_widgets()
        self.ask_mode()

    def create_widgets(self):
        self.status_label = tk.Label(self.root, text="Tic-Tac-Toe", font=('Helvetica', 16))
        self.status_label.grid(row=0, column=0, columnspan=3)

        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text=" ", font=('Helvetica', 24), width=5, height=2,
                                command=lambda r=i, c=j: self.cell_clicked(r, c))
                btn.grid(row=i+1, column=j)
                self.buttons[i][j] = btn

        self.score_label = tk.Label(self.root, text="", font=('Helvetica', 12))
        self.score_label.grid(row=4, column=0, columnspan=3)

    def ask_mode(self):
        answer = messagebox.askquestion("Game Mode", "Do you want to play single-player?")
        if answer == 'yes':
            self.single_player = True
            self.ask_difficulty_dropdown()
        else:
            self.single_player = False
        self.update_status()
        self.update_score()

    def ask_difficulty_dropdown(self):
        top = tk.Toplevel(self.root)
        top.title("Select Difficulty")

        tk.Label(top, text="Choose difficulty:").pack(pady=10)
        var = tk.StringVar(value="easy")

        def set_difficulty():
            self.difficulty = var.get()
            top.destroy()

        tk.OptionMenu(top, var, "easy", "medium", "hard").pack()
        tk.Button(top, text="Start", command=set_difficulty).pack(pady=10)

        top.grab_set()  # Make this window modal

    def update_status(self):
        if self.single_player:
            self.status_label.config(text=f"1-Player | Difficulty: {self.difficulty.capitalize()} | Your Turn (X)")
        else:
            self.status_label.config(text=f"2-Player | {self.current_player}'s Turn")

    def update_score(self):
        self.score_label.config(text=f"Score — X: {self.scores['X']} | O: {self.scores['O']} | Ties: {self.scores['Tie']}")

    def cell_clicked(self, row, col):
        if self.board[row][col] != " ":
            return

        self.make_move(row, col, self.current_player)
        if self.check_winner(self.current_player):
            self.end_game(f"{self.current_player} wins!")
            self.scores[self.current_player] += 1
            return
        elif self.is_tie():
            self.end_game("It's a tie!")
            self.scores["Tie"] += 1
            return

        self.current_player = "O" if self.current_player == "X" else "X"
        self.update_status()

        if self.single_player and self.current_player == "O":
            self.root.after(300, self.ai_move)

    def make_move(self, row, col, player):
        self.board[row][col] = player
        self.buttons[row][col].config(text=player, state="disabled")

    def ai_move(self):
        if self.difficulty == "easy":
            move = self.ai_easy()
        elif self.difficulty == "medium":
            move = self.ai_medium()
        else:
            move = self.ai_hard()
        if move:
            self.cell_clicked(*move)

    def ai_easy(self):
        return random.choice([(r, c) for r in range(3) for c in range(3) if self.board[r][c] == " "])

    def ai_medium(self):
        for r, c in self.get_empty_cells():
            self.board[r][c] = "O"
            if self.check_winner("O"):
                self.board[r][c] = " "
                return (r, c)
            self.board[r][c] = " "

        for r, c in self.get_empty_cells():
            self.board[r][c] = "X"
            if self.check_winner("X"):
                self.board[r][c] = " "
                return (r, c)
            self.board[r][c] = " "

        return self.ai_easy()

    def ai_hard(self):
        best_score = -float('inf')
        best_move = None
        for r, c in self.get_empty_cells():
            self.board[r][c] = "O"
            score = self.minimax(False)
            self.board[r][c] = " "
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_move

    def minimax(self, is_maximizing):
        if self.check_winner("O"):
            return 1
        if self.check_winner("X"):
            return -1
        if self.is_tie():
            return 0

        if is_maximizing:
            best = -float('inf')
            for r, c in self.get_empty_cells():
                self.board[r][c] = "O"
                score = self.minimax(False)
                self.board[r][c] = " "
                best = max(score, best)
            return best
        else:
            best = float('inf')
            for r, c in self.get_empty_cells():
                self.board[r][c] = "X"
                score = self.minimax(True)
                self.board[r][c] = " "
                best = min(score, best)
            return best

    def get_empty_cells(self):
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == " "]

    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_tie(self):
        return all(cell != " " for row in self.board for cell in row)

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.update_score()
        self.ask_restart()

    def ask_restart(self):
        again = messagebox.askyesno("Play Again?", "Do you want to play another game?")
        if again:
            self.reset_board()
        else:
            self.root.destroy()

    def reset_board(self):
        self.board = [[" "]*3 for _ in range(3)]
        self.current_player = "X"
        for i in range(3):
            for j in range(3):
                btn = self.buttons[i][j]
                btn.config(text=" ", state="normal")
        self.update_status()

# ---------- Start the Game ----------

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
