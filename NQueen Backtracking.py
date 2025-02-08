import tkinter as tk
from tkinter import messagebox


class NQueensGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queens Solver")

        self.label = tk.Label(root, text="Enter the value of N:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(root)
        self.entry.pack(pady=10)

        self.solve_button = tk.Button(root, text="Solve", command=self.solve)
        self.solve_button.pack(pady=10)

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack(pady=10)

        self.navigation_frame = tk.Frame(root)
        self.navigation_frame.pack(pady=10)

        self.prev_button = tk.Button(
            self.navigation_frame, text="Previous Solution", command=self.prev_solution
        )
        self.next_button = tk.Button(
            self.navigation_frame, text="Next Solution", command=self.next_solution
        )

        self.solutions = []
        self.solution_idx = 0

    def solve_n_queens(self, n):
        col = set()
        pos_diag = set()  # r+c
        neg_diag = set()  # r-c

        res = []
        board = [["."] * n for _ in range(n)]

        def backtrack(r):
            if r == n:
                copy = ["".join(row) for row in board]
                res.append(copy)
                return

            for c in range(n):
                if c in col or (r + c) in pos_diag or (r - c) in neg_diag:
                    continue

                col.add(c)
                pos_diag.add(r + c)
                neg_diag.add(r - c)
                board[r][c] = "Q"
                backtrack(r + 1)

                col.remove(c)
                pos_diag.remove(r + c)
                neg_diag.remove(r - c)
                board[r][c] = "."

        backtrack(0)
        return res

    def solve(self):
        try:
            n = int(self.entry.get())
            if n <= 0:
                raise ValueError

            self.solutions = self.solve_n_queens(n)
            if not self.solutions:
                messagebox.showinfo("No Solutions", f"No solutions exist for N = {n}")
                return

            self.solution_idx = 0
            self.update_navigation_buttons()
            self.draw_board(self.solutions[self.solution_idx])
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a positive integer.")

    def draw_board(self, solution):
        self.canvas.delete("all")
        n = len(solution)
        square_size = min(400 // n, 50)
        for i in range(n):
            for j in range(n):
                x1, y1 = j * square_size, i * square_size
                x2, y2 = x1 + square_size, y1 + square_size
                color = "white" if (i + j) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                if solution[i][j] == "Q":
                    self.canvas.create_text(
                        (x1 + x2) // 2,
                        (y1 + y2) // 2,
                        text="Q",
                        font=("Arial", square_size // 2),
                        fill="red",
                    )

    def next_solution(self):
        self.solution_idx += 1
        self.update_navigation_buttons()
        self.draw_board(self.solutions[self.solution_idx])

    def prev_solution(self):
        self.solution_idx -= 1
        self.update_navigation_buttons()
        self.draw_board(self.solutions[self.solution_idx])

    def update_navigation_buttons(self):
        # Hide/show "Previous Solution" button
        if self.solution_idx > 0:
            self.prev_button.pack(side="left", padx=10)
        else:
            self.prev_button.pack_forget()

        # Hide/show "Next Solution" button
        if self.solution_idx < len(self.solutions) - 1:
            self.next_button.pack(side="right", padx=10)
        else:
            self.next_button.pack_forget()


if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensGUI(root)
    root.mainloop()
