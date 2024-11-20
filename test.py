import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import random
import math
import re
from dataclasses import dataclass
from typing import List, Tuple
import generate_for_cpp
import generate_for_karatsuba


# Point class for Closest Pair algorithm
@dataclass
class Point:
    x: float
    y: float
    
    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

# --- Karatsuba Helper Functions ---
def findSum(str1, str2):
    if len(str1) > len(str2):
        str1, str2 = str2, str1
    result = ""
    n1, n2 = len(str1), len(str2)
    str1, str2 = str1.zfill(n2), str2.zfill(n2)
    carry = 0
    for i in range(n2 - 1, -1, -1):
        sum_val = int(str1[i]) + int(str2[i]) + carry
        result = str(sum_val % 10) + result
        carry = sum_val // 10
    if carry:
        result = str(carry) + result
    return result

def findDiff(str1, str2):
    result = ""
    n1, n2 = len(str1), len(str2)
    str1, str2 = str1.zfill(n2), str2.zfill(n2)
    carry = 0
    for i in range(n2 - 1, -1, -1):
        sub = int(str1[i]) - int(str2[i]) - carry
        if sub < 0:
            sub += 10
            carry = 1
        else:
            carry = 0
        result = str(sub) + result
    return result

def removeLeadingZeros(s):
    return re.sub("^0+(?!$)", "", s)

def multiply(A, B):
    if len(A) < 10 or len(B) < 10:
        return str(int(A) * int(B))
    n = max(len(A), len(B))
    n2 = n // 2
    A, B = A.zfill(n), B.zfill(n)
    Al, Ar = A[:n2], A[n2:]
    Bl, Br = B[:n2], B[n2:]
    p = multiply(Al, Bl)
    q = multiply(Ar, Br)
    r = multiply(findSum(Al, Ar), findSum(Bl, Br))
    r = findDiff(r, findSum(p, q))
    return removeLeadingZeros(findSum(findSum(p + '0' * (2 * n2), r + '0' * n2), q))

def read_pairs_from_file(file_name):
    pairs = []
    with open(file_name, "r") as file:
        for line in file:
            x, y = line.split()
            pairs.append((x, y))
    return pairs

# Closest Pair Algorithm

# ... (previous code remains the same until the find_closest_pair function)

def find_closest_pair(points):
    # Convert input points to Point objects if they're not already
    point_objects = []
    for point in points:
        if isinstance(point, tuple):
            # Convert string coordinates to float
            x = float(point[0])
            y = float(point[1])
            point_objects.append(Point(x, y))
        else:
            point_objects.append(point)
    
    # Use the divide-and-conquer algorithm
    return closest_pair(point_objects)

def closest_pair(points: List[Point]) -> Tuple[Point, Point, float]:
    if len(points) < 2:
        return None, None, float('inf')
    
    # Sort points by x coordinate
    points_x = sorted(points, key=lambda p: p.x)
    points_y = sorted(points, key=lambda p: p.y)
    
    return closest_pair_recursive(points_x, points_y)

def dist(p1: Point, p2: Point) -> float:
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)




def closest_pair_recursive(points_x: List[Point], points_y: List[Point]) -> Tuple[Point, Point, float]:
    n = len(points_x)
    
    if n <= 3:
        return brute_force(points_x)
    
    mid = n // 2
    mid_point = points_x[mid]
    
    points_y_left = [p for p in points_y if p.x <= mid_point.x]
    points_y_right = [p for p in points_y if p.x > mid_point.x]
    
    left_p1, left_p2, left_min = closest_pair_recursive(points_x[:mid], points_y_left)
    right_p1, right_p2, right_min = closest_pair_recursive(points_x[mid:], points_y_right)
    
    min_dist = min(left_min, right_min)
    min_pair = (left_p1, left_p2) if left_min < right_min else (right_p1, right_p2)
    
    # Look for closer pair across the middle line
    strip = [p for p in points_y if abs(p.x - mid_point.x) < min_dist]
    
    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and strip[j].y - strip[i].y < min_dist:
            dist = strip[i].distance_to(strip[j])
            if dist < min_dist:
                min_dist = dist
                min_pair = (strip[i], strip[j])
            j += 1
    
    return min_pair[0], min_pair[1], min_dist

def brute_force(points: List[Point]) -> Tuple[Point, Point, float]:
    n = len(points)
    min_dist = float('inf')
    pair = (None, None)
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = points[i].distance_to(points[j])
            if dist < min_dist:
                min_dist = dist
                pair = (points[i], points[j])
    
    return pair[0], pair[1], min_dist

