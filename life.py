import tkinter as tk


class GameOfLife:
    def __init__(self, rows=50, cols=50):
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]

    def step(self):
        new_board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                neighbors = self.get_neighbors(row, col)
                if self.board[row][col] == 1:
                    if neighbors in [2, 3]:
                        new_board[row][col] = 1
                elif neighbors == 3:
                    new_board[row][col] = 1
        self.board = new_board

    def get_neighbors(self, row, col):
        neighbors = 0
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                neighbors += self.board[r][c]
        neighbors -= self.board[row][col]
        return neighbors


class GameOfLifeGUI:
    def __init__(self, rows=50, cols=50):
        self.game = GameOfLife(rows, cols)
        self.cell_size = 10
        self.running = False

        self.window = tk.Tk()
        self.window.title("Conway's Game of Life")

        self.canvas = tk.Canvas(
            self.window, width=cols * self.cell_size, height=rows * self.cell_size
        )
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.toggle_cell)
        self.start_button = tk.Button(
            self.window, text="Start", command=self.start_game
        )
        self.start_button.pack(side=tk.LEFT)
        self.stop_button = tk.Button(self.window, text="Stop", command=self.stop_game)
        self.stop_button.pack(side=tk.LEFT)
        self.step_button = tk.Button(self.window, text="Step", command=self.step_game)
        self.step_button.pack(side=tk.LEFT)
        self.clear_button = tk.Button(
            self.window, text="Clear", command=self.clear_game
        )
        self.clear_button.pack(side=tk.LEFT)

        self.draw_board()

    def start_game(self):
        self.running = True
        self.run_game()

    def stop_game(self):
        self.running = False

    def step_game(self):
        self.game.step()
        self.draw_board()

    def clear_game(self):
        self.game = GameOfLife(self.game.rows, self.game.cols)
        self.draw_board()

    def run_game(self):
        while self.running:
            self.game.step()
            self.draw_board()
            self.window.update()
            self.window.after(100)

    def toggle_cell(self, event):
        row = event.y // self.cell_size
        col = event.x // self.cell_size
        self.game.board[row][col] = 1 - self.game.board[row][col]
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                if self.game.board[row][col] == 1:
                    self.canvas.create_rectangle(
                        col * self.cell_size,
                        row * self.cell_size,
                        (col + 1) * self.cell_size,
                        (row + 1) * self.cell_size,
                        fill="black",
                        outline="white",
                    )
                else:
                    self.canvas.create_rectangle(
                        col * self.cell_size,
                        row * self.cell_size,
                        (col + 1) * self.cell_size,
                        (row + 1) * self.cell_size,
                        fill="white",
                        outline="white",
                    )
        self.canvas.pack()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = GameOfLifeGUI()
    gui.run()
