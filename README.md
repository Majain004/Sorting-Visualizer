# Sorting Algorithm Visualizer

A professional, interactive visualization tool for understanding and comparing sorting algorithms in real-time.

## Features

### 🎨 Interactive Visualization
- **Real-time animation** of sorting algorithms
- **Color-coded operations**: 
  - Red: Comparisons
  - Green: Swaps
  - Yellow: Write operations
- **Adjustable speed control** for viewing at your own pace
- **Array size customization** (10-200 elements)

### 📊 Statistics Tracking
- **Live metrics display**:
  - Number of comparisons
  - Number of swaps
  - Number of write operations
  - Total operation count
  - Elapsed time
- **Real-time status updates**

### 🔬 Algorithms Included
1. **Bubble Sort** - O(n²) - Simple but inefficient
2. **Selection Sort** - O(n²) - Minimal swaps
3. **Insertion Sort** - O(n²) average, O(n) best - Efficient for small arrays
4. **Merge Sort** - O(n log n) - Divide & conquer
5. **Quick Sort** - O(n log n) average, O(n²) worst - Practical choice
6. **Heap Sort** - O(n log n) - In-place sorting

### ⚡ Benchmark Tool
- Compare performance of all algorithms
- Test with different array sizes
- Generate performance reports
- Identify the fastest and slowest algorithms

## Project Structure

```
Sorting/
├── visualizer.py       # Main GUI application
├── algorithms.py       # Sorting algorithm implementations
├── benchmark.py        # Performance benchmarking tool
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Installation & Usage

### Prerequisites
- Python 3.6+
- tkinter (included with most Python installations)

### Running the Visualizer

```bash
python visualizer.py
```

### Running the Benchmark

```bash
python benchmark.py
```

## How It Works

### Algorithm Steps
Each algorithm yields `Step` objects with information about:
- **Type**: compare, swap, overwrite, complete, done
- **Indices**: positions being accessed
- **Value**: value being written (for overwrites)
- **Description**: human-readable operation description

### Visualization Process
1. Select an algorithm from the dropdown
2. Choose array size (or generate new random array)
3. Adjust animation speed
4. Click "Start" to begin visualization
5. Watch real-time statistics update
6. "Pause" to freeze the animation
7. "Reset" to start over

## Code Quality Features

✅ **Type Hints** - Full type annotations for better IDE support  
✅ **Documentation** - Comprehensive docstrings and comments  
✅ **Clean Code** - Follows PEP 8 style guidelines  
✅ **Efficient** - Optimized algorithm implementations  
✅ **Professional UI** - Modern tkinter interface  
✅ **Error Handling** - Robust exception management  

## Performance Insights

### Time Complexity Comparison
| Algorithm | Best | Average | Worst | Space |
|-----------|------|---------|-------|-------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) |

## Learning Outcomes

This project helps you understand:
- How different sorting algorithms work
- Time and space complexity trade-offs
- Visual difference between algorithm approaches
- Performance characteristics in practice
- Generator functions in Python
- Professional GUI design with tkinter

## Resume Highlights

This project demonstrates:
- 🎓 **Data Structures & Algorithms** knowledge
- 💻 **GUI Development** with tkinter
- 📈 **Performance Analysis** and optimization
- 🔧 **Code Quality** with type hints and documentation
- 🎨 **UI/UX Design** principles
- 📊 **Benchmarking** and metrics tracking
- ⚙️ **Software Engineering** best practices

## Future Enhancements

- [ ] Additional algorithms (Radix Sort, Counting Sort, etc.)
- [ ] Sound effects for operations
- [ ] Export statistics to CSV
- [ ] Comparison mode (run multiple algorithms side-by-side)
- [ ] Dark/Light theme toggle
- [ ] Array input from file
- [ ] Step-by-step debugging mode

## Author

Created as an educational project for learning data structures and algorithms.

## License

Free to use for educational purposes.

---

**Happy Sorting! 🎉**
