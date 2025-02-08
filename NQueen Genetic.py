import numpy as np
import tkinter as tk
from tkinter import scrolledtext

# Initialize population for N-Queens
def init_pop(pop_size, N):
    return np.random.randint(N, size=(pop_size, N))

# Calculate fitness values based on the N-Queens problem
def cal_fitness(population, N):
    fitness_values = []
    for x in population:
        penalty = 0
        for i in range(N):
            r = x[i]
            for j in range(N):
                if i == j:
                    continue
                d = abs(i - j)
                if x[j] in [r, r + d, r - d]:
                    penalty += 1
        fitness_values.append(penalty)
    return -1 * np.array(fitness_values)

# Selection method with fitness values
def selection(population, fitness_values):
    probs = fitness_values.copy()
    probs += abs(probs.min()) + 1  # Ensure no negative probabilities
    probs = probs / probs.sum()
    N = len(population)
    indices = np.arange(N)
    selected_indices = np.random.choice(indices, size=N, p=probs)
    selected_population = population[selected_indices]
    return selected_population

# Mutation method for N-Queens
def mutation(individual, pm, N):
    r = np.random.random()
    if r < pm:
        m = np.random.randint(N)
        individual[m] = np.random.randint(N)  # Change position of one queen
    return individual

# Crossover method for N-Queens
def crossover(parent1, parent2, pc, N):
    r = np.random.random()
    if r < pc:
        m = np.random.randint(1, N)
        child1 = np.concatenate([parent1[:m], parent2[m:]])
        child2 = np.concatenate([parent2[:m], parent1[m:]])
    else:
        child1 = parent1.copy()
        child2 = parent2.copy()
    return child1, child2

# Crossover and mutation applied to selected population
def crossover_mutation(selected_pop, pc, pm, N):
    N_individuals = len(selected_pop)
    new_pop = np.empty((N_individuals, N), dtype=int)
    for i in range(0, N_individuals, 2):
        parent1 = selected_pop[i]
        parent2 = selected_pop[i + 1]
        child1, child2 = crossover(parent1, parent2, pc, N)
        new_pop[i] = child1
        new_pop[i + 1] = child2
    for i in range(N_individuals):
        mutation(new_pop[i], pm, N)
    return new_pop

# Main function to solve N-Queens problem
def n_queens(pop_size, max_generations, N, pc=0.7, pm=0.01, result_text=None, board_canvas=None):
    population = init_pop(pop_size, N)
    best_fitness_overall = None
    best_solution = None  # Initialize best_solution variable

    for i_gen in range(max_generations):
        fitness_vals = cal_fitness(population, N)
        best_i = fitness_vals.argmax()
        best_fitness = fitness_vals[best_i]

        # Update best solution if current one is better
        if best_fitness_overall is None or best_fitness > best_fitness_overall:
            best_fitness_overall = best_fitness
            best_solution = population[best_i]

        # Print current generation information and the best solution
        result_text.insert(tk.END, f'Generation {i_gen: 06} - Fitness: {-best_fitness_overall:03} - Best Solution: {best_solution}\n')
        result_text.yview(tk.END)  # Scroll to the bottom

        # Visualize the best solution on the board
        if best_solution is not None:
            draw_board(best_solution, N, board_canvas)

        # If optimal solution is found (fitness == 0), break the loop
        if best_fitness == 0:
            result_text.insert(tk.END, 'Found optimal solution!\n')
            result_text.yview(tk.END)
            break

        # Select the next generation and apply crossover and mutation
        selected_pop = selection(population, fitness_vals)
        population = crossover_mutation(selected_pop, pc, pm, N)

    # At the end of the algorithm, print the best solution found
    if best_solution is not None:
        result_text.insert(tk.END, "\nBest Solution Found:\n")
        result_text.insert(tk.END, f'{best_solution}\n')
        result_text.yview(tk.END)
    else:
        result_text.insert(tk.END, "\nNo solution found within the max generations\n")
        result_text.yview(tk.END)

# Function to draw the board on the canvas
def draw_board(solution, N, board_canvas):
    board_canvas.delete("all")  # Clear previous board
    
    # Set size of each cell in the grid
    cell_size = 40

    # Draw the grid
    for i in range(N):
        for j in range(N):
            color = 'white' if (i + j) % 2 == 0 else 'lightgray'
            board_canvas.create_rectangle(j * cell_size, i * cell_size,
                                           (j + 1) * cell_size, (i + 1) * cell_size,
                                           fill=color, outline='black')
    
    # Draw queens on the board
    for i in range(N):
        queen_x = solution[i]
        board_canvas.create_text(queen_x * cell_size + cell_size / 2,
                                 i * cell_size + cell_size / 2,
                                 text="Q", font=("Arial", 20, "bold"), fill="red")

# GUI Application
def create_gui():
    def on_start_button_click():
        # Get N value and other parameters
        N = int(entry_N.get())
        pop_size = int(entry_pop_size.get())
        max_generations = int(entry_max_gen.get())
        pc = float(entry_pc.get())
        pm = float(entry_pm.get())
        
        # Clear the previous result and board
        result_text.delete(1.0, tk.END)
        board_canvas.delete("all")
        
        # Start the N-Queens solution
        n_queens(pop_size, max_generations, N, pc, pm, result_text, board_canvas)

    # Create the main window
    root = tk.Tk()
    root.title("N-Queens Genetic Algorithm")

    # Add input fields and labels
    tk.Label(root, text="Enter N (size of the board):").pack()
    entry_N = tk.Entry(root)
    entry_N.pack()

    tk.Label(root, text="Enter Population Size:").pack()
    entry_pop_size = tk.Entry(root)
    entry_pop_size.pack()

    tk.Label(root, text="Enter Max Generations:").pack()
    entry_max_gen = tk.Entry(root)
    entry_max_gen.pack()

    tk.Label(root, text="Enter Crossover Probability (pc):").pack()
    entry_pc = tk.Entry(root)
    entry_pc.pack()

    tk.Label(root, text="Enter Mutation Probability (pm):").pack()
    entry_pm = tk.Entry(root)
    entry_pm.pack()

    # Add the "Start" button to begin the algorithm
    start_button = tk.Button(root, text="Start", command=on_start_button_click)
    start_button.pack()

    # Add a scrolled text widget to show the result
    result_text = scrolledtext.ScrolledText(root, width=80, height=10)
    result_text.pack()

    # Create a Canvas widget to display the N-Queens board
    board_canvas = tk.Canvas(root, width=400, height=400)
    board_canvas.pack()

    # Start the Tkinter event loop
    root.mainloop()

# Run the GUI application
create_gui()
