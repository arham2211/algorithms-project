import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import random
import time

def closest_pair_algorithm(points):
    # Placeholder for the actual implementation
    return "Closest Pair: (x1, y1) and (x2, y2)", 0.123  # Replace with actual logic

def integer_multiplication(a, b):
    # Placeholder for the actual implementation
    return a * b, 0.001  # Replace with actual logic

def open_file():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        with open(filename, 'r') as file:
            data = file.read()
        input_text.set(data)
        selected_file.set(filename)
    else:
        messagebox.showinfo("Info", "No file selected.")

def run_algorithm():
    algo = selected_algorithm.get()
    data = input_text.get()
    if not data.strip():
        messagebox.showwarning("Warning", "No data loaded.")
        return

    start_time = time.time()
    if algo == "Closest Pair of Points":
        # Parse data into points
        points = [tuple(map(int, line.split())) for line in data.strip().split('\n')]
        result, exec_time = closest_pair_algorithm(points)
        visualize_points(points)
    elif algo == "Integer Multiplication":
        # Parse data into two integers
        numbers = list(map(int, data.strip().split()))
        result, exec_time = integer_multiplication(numbers[0], numbers[1])
    else:
        result, exec_time = "Invalid Algorithm", 0

    output_text.set(f"Result: {result}\nExecution Time: {exec_time:.4f} seconds")

def visualize_points(points):
    x, y = zip(*points)
    plt.scatter(x, y, color='blue')
    plt.title("Closest Pair of Points Visualization")
    plt.show()

# GUI Setup
root = tk.Tk()
root.title("Divide and Conquer Algorithms")

selected_algorithm = tk.StringVar(value="Closest Pair of Points")
selected_file = tk.StringVar(value="No file selected")
input_text = tk.StringVar(value="")
output_text = tk.StringVar(value="")

tk.Label(root, text="Choose Algorithm:").grid(row=0, column=0, padx=10, pady=10)
tk.OptionMenu(root, selected_algorithm, "Closest Pair of Points", "Integer Multiplication").grid(row=0, column=1)

tk.Button(root, text="Load File", command=open_file).grid(row=1, column=0, pady=10)
tk.Label(root, textvariable=selected_file, wraplength=300).grid(row=1, column=1)

tk.Button(root, text="Run", command=run_algorithm).grid(row=2, column=0, pady=10)
tk.Label(root, text="Output:").grid(row=3, column=0, padx=10, pady=10)
tk.Label(root, textvariable=output_text, wraplength=500).grid(row=3, column=1, padx=10)

tk.Button(root, text="Exit", command=root.quit).grid(row=4, column=0, pady=10)

root.mainloop()