class IntegerMultiplicationPage:
    def __init__(self, root, return_callback):
        self.root = root
        self.return_callback = return_callback
        self.setup_gui()

    def setup_gui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Header
        tk.Label(self.frame, text="Integer Multiplication",
                font=('Helvetica', 16, 'bold')).pack(pady=10)

        # Input methods frame
        input_method_frame = tk.Frame(self.frame)
        input_method_frame.pack(pady=10)

        # Manual input area
        # manual_frame = tk.LabelFrame(input_method_frame, text="Manual Input")
        # manual_frame.pack(pady=10, padx=10, fill=tk.X)

        # tk.Label(manual_frame, text="Number 1:").grid(row=0, column=0, padx=5)
        # self.num1_entry = tk.Entry(manual_frame, width=40)
        # self.num1_entry.grid(row=0, column=1, padx=5)

        # tk.Label(manual_frame, text="Number 2:").grid(row=1, column=0, padx=5)
        # self.num2_entry = tk.Entry(manual_frame, width=40)
        # self.num2_entry.grid(row=1, column=1, padx=5)

        # File input area
        file_frame = tk.LabelFrame(input_method_frame, text="File Input")
        file_frame.pack(pady=10, padx=10, fill=tk.X)

        self.file_path = tk.StringVar()
        tk.Label(file_frame, text="Selected File:").pack(side=tk.LEFT, padx=5)
        tk.Label(file_frame, textvariable=self.file_path, width=40).pack(side=tk.LEFT, padx=5)
        tk.Button(file_frame, text="Browse",
                 command=self.load_file,
                 bg='#3498db', fg='white').pack(side=tk.LEFT, padx=5)

        # Buttons
        button_frame = tk.Frame(self.frame)
        button_frame.pack(pady=10)

        # tk.Button(button_frame, text="Calculate Manual",
        #          command=self.calculate_manual,
        #          bg='#2ecc71', fg='white').pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Calculate File",
                 command=self.calculate_file,
                 bg='#2ecc71', fg='white').pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Back to Main",
                 command=self.return_to_main,
                 bg='#e74c3c', fg='white').pack(side=tk.LEFT, padx=5)

        # Result area with scrollbar
        result_frame = tk.Frame(self.frame)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

        # Add scrollbars
        y_scrollbar = tk.Scrollbar(result_frame)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        x_scrollbar = tk.Scrollbar(result_frame, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Result text widget
        self.result_text = tk.Text(result_frame, 
                                 wrap=tk.NONE,
                                 yscrollcommand=y_scrollbar.set,
                                 xscrollcommand=x_scrollbar.set)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Configure scrollbars
        y_scrollbar.config(command=self.result_text.yview)
        x_scrollbar.config(command=self.result_text.xview)

    def load_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            self.file_path.set(filename)

    def calculate_manual(self):
        try:
            num1 = self.num1_entry.get()
            num2 = self.num2_entry.get()
            result = multiply(num1, num2)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"{num1} * {num2} = {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calculate_file(self):
        if not self.file_path.get():
            messagebox.showwarning("Warning", "Please select a file first.")
            return
        
        try:
            pairs = read_pairs_from_file(self.file_path.get())
            self.result_text.delete(1.0, tk.END)
            
            for i, (num1, num2) in enumerate(pairs, 1):
                result = multiply(num1, num2)
                self.result_text.insert(tk.END, f"Pair {i}:\n{num1} * {num2} = {result}\n\n")
                
            self.result_text.see("1.0")  # Scroll to top
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def return_to_main(self):
        self.frame.destroy()
        self.return_callback()

class ClosestPairVisualizer:
    def __init__(self, root, return_callback):
        self.root = root
        self.return_callback = return_callback
        self.setup_gui()

    def setup_gui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Controls frame
        controls_frame = tk.Frame(self.frame)
        controls_frame.pack(fill=tk.X, pady=5)

        tk.Button(controls_frame, text="Load File",
                 command=self.open_file,
                 bg='#3498db', fg='white').pack(side=tk.LEFT, padx=5)

        tk.Button(controls_frame, text="Back to Main",
                 command=self.return_to_main,
                 bg='#e74c3c', fg='white').pack(side=tk.LEFT, padx=5)

        # Plot frame
        self.plot_frame = tk.Frame(self.frame)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

        # Create matplotlib figure
        self.figure = plt.Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Add navigation toolbar (zoom, pan, etc.)
        toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        toolbar.update()

    def open_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            self.process_file(filename)

    def process_file(self, filename):
        try:
            pairs = read_pairs_from_file(filename)
            points = [Point(float(x), float(y)) for x, y in pairs]
            p1, p2, min_dist = find_closest_pair(points)

            self.ax.clear()
            x_coords = [p.x for p in points]
            y_coords = [p.y for p in points]
            
            # Plot all points
            self.ax.scatter(x_coords, y_coords, c='lightblue', alpha=0.6, label='Points')

            if p1 and p2:
                # Plot closest points and their connecting line
                self.ax.scatter([p1.x, p2.x], [p1.y, p2.y], c='orange', s=100, label='Closest Points')
                self.ax.plot([p1.x, p2.x], [p1.y, p2.y], 'r--', label='Distance Line')
                
                # # Add annotations with coordinates
                # self.ax.annotate(f'({p1.x:.2f}, {p1.y:.2f})',
                #             (p1.x, p1.y),
                #             xytext=(10, 10),
                #             textcoords='offset points')
                # self.ax.annotate(f'({p2.x:.2f}, {p2.y:.2f})',
                #             (p2.x, p2.y),
                #             xytext=(10, 10),
                #             textcoords='offset points')

            self.ax.set_title(f'Closest Pair of Points\nDistance: {min_dist:.2f}\n' +
                            f'Point 1: ({p1.x:.2f}, {p1.y:.2f})\n' +
                            f'Point 2: ({p2.x:.2f}, {p2.y:.2f})')
            self.ax.set_xlabel('X Coordinate')
            self.ax.set_ylabel('Y Coordinate')
            self.ax.grid(True)
            self.ax.legend()

            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def setup_gui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Controls frame
        controls_frame = tk.Frame(self.frame)
        controls_frame.pack(fill=tk.X, pady=5)

        tk.Button(controls_frame, text="Load File",
                command=self.open_file,
                bg='#3498db', fg='white').pack(side=tk.LEFT, padx=5)

        tk.Button(controls_frame, text="Back to Main",
                command=self.return_to_main,
                bg='#e74c3c', fg='white').pack(side=tk.LEFT, padx=5)

        # Plot frame
        self.plot_frame = tk.Frame(self.frame)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

        # Create matplotlib figure
        self.figure = plt.Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Add navigation toolbar with zoom and pan capabilities
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.update()

        # # Add reset view button
        # tk.Button(controls_frame,
        #         text="Reset View",
        #         command=self.reset_view,
        #         bg='#3498db',
        #         fg='white').pack(side=tk.LEFT, padx=5)

    # def reset_view(self):
    #     self.ax.relim()
    #     self.ax.autoscale()
    #     self.canvas.draw()

    def return_to_main(self):
        self.frame.destroy()
        self.return_callback()


class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Visualizer")
        self.setup_main_menu()

    def setup_main_menu(self):
        # Create main menu frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(self.main_frame,
                text="Algorithm Visualizer",
                font=('Helvetica', 24, 'bold')).pack(pady=20)

        # Buttons
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(expand=True)

        tk.Button(button_frame,
                 text="Integer Multiplication",
                 command=self.show_multiplication,
                 width=20,
                 height=2,
                 bg='#3498db',
                 fg='white',
                 font=('Helvetica', 12)).pack(pady=10)

        tk.Button(button_frame,
                 text="Closest Pair of Points",
                 command=self.show_closest_pair,
                 width=20,
                 height=2,
                 bg='#2ecc71',
                 fg='white',
                 font=('Helvetica', 12)).pack(pady=10)

        tk.Button(button_frame,
                 text="Exit",
                 command=self.root.quit,
                 width=20,
                 height=2,
                 bg='#e74c3c',
                 fg='white',
                 font=('Helvetica', 12)).pack(pady=10)

    def show_multiplication(self):
        self.main_frame.pack_forget()
        IntegerMultiplicationPage(self.root, self.return_to_main)

    def show_closest_pair(self):
        self.main_frame.pack_forget()
        ClosestPairVisualizer(self.root, self.return_to_main)

    def return_to_main(self):
        self.main_frame.pack(fill=tk.BOTH, expand=True)

def main():
    root = tk.Tk()
    root.geometry("800x600")
    app = MainApplication(root)
    root.mainloop()

if __name__ == "__main__":
    generate_for_karatsuba.run()
    generate_for_cpp.run()
    main()