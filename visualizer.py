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
        self.root.minsize(900, 600)  # Set minimum window size
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
        
        # Bind resize event
        self.root.bind('<Configure>', self._on_window_resize)

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
            to=99,
            textvariable=self.size_var,
            width=10,
            command=self._on_size_change
        )
        size_spinbox.pack(side="left", padx=5)
        # Bind Enter key and focus out to also trigger size change
        size_spinbox.bind('<Return>', lambda e: self._on_size_change())
        size_spinbox.bind('<FocusOut>', lambda e: self._on_size_change())

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

        # Custom Array Input
        input_frame = ttk.LabelFrame(self.root, text="Custom Array Input", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Enter numbers (comma or space separated):", font=("Arial", 9)).pack(side="left", padx=5)
        self.custom_input = ttk.Entry(input_frame, width=40, font=("Arial", 10))
        self.custom_input.pack(side="left", padx=5)
        self.custom_input.insert(0, "64, 34, 25, 12, 22, 11, 90")  # Example
        
        ttk.Button(input_frame, text="Load Custom Array", command=self._load_custom_array).pack(side="left", padx=5)
        
        self.input_status = ttk.Label(input_frame, text="", font=("Arial", 8), foreground="gray")
        self.input_status.pack(side="left", padx=5)

        # Canvas for visualization
        canvas_frame = ttk.LabelFrame(self.root, text="Visualization", padding=5)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(canvas_frame, bg="white", height=350)
        self.canvas.pack(fill="both", expand=True)
        
        # Force canvas to update its size
        self.root.update_idletasks()

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

    def _on_size_change(self):
        """Handle array size change."""
        if not self.running:  # Only allow if not currently sorting
            self._generate_random_array()

    def _generate_random_array(self):
        """Generate a random array based on size."""
        size = self.size_var.get()
        self.array = [random.randint(5, 380) for _ in range(size)]
        self.visual_array = self.array[:]
        self.root.update_idletasks()  # Update canvas size
        self._draw_array()
        self._reset_stats()
        try:
            self.input_status.config(text="")
        except tk.TclError:
            pass

    def _load_custom_array(self):
        """Load custom array from user input."""
        try:
            # Get input and parse
            input_text = self.custom_input.get().strip()
            if not input_text:
                try:
                    self.input_status.config(text="⚠️ Please enter numbers", foreground="red")
                except tk.TclError:
                    pass
                return
            
            # Parse numbers (handle both comma and space separated)
            numbers = []
            for item in input_text.replace(',', ' ').split():
                num = int(item)
                if num < 1 or num > 400:
                    try:
                        self.input_status.config(text="⚠️ Numbers must be between 1-400", foreground="red")
                    except tk.TclError:
                        pass
                    return
                numbers.append(num)
            
            if len(numbers) < 2:
                try:
                    self.input_status.config(text="⚠️ Enter at least 2 numbers", foreground="red")
                except tk.TclError:
                    pass
                return
            
            if len(numbers) > 1000:
                try:
                    self.input_status.config(text="⚠️ Maximum 1000 numbers allowed", foreground="red")
                except tk.TclError:
                    pass
                return
            
            # Load the custom array
            self.array = numbers
            self.visual_array = self.array[:]
            self.root.update_idletasks()  # Update canvas size
            self._draw_array()
            self._reset_stats()
            try:
                self.input_status.config(text=f"✓ Loaded {len(numbers)} numbers", foreground="green")
            except tk.TclError:
                pass
            
        except ValueError:
            try:
                self.input_status.config(text="⚠️ Invalid input. Enter only numbers", foreground="red")
            except tk.TclError:
                pass

    def _draw_array(self, highlight=None, highlight_color="orange"):
        """Draw the array on canvas."""
        try:
            if not self.root.winfo_exists():
                return
        except tk.TclError:
            return
            
        self.canvas.delete("all")
        
        if not self.visual_array:
            return

        # Get current canvas size (avoid update_idletasks during animation)
        try:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
        except tk.TclError:
            return
        
        # Use default size if canvas not yet rendered
        if canvas_width <= 1:
            canvas_width = 1100
        if canvas_height <= 1:
            canvas_height = 350

        n = len(self.visual_array)
        bar_width = canvas_width / n
        max_val = max(self.visual_array) if self.visual_array else 1

        highlight_set = set(highlight) if highlight else set()

        for i, val in enumerate(self.visual_array):
            x0 = i * bar_width
            x1 = x0 + bar_width - 2
            
            # Scale bar height with padding
            bar_height = (val / max_val) * (canvas_height - 30)
            y0 = canvas_height - bar_height - 5
            y1 = canvas_height - 5

            if i in highlight_set:
                color = highlight_color
            else:
                color = "#4A90E2"

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
            
            # Add number labels on bars - always show if there's space
            if bar_width > 12 and n <= 60:  # Show numbers on up to 60 bars
                text_x = (x0 + x1) / 2
                
                # Position text based on bar height
                if bar_height > 25:
                    text_y = y0 - 8  # Above bar
                    text_color = "black"
                else:
                    text_y = y1 - 8  # Inside bar
                    text_color = "white"
                
                # Adjust font size based on bar width
                font_size = int(max(7, min(bar_width/2.5, 11)))
                
                self.canvas.create_text(
                    text_x, text_y,
                    text=str(val),
                    font=("Arial", font_size, "bold"),
                    fill=text_color
                )

        # Only update canvas, not entire GUI (reduces flickering)
        self.canvas.update()

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
        """Reset to initial state - stops sorting and restores original array."""
        self.running = False
        self.paused = False
        self.generator = None
        self.visual_array = self.array[:]  # Reset to original unsorted array
        self._draw_array()
        self._reset_stats()
        try:
            self.status_label.config(text="Reset")
        except tk.TclError:
            pass

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
        try:
            if not self.root.winfo_exists():
                return
            self.comp_label.config(text=str(self.comparisons))
            self.swap_label.config(text=str(self.swaps))
            self.write_label.config(text=str(self.writes))
            self.steps_label.config(text=str(self.total_steps))
            
            if self.start_time:
                self.elapsed_time = time.time() - self.start_time
            self.time_label.config(text=f"{self.elapsed_time:.2f}s")
        except tk.TclError:
            # Widget was destroyed, stop updates
            self.running = False

    def _step(self):
        """Execute one step of the sorting algorithm."""
        if not self.running or not self.generator:
            return
        
        # Check if window still exists
        try:
            if not self.root.winfo_exists():
                self.running = False
                return
        except tk.TclError:
            self.running = False
            return

        try:
            step: Step = next(self.generator)
            self.total_steps += 1

            # Update stats based on step type
            if step.type == "compare":
                self.comparisons += 1
                # Check bounds
                if step.i is not None and step.j is not None and \
                   0 <= step.i < len(self.visual_array) and 0 <= step.j < len(self.visual_array):
                    highlight = [step.i, step.j]
                else:
                    highlight = []
                color = "#FF5733"
            elif step.type == "swap":
                self.swaps += 1
                # Check bounds before swapping
                if step.i is not None and step.j is not None and \
                   0 <= step.i < len(self.visual_array) and 0 <= step.j < len(self.visual_array):
                    self.visual_array[step.i], self.visual_array[step.j] = \
                        self.visual_array[step.j], self.visual_array[step.i]
                    highlight = [step.i, step.j]
                else:
                    highlight = []
                color = "#28A745"
            elif step.type == "overwrite":
                self.writes += 1
                # Check bounds before overwriting
                if step.i is not None and 0 <= step.i < len(self.visual_array) and step.value is not None:
                    self.visual_array[step.i] = step.value
                    highlight = [step.i]
                else:
                    highlight = []
                color = "#FFC300"
            elif step.type == "complete":
                highlight = None
                color = "#4A90E2"
            elif step.type == "done":
                self.running = False
                try:
                    self.status_label.config(text="Completed!")
                    self.info_label.config(text=step.description)
                except tk.TclError:
                    pass
                self._draw_array()
                self._update_stats_display()
                return

            # Draw array with highlights
            self._draw_array(highlight, color)
            
            # Update info label only if description changed
            if step.description:
                try:
                    self.info_label.config(text=step.description)
                except tk.TclError:
                    self.running = False
                    return
            
            # Update stats less frequently for smoother animation
            if self.total_steps % 5 == 0:  # Update every 5 steps
                self._update_stats_display()

            # Schedule next step
            delay = max(1, self.speed_var.get())
            self.root.after(delay, self._step)

        except StopIteration:
            self.running = False
            try:
                self.status_label.config(text="Completed!")
            except tk.TclError:
                pass
            self._draw_array()
            self._update_stats_display()

    def _on_window_resize(self, event):
        """Handle window resize events."""
        # Only redraw if not currently sorting
        if not self.running and self.visual_array:
            # Delay redraw slightly to avoid too many redraws
            if hasattr(self, '_resize_job'):
                self.root.after_cancel(self._resize_job)
            self._resize_job = self.root.after(100, self._draw_array)


def main():
    """Launch the visualizer."""
    root = tk.Tk()
    visualizer = SortingVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
