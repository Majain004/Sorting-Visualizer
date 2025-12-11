# ============================================================================
# Sorting Algorithm Visualizer
# Interactive GUI for visualizing sorting algorithms in real-time
# ============================================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import time
from algorithms import ALGORITHMS, Step


class SortingVisualizer:
    """Professional sorting algorithm visualizer with real-time statistics."""

    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer | Professional Edition")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")

        # State variables
        self.array = []
        self.visual_array = []
        self.generator = None
        self.running = False
        self.paused = False
        self.current_algorithm = "Bubble Sort"

        # Statistics
        self.comparisons = 0
        self.swaps = 0
        self.writes = 0
        self.total_steps = 0
        self.start_time = None
        self.elapsed_time = 0.0

        # UI Setup
        self._setup_ui()
        self._generate_random_array()

    def _setup_ui(self):
        """Setup the complete UI."""
        # Top Control Panel
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill="x", padx=10, pady=10)

        # Algorithm Selection
        ttk.Label(top_frame, text="Algorithm:", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        self.algo_var = tk.StringVar(value="Bubble Sort")
        algo_menu = ttk.Combobox(
            top_frame,
            textvariable=self.algo_var,
            values=list(ALGORITHMS.keys()),
            state="readonly",
            width=18
        )
        algo_menu.pack(side="left", padx=5)
        algo_menu.bind("<<ComboboxSelected>>", lambda e: self._reset_stats())

        # Array Size
        ttk.Label(top_frame, text="Array Size:", font=("Arial", 10, "bold")).pack(side="left", padx=20)
        self.size_var = tk.IntVar(value=50)
        size_spinbox = ttk.Spinbox(
            top_frame,
            from_=10,
            to=200,
            textvariable=self.size_var,
            width=10
        )
        size_spinbox.pack(side="left", padx=5)

        # Speed Control
        ttk.Label(top_frame, text="Speed (ms):", font=("Arial", 10, "bold")).pack(side="left", padx=20)
        self.speed_var = tk.IntVar(value=30)
        speed_scale = ttk.Scale(
            top_frame,
            from_=1,
            to=200,
            variable=self.speed_var,
            orient="horizontal",
            length=150
        )
        speed_scale.pack(side="left", padx=5)

        # Buttons
        button_frame = ttk.Frame(top_frame)
        button_frame.pack(side="left", padx=20)

        ttk.Button(button_frame, text="Generate", command=self._generate_random_array).pack(side="left", padx=3)
        ttk.Button(button_frame, text="Start", command=self._start_sort).pack(side="left", padx=3)
        ttk.Button(button_frame, text="Pause", command=self._pause_sort).pack(side="left", padx=3)
        ttk.Button(button_frame, text="Reset", command=self._reset).pack(side="left", padx=3)

        # Canvas for visualization
        canvas_frame = ttk.LabelFrame(self.root, text="Visualization", padding=5)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(canvas_frame, bg="white", height=350)
        self.canvas.pack(fill="both", expand=True)

        # Statistics Panel
        stats_frame = ttk.LabelFrame(self.root, text="Statistics", padding=10)
        stats_frame.pack(fill="x", padx=10, pady=5)

        stats_inner = ttk.Frame(stats_frame)
        stats_inner.pack(fill="x")

        # Left side stats
        left_stats = ttk.Frame(stats_inner)
        left_stats.pack(side="left", padx=20)

        ttk.Label(left_stats, text="Comparisons:", font=("Arial", 9, "bold")).pack(anchor="w")
        self.comp_label = ttk.Label(left_stats, text="0", font=("Arial", 12), foreground="blue")
        self.comp_label.pack(anchor="w")

        ttk.Label(left_stats, text="Swaps:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(10, 0))
        self.swap_label = ttk.Label(left_stats, text="0", font=("Arial", 12), foreground="green")
        self.swap_label.pack(anchor="w")

        # Middle stats
        mid_stats = ttk.Frame(stats_inner)
        mid_stats.pack(side="left", padx=20)

        ttk.Label(mid_stats, text="Writes:", font=("Arial", 9, "bold")).pack(anchor="w")
        self.write_label = ttk.Label(mid_stats, text="0", font=("Arial", 12), foreground="orange")
        self.write_label.pack(anchor="w")

        ttk.Label(mid_stats, text="Total Steps:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(10, 0))
        self.steps_label = ttk.Label(mid_stats, text="0", font=("Arial", 12), foreground="purple")
        self.steps_label.pack(anchor="w")

        # Right stats
        right_stats = ttk.Frame(stats_inner)
        right_stats.pack(side="left", padx=20)

        ttk.Label(right_stats, text="Time:", font=("Arial", 9, "bold")).pack(anchor="w")
        self.time_label = ttk.Label(right_stats, text="0.00s", font=("Arial", 12), foreground="red")
        self.time_label.pack(anchor="w")

        ttk.Label(right_stats, text="Status:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(10, 0))
        self.status_label = ttk.Label(right_stats, text="Ready", font=("Arial", 12), foreground="darkgreen")
        self.status_label.pack(anchor="w")

        # Info label
        self.info_label = ttk.Label(self.root, text="", font=("Arial", 9), foreground="gray")
        self.info_label.pack(anchor="w", padx=10, pady=5)

    def _generate_random_array(self):
        """Generate a random array based on size."""
        size = self.size_var.get()
        self.array = [random.randint(5, 380) for _ in range(size)]
        self.visual_array = self.array[:]
        self._draw_array()
        self._reset_stats()

    def _draw_array(self, highlight=None, highlight_color="orange"):
        """Draw the array on canvas."""
        self.canvas.delete("all")
        
        if not self.array:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            return

        n = len(self.visual_array)
        bar_width = canvas_width / n
        max_val = max(self.array) if self.array else 1

        highlight_set = set(highlight) if highlight else set()

        for i, val in enumerate(self.visual_array):
            x0 = i * bar_width
            x1 = x0 + bar_width - 1
            
            # Scale bar height
            bar_height = (val / max_val) * (canvas_height - 20)
            y0 = canvas_height - bar_height
            y1 = canvas_height

            if i in highlight_set:
                color = highlight_color
            else:
                color = "#4A90E2"

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

        self.root.update_idletasks()

    def _start_sort(self):
        """Start the sorting animation."""
        if self.running:
            return

        self.running = True
        self.paused = False
        self.generator = ALGORITHMS[self.algo_var.get()](self.array[:])
        self.start_time = time.time()
        self._reset_stats()
        self._step()

    def _pause_sort(self):
        """Pause the sorting animation."""
        self.running = False
        self.paused = True
        self.status_label.config(text="Paused")

    def _reset(self):
        """Reset to initial state."""
        self.running = False
        self.paused = False
        self.generator = None
        self._generate_random_array()
        self.status_label.config(text="Ready")

    def _reset_stats(self):
        """Reset statistics."""
        self.comparisons = 0
        self.swaps = 0
        self.writes = 0
        self.total_steps = 0
        self.elapsed_time = 0.0
        self._update_stats_display()

    def _update_stats_display(self):
        """Update the statistics display."""
        self.comp_label.config(text=str(self.comparisons))
        self.swap_label.config(text=str(self.swaps))
        self.write_label.config(text=str(self.writes))
        self.steps_label.config(text=str(self.total_steps))
        
        if self.start_time:
            self.elapsed_time = time.time() - self.start_time
        self.time_label.config(text=f"{self.elapsed_time:.2f}s")

    def _step(self):
        """Execute one step of the sorting algorithm."""
        if not self.running or not self.generator:
            return

        try:
            step: Step = next(self.generator)
            self.total_steps += 1

            # Update stats based on step type
            if step.type == "compare":
                self.comparisons += 1
                highlight = [step.i, step.j]
                color = "#FF5733"
            elif step.type == "swap":
                self.swaps += 1
                self.visual_array[step.i], self.visual_array[step.j] = \
                    self.visual_array[step.j], self.visual_array[step.i]
                highlight = [step.i, step.j]
                color = "#28A745"
            elif step.type == "overwrite":
                self.writes += 1
                self.visual_array[step.i] = step.value
                highlight = [step.i]
                color = "#FFC300"
            elif step.type == "complete":
                highlight = None
                color = "#4A90E2"
            elif step.type == "done":
                self.running = False
                self.status_label.config(text="Completed!")
                self.info_label.config(text=step.description)
                self._draw_array()
                self._update_stats_display()
                return

            self._draw_array(highlight, color)
            self.info_label.config(text=step.description)
            self._update_stats_display()

            # Schedule next step
            delay = max(1, self.speed_var.get())
            self.root.after(delay, self._step)

        except StopIteration:
            self.running = False
            self.status_label.config(text="Completed!")
            self._draw_array()
            self._update_stats_display()


def main():
    """Launch the visualizer."""
    root = tk.Tk()
    visualizer = SortingVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
