import tkinter as tk
import heapq  # For Best-First Search (priority queue)

def print_solution(board, canvas, n, solution_num):
    """Displays the N-Queens board on the GUI."""
    canvas.delete("all")
    cell_size = 50  # Size of each cell
    for row in range(n):
        for col in range(n):
            x1, y1 = col * cell_size, row * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size

            # Alternate cell colors for the chessboard
            color = "white" if (row + col) % 2 == 0 else "gray"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)

            # Place the queen
            if board[row][col] == 1:
                canvas.create_text(
                    x1 + cell_size // 2, y1 + cell_size // 2,
                    text="Q", font=("Arial", 24), fill="red"
                )
    # Show solution number
    canvas.create_text(
        n * cell_size // 2, n * cell_size + 20,
        text=f"Solution {solution_num + 1}", font=("Arial", 16), fill="blue"
    )

def is_safe(board, row, col, n):
    """Checks if it's safe to place a queen at board[row][col]."""
    for i in range(row):
        if board[i][col]:
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j]:
            return False
    for i, j in zip(range(row, -1, -1), range(col, n)):
        if board[i][j]:
            return False
    return True

def heuristic(board, row, n):
    """Heuristic function to count the number of conflicts on the board."""
    conflicts = 0
    for r in range(row):
        for c in range(n):
            if board[r][c] == 1:
                # Count conflicts for vertical, diagonal-left, diagonal-right
                if any(board[row][c] == 1 for row in range(r+1, n)): 
                    conflicts += 1
                if any(board[row][c] == 1 for row in range(row)):
                    conflicts += 1
    return conflicts

def solve_n_queens_best_first(n):
    """Solves the N-Queens problem using Best-First Search."""
    # Priority queue: (heuristic value, board state, row)
    pq = []
    initial_board = [[0] * n for _ in range(n)]  # Start with an empty board
    heapq.heappush(pq, (0, initial_board, 0))  # (conflict count, board, row)

    solutions = []  # List to store all solutions
    while pq:
        _, board, row = heapq.heappop(pq)

        if row == n:
            # All queens placed successfully, add the solution
            solutions.append([r[:] for r in board])
            continue

        # Try placing a queen in every column of the current row
        for col in range(n):
            if is_safe(board, row, col, n):
                new_board = [r[:] for r in board]  # Copy the board
                new_board[row][col] = 1  # Place the queen
                conflict_count = heuristic(new_board, row + 1, n)
                heapq.heappush(pq, (conflict_count, new_board, row + 1))  # Push new state

    return solutions

def n_queens_gui():
    """Creates the GUI for the N-Queens problem."""
    # Main GUI window
    root = tk.Tk()
    root.title("N-Queens Problem")

    # Entry for inputting N
    tk.Label(root, text="Enter N:").pack(pady=5)
    n_entry = tk.Entry(root)
    n_entry.pack(pady=5)

    # Canvas for displaying the board
    canvas = tk.Canvas(root, width=400, height=400 + 40)
    canvas.pack(pady=10)

    # Function to start solving the N-Queens problem
    def start_n_queens():
        try:
            n = int(n_entry.get())
            if n <= 0:
                raise ValueError("N must be a positive integer.")

            # Solve using Best-First Search
            solutions = solve_n_queens_best_first(n)

            # Adjust canvas size based on N
            canvas.config(width=n * 50, height=n * 50 + 40)

            # Display solutions
            current_solution = [0]

            def show_next_solution():
                if solutions:
                    current_solution[0] = (current_solution[0] + 1) % len(solutions)
                    print_solution(solutions[current_solution[0]], canvas, n, current_solution[0])

            def show_previous_solution():
                if solutions:
                    current_solution[0] = (current_solution[0] - 1) % len(solutions)
                    print_solution(solutions[current_solution[0]], canvas, n, current_solution[0])

            # Buttons for navigation
            prev_button = tk.Button(root, text="Previous", command=show_previous_solution)
            prev_button.pack(side=tk.LEFT, padx=10, pady=10)
            next_button = tk.Button(root, text="Next", command=show_next_solution)
            next_button.pack(side=tk.RIGHT, padx=10, pady=10)

            # Show the first solution
            if solutions:
                print_solution(solutions[0], canvas, n, 0)
            else:
                canvas.delete("all")
                canvas.create_text(
                    n * 25, n * 25, text="No solution exists.", font=("Arial", 24), fill="red"
                )

        except ValueError:
            canvas.delete("all")
            canvas.create_text(
                200, 200, text="Invalid input. Enter a positive integer.", font=("Arial", 16), fill="red"
            )

    # Start button
    start_button = tk.Button(root, text="Start", command=start_n_queens)
    start_button.pack(pady=10)

    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    n_queens_gui()

